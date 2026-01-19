import requests
from bs4 import BeautifulSoup
import pdfkit
import os
import re
import sys

class WeChatArticlePDF:
    def __init__(self, wkhtmltopdf_path=None):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        }
        
        if wkhtmltopdf_path:
            self.config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
        else:
            try:
                self.config = pdfkit.configuration()
            except OSError:
                print("[-] 错误: 未在系统路径中找到 wkhtmltopdf")
                sys.exit(1)

        # 容错配置
        self.options = {
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'no-outline': None,
            'enable-local-file-access': None,
            'load-error-handling': 'ignore', 
            'load-media-error-handling': 'ignore'
        }

    def fetch_and_process(self, url):
        print(f"[*] 正在请求: {url}")
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
        except Exception as e:
            print(f"[-] 网络错误: {e}")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')

        # 1. 获取标题
        title_tag = soup.find("meta", property="og:title")
        title = title_tag.get("content").strip() if title_tag else "wechat_article"
        title = re.sub(r'[\\/*?:"<>|]', "", title)[:60] # 清洗并截断文件名

        # 2. 定位正文核心区域 (id="js_content")
        content_div = soup.find(id="js_content")
        if not content_div:
            print("[-] 错误: 无法找到文章正文内容 (id=js_content 缺失)")
            return None

        # === 核心修复: 强制设置可见性 ===
        # 微信源码里这里通常是 visibility: hidden，必须移除或覆盖
        if 'style' in content_div.attrs:
            del content_div['style'] # 直接干掉 style 属性，最彻底

        # 3. 处理图片懒加载
        for img in content_div.find_all('img'):
            # 处理 src
            if 'data-src' in img.attrs:
                img['src'] = img['data-src']
            
            # 清理图片样式，防止 hidden 或 height:0
            if 'style' in img.attrs:
                del img['style']  

        # 4. 移除视频/iframe (PDF 无法播放，且容易导致渲染错误)
        for tag in content_div.find_all(['iframe', 'script', 'noscript']):
            tag.decompose()

        # 5. 重组 HTML
        html_template = f"""
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <title>{title}</title>
            <style>
                body {{ 
                    font-family: "Microsoft YaHei", sans-serif; 
                    padding: 20px; 
                }}
                /* 确保图片自适应 A4 纸宽度，不溢出 */
                img {{ 
                    max-width: 100% !important; 
                    height: auto !important; 
                    display: block; 
                    margin: 10px auto; 
                }}
                /* 如果有代码块，稍微美化一下 */
                pre, code {{
                    white-space: pre-wrap;
                    word-break: break-all;
                    background: #f5f5f5;
                }}
                /* 文章标题样式 */
                .export-title {{
                    font-size: 24px;
                    font-weight: bold;
                    margin-bottom: 20px;
                    text-align: center;
                }}
            </style>
        </head>
        <body>
            <div class="export-title">{title}</div>
            {str(content_div)} 
        </body>
        </html>
        """
        
        return html_template, title

    def convert(self, url, output_dir="output"):
        result = self.fetch_and_process(url)
        if not result:
            return

        html_str, title = result
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        output_path = os.path.abspath(os.path.join(output_dir, f"{title}.pdf"))

        print(f"[*] 正在生成 PDF: {output_path}")
        try:
            pdfkit.from_string(html_str, output_path, configuration=self.config, options=self.options)
            print(f"[+] 成功! 文件已保存。")
        except Exception as e:
            # 只要文件生成了，就算成功（忽略网络小错误）
            if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
                print(f"[+] 转换完成 (忽略非致命资源错误)。已保存: {output_path}")
            else:
                print(f"[-] 失败: {e}")

if __name__ == "__main__":
    WKHTMLTOPDF_PATH = None 
    converter = WeChatArticlePDF(wkhtmltopdf_path=WKHTMLTOPDF_PATH)
    
    url = input("请输入链接: ").strip()
    if url:
        converter.convert(url)