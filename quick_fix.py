"""
Quick Fix Script - BioAnalyzer Pro
Fixes common issues and installs missing dependencies
"""

import subprocess
import sys
import os

def print_banner():
    print("\n" + "=" * 60)
    print("  🧬 BioAnalyzer Pro - Quick Fix")
    print("=" * 60 + "\n")


def install_pillow():
    """Install Pillow (PIL)"""
    print("📦 Installing Pillow (PIL)...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])
        print("  ✓ Pillow installed successfully\n")
        return True
    except Exception as e:
        print(f"  ✗ Failed to install Pillow: {e}\n")
        return False


def install_all_dependencies():
    """Install all required packages"""
    print("📦 Installing all dependencies...")
    packages = ["pillow", "pandas", "numpy"]
    
    for package in packages:
        print(f"  Installing {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"  ✓ {package} installed\n")
        except:
            print(f"  ✗ Failed to install {package}\n")
    
    print("✅ All dependencies installed!\n")


def check_syntax():
    """Check if main.py has syntax errors"""
    print("🔍 Checking main.py for syntax errors...")
    
    if not os.path.exists('main.py'):
        print("  ⚠️  main.py not found!")
        return False
    
    try:
        with open('main.py', 'r', encoding='utf-8') as f:
            code = f.read()
            compile(code, 'main.py', 'exec')
        print("  ✓ No syntax errors found\n")
        return True
    except SyntaxError as e:
        print(f"  ✗ Syntax error found: {e}\n")
        print("  Line:", e.lineno)
        print("  Text:", e.text)
        return False


def main():
    """Main execution"""
    print_banner()
    
    # Install dependencies
    install_all_dependencies()
    
    # Check syntax
    if not check_syntax():
        print("\n⚠️  Please fix syntax errors in main.py")
        print("   You can use main_fixed.py instead:\n")
        print("   1. Delete or rename main.py")
        print("   2. Rename main_fixed.py to main.py")
        print("   3. Run again\n")
        return
    
    # All good!
    print("=" * 60)
    print("✅ All checks passed!")
    print("=" * 60)
    print("\n🚀 You can now run:")
    print("   python main.py\n")


if __name__ == "__main__":
    try:
        main()
        input("\nPress Enter to exit...")
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        input("\nPress Enter to exit...")
