"""
Build script to create DAQ_System.exe using PyInstaller
Run this script from the project root directory
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path

def build_exe():
    """Build the .exe using PyInstaller"""
    
    # Ensure we're in the correct directory
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    print("=" * 60)
    print("DAQ System - Building .exe")
    print("=" * 60)
    print(f"Project root: {project_root}")
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print(f"✓ PyInstaller found: {PyInstaller.__file__}")
    except ImportError:
        print("✗ PyInstaller not found!")
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Clean previous builds
    print("\nCleaning previous builds...")
    if os.path.exists('build'):
        print("  Removing 'build' directory...")
        shutil.rmtree('build', ignore_errors=True)
    if os.path.exists('dist'):
        print("  Removing 'dist' directory...")
        shutil.rmtree('dist', ignore_errors=True)
    
    # Build the exe
    print("\nBuilding DAQ_System.exe...")
    print("-" * 60)
    
    cmd = [
        sys.executable,
        '-m', 'PyInstaller',
        'DAQ_System.spec',
        '--workpath', 'build',
        '--distpath', 'dist',
        '--noconfirm'
    ]
    
    try:
        result = subprocess.run(cmd, check=True)
        print("-" * 60)
        print("\n✓ Build completed successfully!")
        print(f"\nThe executable is located at: {project_root / 'dist' / 'DAQ_System' / 'DAQ_System.exe'}")
        print("\nTo run the application:")
        print(f"  {project_root / 'dist' / 'DAQ_System' / 'DAQ_System.exe'}")
        print("\nOr create a shortcut to the executable for easy access.")
        return True
        
    except subprocess.CalledProcessError as e:
        print("-" * 60)
        print(f"\n✗ Build failed with error code: {e.returncode}")
        return False
    except Exception as e:
        print(f"\n✗ Build failed: {e}")
        return False


def verify_dependencies():
    """Verify all required dependencies are installed"""
    print("\nVerifying dependencies...")
    
    required_packages = [
        'fastapi',
        'uvicorn',
        'sqlalchemy',
        'mysql-connector-python',
        'pydantic',
        'requests',
        'python-dotenv',
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} (missing)")
            missing.append(package)
    
    if missing:
        print(f"\nInstalling missing packages: {', '.join(missing)}")
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)
        print("All dependencies installed!")
    else:
        print("\n✓ All dependencies are installed!")
    
    return True


if __name__ == "__main__":
    print("DAQ System - .exe Builder")
    print("=" * 60)
    
    # Verify dependencies
    if not verify_dependencies():
        print("Dependency check failed. Please install required packages.")
        sys.exit(1)
    
    # Build the exe
    success = build_exe()
    
    sys.exit(0 if success else 1)
