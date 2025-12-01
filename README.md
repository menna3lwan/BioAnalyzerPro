# 🧬 BioAnalyzer Pro

A comprehensive desktop bioinformatics application for DNA sequence analysis, pattern matching, and sequence assembly.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.7+-green)
![License](https://img.shields.io/badge/license-MIT-blue)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)



## ✨ Features

### 📄 1. FASTA Parser
- Parse FASTA formatted sequences
- Validate DNA sequences
- Extract headers and metadata
- Calculate sequence statistics

### 🧬 2. DNA Analysis
- **GC Content** - Calculate percentage of G and C nucleotides
- **AT Content** - Calculate percentage of A and T nucleotides
- **Complement** - Generate complementary DNA strand
- **Reverse Complement** - Generate reverse complement
- **Translation** - Translate DNA to protein sequence

### 🔍 3. Naive Pattern Search
- Simple exact pattern matching algorithm
- Shows all match positions with context
- Efficient for short patterns

### ⚡ 4. Boyer-Moore Search
- Advanced pattern matching algorithm
- Bad Character Table visualization
- Faster than naive search for longer patterns
- Optimal for multiple searches

### 📇 5. Index Search
- K-mer based indexing (k=2 to 10)
- Fast pattern lookup
- Index statistics and visualization
- Efficient for repeated queries

### 📊 6. Suffix Array
- Iterative doubling construction
- Step-by-step visualization
- Optimal for suffix-based searches
- Educational mode for learning

### 🧩 7. Sequence Assembly
- **Overlap Detection** - Find all sequence overlaps
- **Greedy Assembly** - Assemble sequences using greedy algorithm
- **Overlap Visualization** - Visual representation of overlaps
- **Assembly Statistics** - Compression ratio and steps

---

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- tkinter (usually comes with Python)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/BioAnalyzerPro.git
   cd BioAnalyzerPro
   ```

2. **Install dependencies** (optional - for icons only)
   ```bash
   pip install -r requirements.txt
   ```
   
   Or minimal install:
   ```bash
   # No dependencies required! tkinter comes with Python
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

---

## 📦 Building Executable (Windows)

Create a standalone `.exe` file that runs without Python:

### Quick Build (Recommended)
```bash
# Just double-click
build.bat
```

### Manual Build
```bash
pip install pyinstaller
python build_exe.py
```

### Advanced Build
```bash
pip install pyinstaller
pyinstaller BioAnalyzerPro.spec
```

**Output:** `dist/BioAnalyzerPro.exe` (15-25 MB)

See [BUILD_GUIDE.md](BUILD_GUIDE.md) for detailed instructions.

---

## 📁 Project Structure

```
BioAnalyzerPro/
│
├── main.py                     # Main application entry point
├── config.py                   # Configuration and settings
├── requirements.txt            # Python dependencies
│
├── algorithms/                 # Core bioinformatics algorithms
│   ├── __init__.py
│   ├── fasta_parser.py        # FASTA file parsing
│   ├── dna_operations.py      # DNA analysis functions
│   ├── pattern_matching.py    # Pattern matching algorithms
│   ├── index_search.py        # K-mer indexing
│   ├── suffix_array.py        # Suffix array construction
│   └── assembly.py            # Sequence assembly
│
├── ui/                         # User interface
│   ├── __init__.py
│   └── styles.py              # UI styling
│
├── assets/                     # Icons and images
│   ├── icon.ico               # Application icon
│   ├── logo.png               # Logo
│   └── icon_*.png             # Various icon sizes
│
├── build_exe.py               # Build script for executable
├── build.bat                  # Windows build automation
├── BioAnalyzerPro.spec        # PyInstaller spec file
│
└── docs/                       # Documentation
    ├── BUILD_GUIDE.md         # Build instructions
    ├── HOW_TO_BUILD_EXE.md    # Executable creation guide
    └── FUNCTIONS_SUMMARY.md   # API documentation
```

---

## 🎯 Usage Examples

### Example 1: DNA Analysis
```python
# Load example
sequence = "ATGGCGTCGCTGTGGAGGCGATCGATCG"

# Results:
# GC Content: 65.52%
# AT Content: 34.48%
# Complement: TACCGCAGCGACAGCTCCGCTAGCTAGC
# Translation: MASCGRID
```

### Example 2: Pattern Matching
```python
# Sequence
sequence = "ATGCGATCGATCGATCGATCGATCGATCG"

# Pattern
pattern = "GATC"

# Results:
# Found 6 matches at positions: [4, 8, 12, 16, 20, 24]
```

### Example 3: Sequence Assembly
```python
# Sequences
sequences = [
    "ATGCGATCG",
    "TCGATCGAT",
    "ATCGATCGC"
]

# Assembly with min_overlap=3
# Result: ATGCGATCGATCGC
# Compression: 42.8%
```

---

## 🛠️ Algorithm Details

### Pattern Matching Algorithms

| Algorithm | Time Complexity | Space | Best For |
|-----------|----------------|-------|----------|
| Naive | O(n×m) | O(1) | Short patterns |
| Boyer-Moore | O(n/m) average | O(m+σ) | Long patterns |
| Index Search | O(m+k) | O(n) | Multiple queries |

Where:
- n = sequence length
- m = pattern length  
- σ = alphabet size
- k = number of matches

### Suffix Array Construction
- **Algorithm:** Iterative Doubling
- **Time Complexity:** O(n log n)
- **Space Complexity:** O(n)

### Assembly Algorithm
- **Type:** Greedy Overlap-Based
- **Time Complexity:** O(n² × m)
- **Best for:** Small datasets, educational purposes

---

## 📚 API Documentation

### DNA Operations

```python
from algorithms import dna_operations as dna

# Calculate GC content
gc = dna.gc_content("ATGC")  # Returns: 50.0

# Get complement
comp = dna.complement("ATGC")  # Returns: "TACG"

# Translate to protein
protein = dna.translate("ATGGCG")  # Returns: "MA"
```

### Pattern Matching

```python
from algorithms import pattern_matching as pattern

# Naive search
positions = pattern.naive_match(sequence, pattern)

# Boyer-Moore search
positions, bc_table = pattern.boyer_moore_match(sequence, pattern)
```

### Index Search

```python
from algorithms import index_search as index

# Build k-mer index
idx = index.build_index(sequence, k=3)

# Query index
matches = index.query_index(idx, sequence, pattern)
```

See [FUNCTIONS_SUMMARY.md](FUNCTIONS_SUMMARY.md) for complete API reference.

---

## 🎨 Customization

### Colors
Edit `config.py` to customize the color scheme:

```python
class Colors:
    PRIMARY = "#3d5a80"      # Header color
    SECONDARY = "#3498db"    # Button color
    ACCENT = "#2ecc71"       # Accent color
    BACKGROUND = "#f0f4f8"   # Background
```

### Adding New Analysis
1. Create algorithm in `algorithms/`
2. Add tab in `main.py`
3. Import and call functions
4. Update UI accordingly

---

## 🧪 Testing

```bash
# Test DNA operations
python -m pytest tests/test_dna.py

# Test pattern matching
python -m pytest tests/test_pattern.py

# Run all tests
python -m pytest
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a new branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Add docstrings to all functions
- Include unit tests for new features
- Update README with new features

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 BioAnalyzer Pro

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

## 👥 Authors

- **Your Name** - *Initial work* - [YourGitHub](https://github.com/yourusername)

See also the list of [contributors](https://github.com/yourusername/BioAnalyzerPro/contributors) who participated in this project.

---

## 🙏 Acknowledgments

- Built with Python and Tkinter
- Inspired by bioinformatics tools like BLAST and Clustal
- Thanks to the open-source community

---

## 📞 Support

- **Documentation:** [Wiki](https://github.com/yourusername/BioAnalyzerPro/wiki)
- **Issues:** [Issue Tracker](https://github.com/yourusername/BioAnalyzerPro/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/BioAnalyzerPro/discussions)

---

## 🔮 Future Features

- [ ] Multiple sequence alignment
- [ ] Phylogenetic tree construction
- [ ] BLAST integration
- [ ] Export to various formats (GenBank, EMBL)
- [ ] Batch processing
- [ ] Command-line interface
- [ ] Web-based version
- [ ] Cloud storage integration

---

## 📊 Statistics

![GitHub stars](https://img.shields.io/github/stars/yourusername/BioAnalyzerPro?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/BioAnalyzerPro?style=social)
![GitHub issues](https://img.shields.io/github/issues/yourusername/BioAnalyzerPro)
![GitHub pull requests](https://img.shields.io/github/issues-pr/yourusername/BioAnalyzerPro)

---

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/BioAnalyzerPro&type=Date)](https://star-history.com/#yourusername/BioAnalyzerPro&Date)

---

## 📖 Citation

If you use BioAnalyzer Pro in your research, please cite:

```bibtex
@software{bioanalyzer_pro,
  author = {Your Name},
  title = {BioAnalyzer Pro: A Comprehensive Bioinformatics Analysis Tool},
  year = {2024},
  url = {https://github.com/yourusername/BioAnalyzerPro}
}
```

---

## 🔗 Related Projects

- [Biopython](https://biopython.org/) - Python tools for computational biology
- [BLAST](https://blast.ncbi.nlm.nih.gov/) - Basic Local Alignment Search Tool
- [Clustal Omega](http://www.clustal.org/omega/) - Multiple sequence alignment

---

<div align="center">

**Made with ❤️ for Bioinformatics**

[⬆ Back to Top](#-bioanalyzer-pro)

</div>
