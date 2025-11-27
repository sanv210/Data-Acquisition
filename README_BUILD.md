# DAQ System .exe Build - Complete Setup

Everything needed to build a single `.exe` file containing the entire DAQ system (frontend + backend + connection folder) is now ready!

## Files Created

### Build Scripts
- **`launcher.py`** - Main entry point that starts backend and frontend together
- **`build_exe.py`** - Python script to build the .exe using PyInstaller
- **`build.bat`** - Windows batch file for quick building
- **`preflight_check.py`** - Pre-flight checklist to verify everything is ready

### Configuration
- **`DAQ_System.spec`** - PyInstaller configuration (defines what to include in .exe)
- **`build_requirements.txt`** - Build dependencies list

### Documentation
- **`BUILD_EXE_GUIDE.md`** - Comprehensive build guide
- **`EXE_BUILD_QUICK_REFERENCE.md`** - Quick reference for building
- **`README_BUILD.md`** - This file

## Quick Start - Build in 3 Steps

### 1️⃣ Activate Virtual Environment
```powershell
cd C:\Users\jhaad\Downloads\Data-Acquisition
.\venv\Scripts\Activate.ps1
```

### 2️⃣ Run Pre-flight Check (Optional but Recommended)
```powershell
python preflight_check.py
```

### 3️⃣ Build the .exe
```powershell
# Option A: Python script
python build_exe.py

# Option B: Batch file (Windows)
.\build.bat
```

## What Gets Built

The `.exe` will contain:
```
DAQ_System.exe (executable)
├── Frontend (Tkinter GUI)
│   ├── Main analytical group selection
│   ├── Analytical condition forms
│   ├── Element information pages
│   ├── Channel information pages
│   └── Attenuator information pages
│
├── Backend (FastAPI REST API)
│   ├── /api/analytical-conditions/bulk
│   ├── /api/analytical-conditions/{id}
│   ├── /api/element-information/bulk
│   ├── /api/element-information/{id}
│   ├── /api/channel-information/bulk
│   ├── /api/channel-information/{id}
│   ├── /api/attenuator-information/bulk
│   ├── /api/attenuator-information/{id}
│   └── MySQL database connection
│
├── Connection Scripts
│   ├── integration.py (fetch endpoints)
│   ├── populate_test_data.py (populate database)
│   └── Other connection utilities
│
└── All Dependencies (bundled)
    ├── FastAPI, Uvicorn, SQLAlchemy
    ├── MySQL Connector, Pydantic
    ├── Requests, python-dotenv
    └── Tkinter (Python standard library)
```

## Where the .exe Will Be

After successful build:
```
C:\Users\jhaad\Downloads\Data-Acquisition\dist\DAQ_System\DAQ_System.exe
```

## Running the .exe

### Double-Click Method
1. Navigate to `dist\DAQ_System\`
2. Double-click `DAQ_System.exe`
3. Backend starts automatically on port 8000
4. Frontend GUI opens

### Command Line Method
```powershell
.\dist\DAQ_System\DAQ_System.exe
```

### Create Shortcut
Right-click `DAQ_System.exe` → "Send to" → "Desktop (create shortcut)"

## System Requirements for Running

Users who run the .exe need:
- Windows 7 or later (or macOS/Linux if built there)
- MySQL server running
- ~200MB free disk space
- No Python installation needed (bundled in .exe)

## File Structure After Build

```
Data-Acquisition/
├── launcher.py
├── build_exe.py
├── build.bat
├── DAQ_System.spec
├── preflight_check.py
├── build_requirements.txt
├── BUILD_EXE_GUIDE.md
├── EXE_BUILD_QUICK_REFERENCE.md
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── .env
│   └── ...
├── frontend/
│   ├── app.py
│   ├── pages/
│   ├── utils/
│   └── ...
├── connection/
│   ├── integration.py
│   ├── populate_test_data.py
│   └── ...
├── venv/
│   └── ... (virtual environment)
└── dist/
    └── DAQ_System/
        ├── DAQ_System.exe  ← Your executable!
        ├── daq_system.log  (created on first run)
        ├── backend/
        ├── frontend/
        ├── connection/
        └── ... (all dependencies)
```

## Before Building - Checklist

- [ ] Virtual environment is activated
- [ ] MySQL is installed and accessible
- [ ] `.env` file has correct MySQL credentials:
  ```
  MYSQL_USER=root
  MYSQL_PASSWORD=your_password
  MYSQL_HOST=localhost
  MYSQL_PORT=3306
  ```
- [ ] All dependencies are installed (`pip install -r requirements.txt`)
- [ ] PyInstaller is installed (`pip install pyinstaller`)
- [ ] Sufficient disk space (at least 1GB free)

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| "venv not activated" | Run: `.\venv\Scripts\Activate.ps1` |
| "PyInstaller not found" | Run: `pip install pyinstaller` |
| "Module not found" error | Run: `python preflight_check.py` |
| Large file size (100+MB) | Normal - includes all Python dependencies |
| Backend won't start | Verify MySQL is running and credentials in `.env` are correct |
| Frontend won't display | Check if tkinter is available in Python installation |

## Next Steps

1. **Verify everything is ready:**
   ```powershell
   python preflight_check.py
   ```

2. **Build the .exe:**
   ```powershell
   python build_exe.py
   ```

3. **Test the .exe:**
   ```powershell
   .\dist\DAQ_System\DAQ_System.exe
   ```

4. **Create shortcut for easy access**

5. **Share the `dist\DAQ_System` folder with others**

## Distribution

To share the application with others:

**Option 1: Direct folder share**
- Copy `dist\DAQ_System` folder
- Share via USB, cloud drive, or email
- Recipients extract and run `.exe`

**Option 2: Create installer (advanced)**
- Use NSIS or Inno Setup
- Creates professional Windows installer
- Users install to Program Files

**Option 3: Zip archive**
```powershell
Compress-Archive -Path .\dist\DAQ_System -DestinationPath DAQ_System.zip
```
- Share the `.zip` file
- Users extract and run `.exe`

## Customization Before Building

### Change Application Icon
1. Add `.ico` file to `frontend/assets/icon.ico`
2. Rebuild - spec file automatically detects it

### Hide Console Window (Silent Mode)
Edit `DAQ_System.spec`:
```python
console=True,  # Change to False
```

### Single File .exe (No Folder)
Edit `DAQ_System.spec`:
```python
exe = EXE(
    # ... existing code ...
    onefile=True,  # Add this
)
```

### Add Startup Arguments
Edit `launcher.py` to add command-line arguments support

## Logging & Debugging

When the `.exe` runs, logs are saved to:
```
<.exe directory>/daq_system.log
```

View logs to troubleshoot:
```powershell
Get-Content .\dist\DAQ_System\daq_system.log -Wait
```

## Summary

✅ **Complete system packaged in one .exe**
✅ **Frontend + Backend + Connection scripts bundled**
✅ **All dependencies included**
✅ **Easy to share and distribute**
✅ **No Python installation needed for end users**

**Ready to build? Run:** `python build_exe.py`

---

For more details, see:
- `BUILD_EXE_GUIDE.md` - Comprehensive guide
- `EXE_BUILD_QUICK_REFERENCE.md` - Quick reference
- `preflight_check.py` - Verify setup before building
