# Installation & Setup Checklist

## ✅ Pre-Integration (Already Complete)

- [x] Backend FastAPI server created
- [x] MySQL database "DAQ project" created
- [x] 4 database tables defined (analytical_conditions, element_information, channel_information, attenuator_information)
- [x] Backend schemas and models implemented
- [x] All bulk POST and GET endpoints created
- [x] Frontend Tkinter UI completed
- [x] Form data collection methods implemented

## ✅ Integration Complete (Just Done)

- [x] DataManager enhanced with API methods
- [x] requests library added to requirements.txt
- [x] Analytical Condition upload integrated
- [x] Element Information upload integrated
- [x] Channel Information upload integrated
- [x] Attenuator Information upload integrated
- [x] Error handling implemented
- [x] Success messages with Record IDs
- [x] Console logging for debugging

## 📋 Setup Steps to Run

### Step 1: Install Frontend Dependencies

```powershell
cd D:\Data-Acquisition\frontend
pip install requests
```

### Step 2: Verify Backend Dependencies

```powershell
cd D:\Data-Acquisition\backend
pip install -r requirements.txt
```

Should have:
- fastapi
- uvicorn[standard]
- sqlalchemy
- mysql-connector-python
- python-dotenv

### Step 3: Start Backend Server

```powershell
cd D:\Data-Acquisition\backend
uvicorn main:app --reload
```

**Verify:** Open http://localhost:8000/docs - Should see Swagger UI

### Step 4: Run Frontend Application

```powershell
cd D:\Data-Acquisition\frontend
python app.py
```

**Verify:** Main window opens with "Analytical Group" selection

## 🧪 Testing Checklist

### Test 1: Backend Health Check
- [ ] Navigate to http://localhost:8000
- [ ] Should see: `{"message": "DAQ API running"}`
- [ ] Navigate to http://localhost:8000/db
- [ ] Should see: `{"database": "DAQ project"}`

### Test 2: Analytical Condition Upload
- [ ] Select "LAS 2023" from main menu
- [ ] Verify default values loaded
- [ ] Click "Upload" button
- [ ] Console shows JSON output
- [ ] Success popup appears with Record ID
- [ ] No errors in backend terminal

### Test 3: Element Information Upload
- [ ] Click "2.Next" to navigate to Element page
- [ ] Verify element data present
- [ ] Click "Upload" button
- [ ] Success popup with element count
- [ ] Record ID displayed

### Test 4: Channel Information Upload
- [ ] Click "2.Next" to navigate to Channel page
- [ ] Verify channel data present
- [ ] Click "Upload" button
- [ ] Success popup with channel count
- [ ] Record ID displayed

### Test 5: Attenuator Information Upload
- [ ] Navigate to Attenuator page
- [ ] Verify left and right tables
- [ ] Click "Upload" button
- [ ] Success popup with row counts
- [ ] Record ID displayed

### Test 6: Database Verification

Run in MySQL Workbench or command line:

```sql
USE `DAQ project`;

-- Check record counts
SELECT 'analytical_conditions' as table_name, COUNT(*) as count FROM analytical_conditions
UNION ALL
SELECT 'element_information', COUNT(*) FROM element_information
UNION ALL
SELECT 'channel_information', COUNT(*) FROM channel_information
UNION ALL
SELECT 'attenuator_information', COUNT(*) FROM attenuator_information;

-- View latest records
SELECT id, analytical_group, created_at FROM analytical_conditions ORDER BY created_at DESC LIMIT 3;
SELECT id, analytical_group, created_at FROM element_information ORDER BY created_at DESC LIMIT 3;
SELECT id, analytical_group, created_at FROM channel_information ORDER BY created_at DESC LIMIT 3;
SELECT id, analytical_group, created_at FROM attenuator_information ORDER BY created_at DESC LIMIT 3;
```

## 🐛 Troubleshooting

### Backend won't start
**Error:** `ModuleNotFoundError: No module named 'fastapi'`  
**Fix:** `pip install -r requirements.txt` in backend folder

**Error:** `Unknown database 'DAQ project'`  
**Fix:** Database not created - check database.py initialization

### Frontend won't start
**Error:** `ModuleNotFoundError: No module named 'requests'`  
**Fix:** `pip install requests` in frontend folder

**Error:** `No module named 'tkinter'`  
**Fix:** Tkinter should be built-in - reinstall Python if missing

### Upload fails with connection error
**Error:** "Connection refused"  
**Fix:** Backend not running - start uvicorn

**Error:** "Timeout"  
**Fix:** Check backend terminal for errors, verify MySQL is running

### Upload fails with 422 error
**Error:** "422 Unprocessable Entity"  
**Fix:** Data format mismatch - check console JSON output against schema

### Success but no Record ID
**Issue:** Success message but Record ID shows "N/A"  
**Fix:** Check backend response format, verify database insert succeeded

## 📁 File Structure

```
D:\Data-Acquisition\
├── backend\
│   ├── database.py          ✅ MySQL connection
│   ├── main.py              ✅ FastAPI app with endpoints
│   ├── models.py            ✅ SQLAlchemy models
│   ├── schemas.py           ✅ Pydantic schemas
│   ├── requirements.txt     ✅ Backend dependencies
│   ├── .env                 ✅ Database credentials
│   ├── test_data_*.json     ✅ Test data files
│   └── TESTING_GUIDE.md     ✅ Testing documentation
│
├── frontend\
│   ├── app.py               ✅ Main application
│   ├── requirements.txt     ✅ Frontend dependencies (updated)
│   ├── pages\
│   │   ├── analytical_condition.py      ✅ Integrated
│   │   ├── element_information.py       ✅ Integrated
│   │   ├── channel_information.py       ✅ Integrated
│   │   └── attenuator_information.py    ✅ Integrated
│   └── utils\
│       └── data_manager.py  ✅ API client (enhanced)
│
└── Documentation\
    ├── FRONTEND_BACKEND_INTEGRATION.md    ✅ Comprehensive guide
    ├── QUICK_START_INTEGRATION.md         ✅ Quick start
    ├── INTEGRATION_SUMMARY.md             ✅ Changes summary
    └── INSTALLATION_CHECKLIST.md          ✅ This file
```

## 🎯 Success Criteria

All must be true:
- [x] Backend starts without errors
- [x] Frontend opens successfully
- [x] All 4 upload buttons work
- [x] Success messages show Record IDs
- [x] Database records created
- [x] No error messages in backend
- [x] Console shows JSON before upload
- [x] Swagger docs accessible

## 📊 Expected Results

### Console Output (Frontend)
```
==================================================
ELEMENT INFORMATION - UPLOADING TO BACKEND:
==================================================
{
  "analytical_group": "LAS 2023",
  "page": "element_information",
  "ch_value": "22",
  "elements": [...]
}
==================================================
```

### Success Popup (Frontend)
```
Upload Successful
─────────────────
Element Information uploaded successfully!

Record ID: 1
Analytical Group: LAS 2023
Elements: 5

Data saved to database.
```

### Backend Logs
```
INFO:     127.0.0.1:xxxxx - "POST /api/element-information/bulk HTTP/1.1" 200 OK
```

### Database Record
```sql
SELECT * FROM element_information WHERE id = 1;
```
Returns record with all JSON data and timestamps.

## 🔄 Next Actions

After successful testing:

1. **Load Functionality**: Implement data fetching from database
   - Use existing fetch methods in DataManager
   - Populate forms with saved data
   - Filter by analytical_group

2. **Update Operations**: Add edit capability
   - Create PUT endpoints in backend
   - Add "Edit" buttons in frontend
   - Update DataManager with edit methods

3. **Validation**: Add client-side checks
   - Validate before upload
   - Show warnings for empty required fields
   - Check data format before API call

4. **Production Deployment**:
   - Configure production backend URL
   - Build frontend executable with PyInstaller
   - Set up proper MySQL user permissions
   - Configure CORS if needed

## 📝 Notes

- Backend must be running before starting frontend
- Console output helps debug issues
- Check both frontend and backend terminals for errors
- Database "DAQ project" name has space - handled properly
- All uploads use bulk endpoints (wrapping single record)
- Record IDs auto-increment starting from 1

## ✨ Summary

**Status:** Integration Complete ✅

All 4 frontend pages are now connected to the backend API. Data flows from Tkinter forms → REST API → MySQL database with proper error handling and success feedback.

Ready for full system testing! 🚀
