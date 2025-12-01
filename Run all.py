"""
Run All - BioAnalyzer Pro
Quick start script that sets up and runs everything
"""

import os
import sys
import subprocess

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")


def check_dependencies():
    """Check if required packages are installed"""
    print_header("🔍 Checking Dependencies")
    
    required = ['PIL', 'pandas', 'numpy', 'tkinter']
    missing = []
    
    for package in required:
        try:
            if package == 'PIL':
                __import__('PIL')
            else:
                __import__(package)
            print(f"  ✓ {package} installed")
        except ImportError:
            print(f"  ✗ {package} missing")
            missing.append(package)
    
    if missing:
        print("\n⚠️  Missing packages detected!")
        print("Installing required packages...\n")
        
        install_map = {
            'PIL': 'pillow',
            'pandas': 'pandas',
            'numpy': 'numpy',
            'tkinter': 'tk'  # Usually comes with Python
        }
        
        for package in missing:
            if package == 'tkinter':
                print("⚠️  tkinter is usually included with Python.")
                print("   If missing, please install python3-tk (Linux) or reinstall Python (Windows)")
                continue
            
            package_name = install_map.get(package, package)
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
                print(f"  ✓ Installed {package_name}")
            except:
                print(f"  ✗ Failed to install {package_name}")
                return False
    
    return True


def create_icons():
    """Generate application icons"""
    print_header("🎨 Creating Icons")
    
    if not os.path.exists('create_icon.py'):
        print("  ⚠️  create_icon.py not found!")
        return False
    
    try:
        subprocess.check_call([sys.executable, "create_icon.py"])
        print("  ✓ Icons created successfully")
        return True
    except:
        print("  ✗ Failed to create icons")
        return False


def run_setup():
    """Run setup script"""
    print_header("📦 Running Setup")
    
    if not os.path.exists('setup.py'):
        print("  ⚠️  setup.py not found!")
        return False
    
    try:
        subprocess.check_call([sys.executable, "setup.py"])
        print("  ✓ Setup completed")
        return True
    except:
        print("  ✗ Setup failed")
        return False


def run_application():
    """Run the main application"""
    print_header("🚀 Launching BioAnalyzer Pro")
    
    if not os.path.exists('main.py'):
        print("  ⚠️  main.py not found!")
        return False
    
    try:
        print("  Starting application...\n")
        subprocess.check_call([sys.executable, "main.py"])
        return True
    except KeyboardInterrupt:
        print("\n\n  Application closed by user")
        return True
    except:
        print("  ✗ Application failed to start")
        return False


def main():
    """Main execution"""
    print("\n" + "=" * 60)
    print("  🧬 BioAnalyzer Pro - Quick Start")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Dependency check failed. Please install manually:")
        print("   pip install pillow pandas numpy")
        return
    
    # Create icons
    create_icons()
    
    # Run setup
    run_setup()
    
    # Run application
    success = run_application()
    
    if success:
        print_header("✅ All Done!")
        print("Thank you for using BioAnalyzer Pro! 🧬✨\n")
    else:
        print_header("❌ Setup Failed")
        print("Please check the error messages above.\n")
        print("For help, see INSTALLATION_GUIDE.md\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)