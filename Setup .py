"""
Setup Script for BioAnalyzer Pro
Creates folder structure and moves icons to assets folder
"""

import os
import shutil

def create_folder_structure():
    """Create project folder structure"""
    print("📁 Creating folder structure...")
    
    folders = [
        'assets',
        'algorithms',
        'ui',
        'utils'
    ]
    
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"  ✓ Created {folder}/")
        else:
            print(f"  ✓ {folder}/ exists")


def move_icons_to_assets():
    """Move icon files to assets folder"""
    print("\n🎨 Moving icons to assets folder...")
    
    icon_files = [
        'icon.ico',
        'icon_16x16.png',
        'icon_32x32.png',
        'icon_48x48.png',
        'icon_64x64.png',
        'icon_128x128.png',
        'icon_256x256.png',
        'icon_512x512.png',
        'logo.png'
    ]
    
    for icon_file in icon_files:
        if os.path.exists(icon_file):
            dest = os.path.join('assets', icon_file)
            shutil.copy2(icon_file, dest)
            print(f"  ✓ Copied {icon_file} → assets/")
        else:
            print(f"  ⚠ {icon_file} not found")


def create_algorithm_init_files():
    """Create __init__.py files for algorithm modules"""
    print("\n📦 Creating __init__.py files...")
    
    # algorithms/__init__.py
    algorithms_init = '''"""
Algorithms Package
All bioinformatics algorithms
"""

from .fasta_parser import *
from .dna_operations import *
from .pattern_matching import *
from .index_search import *
from .suffix_array import *
from .assembly import *
'''
    
    with open('algorithms/__init__.py', 'w') as f:
        f.write(algorithms_init)
    print("  ✓ Created algorithms/__init__.py")
    
    # ui/__init__.py
    ui_init = '''"""
UI Package
All UI related modules
"""

from .styles import *
'''
    
    with open('ui/__init__.py', 'w') as f:
        f.write(ui_init)
    print("  ✓ Created ui/__init__.py")


def create_readme():
    """Create main README.md"""
    print("\n📄 Creating README.md...")
    
    readme = '''# 🧬 BioAnalyzer Pro

A comprehensive bioinformatics desktop application for DNA sequence analysis.

## 🚀 Features

### 1. 📄 FASTA Parser
- Parse FASTA formatted sequences
- Validate sequences
- Extract headers and metadata

### 2. 🧬 DNA Analysis
- Calculate GC content
- Calculate AT content
- Generate complement sequences
- Generate reverse complement
- DNA to protein translation

### 3. 🔍 Pattern Matching
- **Naive Search** - Simple pattern matching
- **Boyer-Moore** - Optimized pattern matching with bad character table
- **Index Search** - K-mer index based search
- **Suffix Array** - Advanced suffix array construction

### 4. 🧩 Sequence Assembly
- Find overlaps between sequences
- Greedy assembly algorithm
- Overlap visualization
- Assembly statistics

---

## 📋 Requirements

```txt
tkinter (usually comes with Python)
pillow>=10.0.0
pandas>=2.0.0
numpy>=1.24.0
```

---

## 🎯 Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/BioAnalyzerPro.git
cd BioAnalyzerPro
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run setup (optional):**
```bash
python setup.py
```

4. **Run the application:**
```bash
python main.py
```

---

## 📁 Project Structure

```
BioAnalyzerPro/
├── assets/                 # Icons and images
│   ├── icon.ico
│   ├── logo.png
│   └── icon_*.png
├── algorithms/             # Core algorithms
│   ├── __init__.py
│   ├── fasta_parser.py
│   ├── dna_operations.py
│   ├── pattern_matching.py
│   ├── index_search.py
│   ├── suffix_array.py
│   └── assembly.py
├── ui/                     # UI components
│   ├── __init__.py
│   └── styles.py
├── utils/                  # Utility functions
│   └── config.py
├── main.py                 # Main application
├── config.py               # Configuration
└── requirements.txt        # Dependencies
```

---

## 🎨 Screenshots

[Add screenshots here]

---

## 📖 Usage Guide

### FASTA Parser
1. Paste or upload FASTA formatted sequences
2. Configure parsing options
3. Click "Parse FASTA" to analyze

### DNA Analysis
1. Enter DNA sequence
2. Select analysis options
3. View GC/AT content, complement, and translation

### Pattern Search
1. Enter sequence and pattern
2. Choose search algorithm
3. View all matches with positions

### Sequence Assembly
1. Enter multiple sequences (one per line)
2. Set minimum overlap length
3. Find overlaps or run greedy assembly

---

## 🛠️ Development

### Adding New Features

1. Create algorithm file in `algorithms/`
2. Import in `algorithms/__init__.py`
3. Add tab in `main.py`
4. Update `config.py` if needed

---

## 📝 License

[Add your license here]

---

## 👥 Contributors

[Add contributors here]

---

## 🐛 Bug Reports

Found a bug? Please open an issue on GitHub.

---

## ⭐ Acknowledgments

Built with Python and Tkinter
Icons created with PIL

---

**Made with ❤️ for Bioinformatics**
'''
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme)
    print("  ✓ Created README.md")


def create_requirements():
    """Create requirements.txt"""
    print("\n📦 Creating requirements.txt...")
    
    requirements = '''# BioAnalyzer Pro Requirements

# GUI
pillow>=10.0.0

# Data Processing
pandas>=2.0.0
numpy>=1.24.0

# Optional: For better performance
# scipy>=1.10.0
'''
    
    with open('requirements.txt', 'w') as f:
        f.write(requirements)
    print("  ✓ Created requirements.txt")


def create_gitignore():
    """Create .gitignore"""
    print("\n🔒 Creating .gitignore...")
    
    gitignore = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Project specific
*.log
temp/
test_data/
'''
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore)
    print("  ✓ Created .gitignore")


def main():
    """Run setup"""
    print("=" * 60)
    print("🧬 BioAnalyzer Pro - Setup Script")
    print("=" * 60)
    
    create_folder_structure()
    move_icons_to_assets()
    create_algorithm_init_files()
    create_readme()
    create_requirements()
    create_gitignore()
    
    print("\n" + "=" * 60)
    print("✅ Setup completed successfully!")
    print("=" * 60)
    print("\n📋 Next steps:")
    print("  1. Install requirements: pip install -r requirements.txt")
    print("  2. Place your algorithm files in algorithms/")
    print("  3. Place your UI files in ui/")
    print("  4. Run the app: python main.py")
    print("\n🎉 Happy coding!")


if __name__ == "__main__":
    main()