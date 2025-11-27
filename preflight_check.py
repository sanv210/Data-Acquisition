"""
Pre-flight Checklist for Building DAQ System .exe
Run this script to verify everything is ready before building
"""

import subprocess
import sys
import os
from pathlib import Path


def check_python_version():
    """Verify Python version is 3.8+"""
    print("\n[1/7] Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"  ✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"  ✗ Python {version.major}.{version.minor} (requires 3.8+)")
        return False


def check_venv_activated():
    """Check if virtual environment is activated"""
    print("\n[2/7] Checking virtual environment...")
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print(f"  ✓ Virtual environment activated: {sys.prefix}")
        return True
    else:
        print("  ✗ Virtual environment NOT activated!")
        print("     Run: .\\venv\\Scripts\\Activate.ps1")
        return False


def check_package_installed(package_name, import_name=None):
    """Check if a package is installed"""
    if import_name is None:
        import_name = package_name.replace('-', '_')
    
    try:
        __import__(import_name)
        return True
    except ImportError:
        return False


def check_dependencies():
    """Check if all required packages are installed"""
    print("\n[3/7] Checking required dependencies...")
    
    required = {
        'fastapi': 'fastapi',
        'uvicorn': 'uvicorn',
        'sqlalchemy': 'sqlalchemy',
        'mysql-connector-python': 'mysql',
        'pydantic': 'pydantic',
        'requests': 'requests',
        'python-dotenv': 'dotenv',
        'pyinstaller': 'PyInstaller',
    }
    
    missing = []
    for pkg_name, import_name in required.items():
        if check_package_installed(pkg_name, import_name):
            print(f"  ✓ {pkg_name}")
        else:
            print(f"  ✗ {pkg_name} (missing)")
            missing.append(pkg_name)
    
    return missing


def check_project_structure():
    """Verify project folder structure"""
    print("\n[4/7] Checking project structure...")
    
    required_dirs = [
        'backend',
        'frontend',
        'connection',
    ]
    
    required_files = [
        'launcher.py',
        'build_exe.py',
        'DAQ_System.spec',
    ]
    
    all_ok = True
    
    for dir_name in required_dirs:
        if os.path.isdir(dir_name):
            print(f"  ✓ {dir_name}/")
        else:
            print(f"  ✗ {dir_name}/ (missing)")
            all_ok = False
    
    for file_name in required_files:
        if os.path.isfile(file_name):
            print(f"  ✓ {file_name}")
        else:
            print(f"  ✗ {file_name} (missing)")
            all_ok = False
    
    return all_ok


def check_env_file():
    """Check if .env file exists and has credentials"""
    print("\n[5/7] Checking .env file...")
    
    env_file = Path('backend/.env')
    
    if not env_file.exists():
        print("  ✗ backend/.env not found")
        return False
    
    try:
        with open(env_file) as f:
            content = f.read()
            if 'MYSQL_USER' in content and 'MYSQL_PASSWORD' in content:
                print("  ✓ backend/.env found with credentials")
                return True
            else:
                print("  ⚠ backend/.env found but may be incomplete")
                return True
    except Exception as e:
        print(f"  ✗ Error reading backend/.env: {e}")
        return False


def check_disk_space():
    """Check if there's enough disk space"""
    print("\n[6/7] Checking disk space...")
    
    try:
        import shutil
        disk_usage = shutil.disk_usage('.')
        free_gb = disk_usage.free / (1024**3)
        
        if free_gb > 1:  # Need at least 1GB free
            print(f"  ✓ Sufficient disk space ({free_gb:.1f}GB free)")
            return True
        else:
            print(f"  ✗ Insufficient disk space ({free_gb:.1f}GB free, need 1GB+)")
            return False
    except Exception as e:
        print(f"  ⚠ Could not check disk space: {e}")
        return True


def check_mysql_access():
    """Check if MySQL is accessible"""
    print("\n[7/7] Checking MySQL access...")
    
    try:
        import mysql.connector
        # Don't actually try to connect, just verify the module loads
        print("  ✓ MySQL connector available")
        print("  ⚠ Note: Verify MySQL server is running before building")
        return True
    except ImportError:
        print("  ✗ MySQL connector not available")
        return False


def main():
    """Run all checks"""
    print("=" * 60)
    print("DAQ System - Pre-flight Checklist")
    print("=" * 60)
    
    checks = [
        ("Python Version", check_python_version),
        ("Virtual Environment", check_venv_activated),
        ("Project Structure", check_project_structure),
        ("Environment File", check_env_file),
        ("Disk Space", check_disk_space),
        ("MySQL Access", check_mysql_access),
    ]
    
    results = []
    
    for name, check_func in checks:
        try:
            if name == "Python Version":
                result = check_func()
            elif name == "Virtual Environment":
                result = check_func()
            elif name == "Project Structure":
                result = check_func()
            elif name == "Environment File":
                result = check_func()
            elif name == "Disk Space":
                result = check_func()
            elif name == "MySQL Access":
                result = check_func()
            else:
                result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"  ✗ Error: {e}")
            results.append((name, False))
    
    # Check dependencies separately (may need install)
    print("\n[3/7] Checking required dependencies...")
    missing = check_dependencies()
    
    # Print summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:8} - {name}")
    
    if missing:
        print(f"\nMissing packages: {', '.join(missing)}")
        print("\nInstall with:")
        print(f"  pip install {' '.join(missing)}")
    else:
        print("\n✓ All dependencies installed")
    
    # Determine if we can proceed
    all_passed = all(result for _, result in results) and not missing
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ Ready to build! Run: python build_exe.py")
    else:
        print("✗ Some checks failed. Please fix the issues above.")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
