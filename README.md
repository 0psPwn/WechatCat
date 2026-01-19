# WechatCat

WechatCat 是一个轻量级的 Python 工具，用于将微信公众号文章转换为高质量的 PDF 文件。它能够自动处理微信文章的各种格式问题，包括图片懒加载、内容可见性等，确保生成的 PDF 文档保持文章的原始排版和内容完整性。

## 功能特性

- 📥 **自动获取文章内容**：通过微信公众号文章 URL 自动获取标题和正文内容
- 📝 **智能内容处理**：
  - 自动处理图片懒加载问题
  - 清理微信文章特有的隐藏样式
  - 移除不必要的元素（视频、iframe 等）
  - 优化图片显示和尺寸
- 📄 **高质量 PDF 输出**：
  - 保持文章原始排版
  - 支持自定义页面设置（A4 纸张、边距等）
  - 自动命名 PDF 文件（基于文章标题）
- 🛡️ **容错机制**：
  - 处理网络请求错误
  - 忽略非致命资源加载错误
  - 文件名自动清理和截断

## 安装要求

### 系统依赖

- Python 3.6+
- wkhtmltopdf (用于 HTML 到 PDF 的转换)

### Python 依赖

```
requests
beautifulsoup4
pdfkit
```

## 安装步骤

1. **安装 Python 依赖**：

```bash
pip install requests beautifulsoup4 pdfkit
```

2. **安装 wkhtmltopdf**：
   - **Windows**: 下载地址 https://wkhtmltopdf.org/downloads.html
   - **macOS**: 使用Homebrew安装 `brew install wkhtmltopdf`
   - **Linux**: 使用包管理器安装，例如 `apt-get install wkhtmltopdf`
   - OR

## 使用方法

### 基本使用

1. 克隆或下载本项目

2. 运行主程序：

```bash
python main.py
```

3. 根据提示输入微信公众号文章的 URL：

```
请输入链接: https://mp.weixin.qq.com/s/xxxxxxxxxxxxxxxxx
```

4. 转换完成后，PDF 文件将保存在项目目录下的 `output` 文件夹中

### 自定义 wkhtmltopdf 路径

如果 wkhtmltopdf 未添加到系统 PATH，可以在代码中指定其路径：

```python
if __name__ == "__main__":
    WKHTMLTOPDF_PATH = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"  # Windows 示例路径
    converter = WeChatArticlePDF(wkhtmltopdf_path=WKHTMLTOPDF_PATH)
    
    url = input("请输入链接: ").strip()
    if url:
        converter.convert(url)
```

### 批量转换

可以修改代码，添加批量处理功能：

```python
if __name__ == "__main__":
    converter = WeChatArticlePDF()
    
    urls = [
        "https://mp.weixin.qq.com/s/xxxxxxxxxxxxxxxxx",
        "https://mp.weixin.qq.com/s/yyyyyyyyyyyyyyyyy",
        # 添加更多 URL
    ]
    
    for url in urls:
        converter.convert(url)
```

## 项目结构

```
WechatCat/
├── main.py        # 主程序文件
├── output/        # PDF 输出目录
└── README.md      # 项目说明文档
```

### 配置选项

程序提供了丰富的 PDF 生成配置选项：

```python
options = {
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
```

## 常见问题

### 1. 转换失败，提示找不到 wkhtmltopdf

**解决方案**：确保已正确安装 wkhtmltopdf 并将其添加到系统 PATH，或在代码中指定其路径。

### 2. PDF 中图片显示不完整或模糊

**解决方案**：微信公众号文章的图片通常经过压缩，转换后的清晰度取决于原始图片质量。程序已优化图片显示设置，确保最佳效果。

### 3. 部分内容在 PDF 中不显示

**解决方案**：程序已处理微信文章特有的隐藏样式，但某些特殊格式可能仍存在兼容性问题。可以尝试修改 HTML 处理逻辑以适应特定文章格式。

# 免责声明

- **本软件提供的所有内容，仅可用作学习交流使用，禁止用于其他用途。请在下载24小时内删除。为尊重作者版权，请前往资源的原始发布网站观看，支持原创，谢谢。**