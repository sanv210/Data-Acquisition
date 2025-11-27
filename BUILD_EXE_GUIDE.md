# DAQ System - Building .exe Package

This guide explains how to build the complete DAQ System (frontend, backend, connection folder) into a single `.exe` executable.

## What Gets Packaged

The `.exe` includes:
- **Frontend** - Tkinter GUI application (`frontend/app.py`)
- **Backend** - FastAPI server with MySQL database (`backend/main.py`)
- **Connection** - Data integration scripts (`connection/`)
- **All dependencies** - Python packages and libraries

## Prerequisites

1. **Python 3.8+** installed and accessible from command line
2. **Virtual environment activated** with all dependencies installed
3. **PyInstaller** installed

## Quick Start - Build the .exe

### Step 1: Activate Virtual Environment
```powershell
# Navigate to project root
cd C:\Users\jhaad\Downloads\Data-Acquisition

# Activate venv
.\venv\Scripts\Activate.ps1
```

### Step 2: Install PyInstaller (if not already installed)
```powershell
pip install pyinstaller
```

### Step 3: Run the Build Script
```powershell
# From project root (C:\Users\jhaad\Downloads\Data-Acquisition)
python build_exe.py
```

The script will:
1. ✓ Verify all dependencies are installed
2. ✓ Clean previous builds
3. ✓ Compile the application using PyInstaller
4. ✓ Create the `.exe` file

### Step 4: Find Your .exe

After successful build, the executable will be at:
```
C:\Users\jhaad\Downloads\Data-Acquisition\dist\DAQ_System\DAQ_System.exe
```

## Running the .exe

### Option 1: Direct Execution
```powershell
C:\Users\jhaad\Downloads\Data-Acquisition\dist\DAQ_System\DAQ_System.exe
```

### Option 2: Create Desktop Shortcut
1. Navigate to `dist\DAQ_System\`
2. Right-click `DAQ_System.exe`
3. Select "Send to" → "Desktop (create shortcut)"
4. Double-click the shortcut to run

### Option 3: Add to Start Menu
1. Copy `DAQ_System.exe` to a permanent location
2. Create a shortcut in Windows Start Menu folder

## What Happens When You Run the .exe

1. **Backend Server Starts**
   - FastAPI server launches on `http://127.0.0.1:8000`
   - Attempts to connect to MySQL database
   - Creates necessary tables if needed

2. **Frontend Launches**
   - Tkinter GUI application opens
   - Displays analytical group selection interface
   - Connects to backend API automatically

3. **Logging**
   - Application logs saved to `daq_system.log` in same directory as `.exe`

## Troubleshooting

### "Python not found" error
- Ensure Python is in your system PATH
- Or specify full Python path in build script

### "Module not found" error
- Some modules may not be automatically detected
- Edit `DAQ_System.spec` and add to `hiddenimports`:
  ```python
  hiddenimports=[
      'your_missing_module',
      # ... add others
  ]
  ```

### Backend fails to start
- Ensure MySQL server is running
- Check `.env` file credentials are correct
- Review `daq_system.log` for details

### Large .exe file size
- This is normal (typically 50-150 MB with all dependencies)
- Use UPX to compress further if needed

## Advanced Options

### Hide Console Window (Production)
Edit `DAQ_System.spec`, change:
```python
console=True,  # Change to False to hide console
```

### Add Custom Icon
Place an `.ico` file at `frontend/assets/icon.ico`
The spec file will automatically detect and use it

### Single File Executable
To create a single `.exe` file instead of a folder with dependencies:
```python
exe = EXE(
    # ... other parameters
    onefile=True,  # Add this line
)
```

## Distribution

To share the application:

1. **Method 1: Just the .exe folder**
   - Copy entire `dist\DAQ_System` folder
   - Users double-click `.exe` to run

2. **Method 2: Create installer**
   - Use NSIS or Inno Setup to create an installer
   - Allows users to install to Program Files, etc.

3. **Method 3: Standalone package**
   - Zip the entire `dist\DAQ_System` folder
   - Users extract and run `.exe`

## File Structure in Build

```
dist/
└── DAQ_System/
    ├── DAQ_System.exe          # Main executable
    ├── daq_system.log          # Created on first run
    ├── backend/                # Backend files
    │   ├── main.py
    │   ├── database.py
    │   ├── models.py
    │   ├── schemas.py
    │   ├── .env
    │   └── ...
    ├── frontend/               # Frontend files
    │   ├── app.py
    │   ├── pages/
    │   ├── utils/
    │   └── ...
    ├── connection/             # Connection folder
    │   ├── integration.py
    │   ├── populate_test_data.py
    │   └── ...
    └── ... (other dependencies)
```

## Notes

- The `.exe` is created with console window enabled (visible logs)
- Logs are saved to `daq_system.log` in the `.exe` directory
- Backend server runs on `127.0.0.1:8000` (localhost)
- All dependencies are bundled (no need to install separately)

## Support

If you encounter issues:
1. Check `daq_system.log` for error messages
2. Ensure MySQL is running and accessible
3. Verify `.env` file has correct database credentials
4. Run `build_exe.py` again to rebuild

---

**Created:** 2025-11-27
**Version:** 1.0
