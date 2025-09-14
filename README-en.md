# 📄 PDF Compressor

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI - Downloads](https://img.shields.io/badge/downloads-1k%2Fmonth-brightgreen)](https://github.com/laurent-deberti/pdf-compressor)

A powerful and intelligent Python script for compressing PDF files with automatic content type detection.

## ✨ Key Features

- 🧠 **Intelligent automatic detection**: Analyzes content and chooses the best strategy
- 🖼️ **Advanced image compression**: PNG→JPEG conversion, intelligent resizing
- ⚡ **Up to 95% reduction**: Spectacular results on scanned PDFs
- 🔧 **Robust**: Automatic fallback, error handling, original preservation
- 📁 **Batch processing**: Compress entire folders
- 🛠️ **Advanced tools**: Analysis, diagnostics, precise control

## 📊 Performance Examples

| PDF Type | Original Size | Compressed Size | Reduction |
|----------|---------------|-----------------|-----------|
| Scanned document (PNG images) | 22.3 MB | 1.2 MB | **94.5%** |
| Presentation with photos | 15.8 MB | 4.2 MB | **73.4%** |
| Text document | 8.5 MB | 3.1 MB | **63.5%** |

## 🚀 Quick Installation

```bash
# Clone the repository
git clone https://github.com/laurent-deberti/pdf-compressor.git
cd pdf-compressor

# Install dependencies
pip install -r requirements.txt

# Test installation
python tools/test_setup.py
```

## ⚡ Usage

### Simple compression (recommended)
```bash
python compress_pdf.py your_file.pdf
```

### Advanced options
```bash
# Specify output file
python compress_pdf.py input.pdf -o output_compressed.pdf

# Choose compression level
python compress_pdf.py input.pdf -l high

# Specific method
python compress_pdf.py input.pdf -m pikepdf
```

## 📋 Available Options

### Arguments
- `input`: Input PDF file (required)
- `-o, --output`: Output PDF file (default: `original_name_compressed.pdf`)
- `-m, --method`: Compression method (`auto`, `pikepdf`, `fitz`, `pypdf`)
- `-l, --level`: Compression level (`low`, `medium`, `high`)

### Compression Methods

| Method | Description | Recommended for |
|--------|-------------|-----------------|
| `auto` | **Automatic detection (default)** | General use |
| `pikepdf` | Modern and efficient | Text documents, forms |
| `fitz` | PyMuPDF - high performance | Large files, images |
| `pypdf` | PyPDF2 - compatible | Maximum compatibility |

## 🛠️ Advanced Tools

Specialized tools are available in the `tools/` folder:

- **Specialized image compression**: `python tools/compress_image_pdf.py`
- **Batch processing**: `python tools/batch_compress.py`
- **PDF analysis**: `python tools/analyze_pdf.py`
- **Testing and diagnostics**: `python tools/test_setup.py`

See [`tools/README.md`](tools/README.md) for details.

## 🧠 How It Works

### Intelligent Automatic Detection
The script automatically analyzes PDF content:

1. **PDFs with large images** → Advanced image compression
   - PNG → JPEG conversion with adjustable quality
   - Intelligent resizing
   - Up to 95% reduction

2. **Mainly text PDFs** → Optimized classic compression
   - Stream compression
   - Object optimization
   - 20-50% reduction

3. **Mixed PDFs** → Best method based on dominant content

### Robustness
- **Automatic fallback**: If one method fails, tries others
- **Validation**: Verifies compression actually reduces size
- **Preservation**: Never modifies the original file

## 📚 Documentation

- [**French README**](README.md) - Documentation française
- [**English README**](README-en.md) - This file
- [**Tools Guide**](tools/README.md) - Advanced tools documentation

## 🔧 Requirements

- Python 3.7+
- Dependencies: `pikepdf`, `PyMuPDF`, `PyPDF2`, `Pillow`

## 🐛 Troubleshooting

### Dependencies Installation
```bash
# If pip install fails
python tools/install_deps.py

# Or bash installation
bash tools/install.sh
```

### Diagnostics
```bash
# Check installation
python tools/test_setup.py

# Analyze problematic PDF
python tools/analyze_pdf.py file.pdf
```

## 💡 Use Cases

### Work documents
```bash
python compress_pdf.py report.pdf
```

### Email sending (maximum compression)
```bash
python compress_pdf.py presentation.pdf -l high
```

### Archive folder processing
```bash
python tools/batch_compress.py ~/Documents/Archives/
```

### Precise quality control
```bash
python tools/compress_image_pdf.py scan.pdf -q 60 -w 800
```

## 🤝 Contributing

Contributions are welcome! Feel free to:

- 🐛 Report bugs
- 💡 Suggest improvements
- 📖 Improve documentation
- 🔧 Submit pull requests

## 📄 License

This project is licensed under the [MIT License](LICENSE). See the `LICENSE` file for details.

## ⭐ Support

If this project helped you, please give it a star ⭐!

---

**⚡ Auto mode intelligently detects PDF type and applies optimal compression!**
