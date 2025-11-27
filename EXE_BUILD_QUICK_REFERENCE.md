# DAQ System .exe Build Summary

## Files Created

1. **launcher.py** - Main entry point that launches both backend and frontend
2. **build_exe.py** - Python script to build the .exe using PyInstaller
3. **DAQ_System.spec** - PyInstaller specification file (defines what to include)
4. **build.bat** - Windows batch file for quick building
5. **build_requirements.txt** - Build dependencies
6. **BUILD_EXE_GUIDE.md** - Comprehensive build documentation

## Quick Start - 3 Steps

### Step 1: Activate Virtual Environment
```powershell
cd C:\Users\jhaad\Downloads\Data-Acquisition
.\venv\Scripts\Activate.ps1
```

### Step 2: Install Build Tools
```powershell
pip install pyinstaller
```

### Step 3: Build the .exe
```powershell
# Option A: Run Python build script
python build_exe.py

# Option B: Use batch file (Windows only)
build.bat
```

## What Gets Packaged

✓ **Frontend** - Tkinter GUI (analytical group selection, forms, etc.)
✓ **Backend** - FastAPI REST API with MySQL database
✓ **Connection** - Integration scripts (populate_test_data.py, integration.py)
✓ **All Python dependencies** - Auto-bundled with the .exe
✓ **.env file** - Database configuration

## Output

After successful build, find your `.exe` at:
```
C:\Users\jhaad\Downloads\Data-Acquisition\dist\DAQ_System\DAQ_System.exe
```

## How to Run the .exe

1. **Ensure MySQL is running**
   - Open Services or command line
   - Start MySQL service

2. **Double-click the .exe**
   - Backend starts automatically
   - Frontend GUI opens
   - Both connect seamlessly

3. **Logs saved to**
   - `daq_system.log` in the same directory as the .exe

## File Size

Typical .exe package size: **60-150 MB** (includes all Python libraries and dependencies)

## System Requirements

Users running the .exe need:
- Windows 7+ (or macOS/Linux with native build)
- MySQL server running
- ~200MB disk space

## What's Inside the .exe

```
DAQ_System.exe (main executable)
├── Backend files (FastAPI, SQLAlchemy, etc.)
├── Frontend files (Tkinter GUI, pages)
├── Connection folder (integration scripts)
├── Python runtime
├── All required libraries bundled
└── .env (database config)
```

## Customization

Before building, you can:

1. **Change icon** - Add `.ico` file to `frontend/assets/icon.ico`
2. **Hide console** - Edit `DAQ_System.spec`, set `console=False`
3. **Add features** - Modify `launcher.py` to add more functionality
4. **Adjust logging** - Modify logging configuration in `launcher.py`

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "PyInstaller not found" | Run: `pip install pyinstaller` |
| "Module not found" | Add to `hiddenimports` in `DAQ_System.spec` |
| Backend won't start | Check MySQL running, verify `.env` credentials |
| Large file size | Normal - includes all dependencies |
| Application crashes | Check `daq_system.log` for error details |

## Distribution

To share the application:
1. Zip the entire `dist\DAQ_System` folder
2. Users extract and run `DAQ_System.exe`
3. Ensure they have MySQL installed and running

## Next Steps

1. Ensure `.env` has correct MySQL credentials:
   ```
   MYSQL_USER=root
   MYSQL_PASSWORD=your_password
   MYSQL_HOST=localhost
   MYSQL_PORT=3306
   ```

2. Test the build:
   ```powershell
   python build_exe.py
   ```

3. Run the created .exe:
   ```powershell
   .\dist\DAQ_System\DAQ_System.exe
   ```

---

**Ready to build?** Run: `python build_exe.py`
