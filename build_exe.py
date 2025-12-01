"""
Build Script for BioAnalyzer Pro
Creates Windows executable using PyInstaller
"""

import os
import subprocess
import sys
import shutil

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")


def check_pyinstaller():
    """Check if PyInstaller is installed"""
    print("🔍 Checking for PyInstaller...")
    try:
        import PyInstaller
        print("  ✓ PyInstaller is installed\n")
        return True
    except ImportError:
        print("  ✗ PyInstaller not found\n")
        return False


def install_pyinstaller():
    """Install PyInstaller"""
    print("📦 Installing PyInstaller...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("  ✓ PyInstaller installed successfully\n")
        return True
    except:
        print("  ✗ Failed to install PyInstaller\n")
        return False


def check_required_files():
    """Check if all required files exist"""
    print("📋 Checking required files...")
    
    required = {
        'main.py': 'Main application file',
        'config.py': 'Configuration file',
        'ui/styles.py': 'UI styles',
        'algorithms/fasta_parser.py': 'FASTA parser',
        'algorithms/dna_operations.py': 'DNA operations',
        'algorithms/pattern_matching.py': 'Pattern matching',
        'algorithms/index_search.py': 'Index search',
        'algorithms/suffix_array.py': 'Suffix array',
        'algorithms/assembly.py': 'Assembly algorithms',
    }
    
    missing = []
    for file, desc in required.items():
        if os.path.exists(file):
            print(f"  ✓ {desc}: {file}")
        else:
            print(f"  ✗ Missing: {file}")
            missing.append(file)
    
    print()
    return len(missing) == 0, missing


def create_spec_file():
    """Create PyInstaller spec file"""
    print("📝 Creating spec file...")
    
    spec_content = """# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('algorithms', 'algorithms'),
        ('ui', 'ui'),
        ('config.py', '.'),
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.scrolledtext',
        'tkinter.filedialog',
        'tkinter.messagebox',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='BioAnalyzerPro',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico' if os.path.exists('assets/icon.ico') else None,
)
"""
    
    try:
        with open('BioAnalyzerPro.spec', 'w') as f:
            f.write(spec_content)
        print("  ✓ Spec file created: BioAnalyzerPro.spec\n")
        return True
    except Exception as e:
        print(f"  ✗ Failed to create spec file: {e}\n")
        return False


def build_executable():
    """Build the executable"""
    print("🔨 Building executable...")
    print("This may take several minutes...\n")
    
    try:
        # Use the spec file
        result = subprocess.run(
            ['pyinstaller', '--clean', 'BioAnalyzerPro.spec'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("  ✓ Build completed successfully!\n")
            return True
        else:
            print("  ✗ Build failed\n")
            print("Error output:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"  ✗ Build failed: {e}\n")
        return False


def copy_assets():
    """Copy assets folder to dist"""
    print("📁 Copying assets...")
    
    if os.path.exists('assets'):
        try:
            dist_assets = os.path.join('dist', 'assets')
            if os.path.exists(dist_assets):
                shutil.rmtree(dist_assets)
            shutil.copytree('assets', dist_assets)
            print("  ✓ Assets copied to dist/\n")
            return True
        except Exception as e:
            print(f"  ⚠️  Failed to copy assets: {e}\n")
            return False
    else:
        print("  ⚠️  No assets folder found\n")
        return True


def create_readme():
    """Create README for distribution"""
    print("📝 Creating README...")
    
    readme = """# BioAnalyzer Pro

## Installation

Simply run BioAnalyzerPro.exe

No installation or Python required!

## System Requirements

- Windows 7 or later
- 4GB RAM minimum
- 100MB free disk space

## Features

1. FASTA Parser - Parse and analyze FASTA sequences
2. DNA Analysis - Calculate GC/AT content, complement, translation
3. Naive Search - Simple pattern matching
4. Boyer-Moore - Efficient pattern matching algorithm
5. Index Search - K-mer based search
6. Suffix Array - Advanced suffix array construction
7. Sequence Assembly - Greedy assembly with overlap detection

## Usage

1. Launch BioAnalyzerPro.exe
2. Select a tab for the analysis you want
3. Load example or paste your data
4. Click the analysis button
5. View and save results

## Support

For issues or questions, please contact the developer.

## Version

v1.0 - Initial Release

Built with Python and Tkinter
"""
    
    try:
        with open('dist/README.txt', 'w') as f:
            f.write(readme)
        print("  ✓ README created in dist/\n")
        return True
    except Exception as e:
        print(f"  ⚠️  Failed to create README: {e}\n")
        return False


def main():
    """Main build process"""
    print_header("🧬 BioAnalyzer Pro - Build Script")
    
    # Step 1: Check PyInstaller
    if not check_pyinstaller():
        if not install_pyinstaller():
            print("❌ Cannot proceed without PyInstaller")
            return False
    
    # Step 2: Check required files
    files_ok, missing = check_required_files()
    if not files_ok:
        print("❌ Missing required files:")
        for file in missing:
            print(f"   - {file}")
        print("\nPlease ensure all files are in place before building.")
        return False
    
    # Step 3: Create spec file
    if not create_spec_file():
        print("❌ Failed to create spec file")
        return False
    
    # Step 4: Build executable
    if not build_executable():
        print("❌ Build failed")
        return False
    
    # Step 5: Copy assets
    copy_assets()
    
    # Step 6: Create README
    create_readme()
    
    # Success!
    print_header("✅ Build Complete!")
    
    print("📦 Your executable is ready!\n")
    print("Location: dist/BioAnalyzerPro.exe\n")
    print("📁 Distribution folder contents:")
    print("   - BioAnalyzerPro.exe  (Main application)")
    print("   - assets/             (Icons and images)")
    print("   - README.txt          (User guide)\n")
    
    print("🚀 You can now:")
    print("   1. Run dist/BioAnalyzerPro.exe to test")
    print("   2. Zip the dist/ folder for distribution")
    print("   3. Share with others - no Python needed!\n")
    
    # Show file size
    exe_path = 'dist/BioAnalyzerPro.exe'
    if os.path.exists(exe_path):
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        print(f"📊 Executable size: {size_mb:.1f} MB\n")
    
    return True


if __name__ == "__main__":
    try:
        success = main()
        if success:
            input("\n✅ Press Enter to exit...")
        else:
            input("\n❌ Press Enter to exit...")
    except KeyboardInterrupt:
        print("\n\n⚠️  Build cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        input("\nPress Enter to exit...")
