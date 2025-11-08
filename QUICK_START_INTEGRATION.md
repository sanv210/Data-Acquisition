# Quick Start: Frontend-Backend Integration

## Setup Steps

### 1. Install Frontend Dependencies

```powershell
cd D:\Data-Acquisition\frontend
pip install -r requirements.txt
```

This will install:
- `requests>=2.31.0` - For HTTP API calls
- `pyinstaller==6.3.0` - For building executables

### 2. Start Backend Server

```powershell
cd D:\Data-Acquisition\backend
uvicorn main:app --reload
```

Verify it's running:
- Open browser to http://localhost:8000/docs
- You should see the FastAPI Swagger documentation

### 3. Run Frontend Application

```powershell
cd D:\Data-Acquisition\frontend
python app.py
```

## Testing the Integration

### Test 1: Analytical Condition Upload

1. **Select Group**: Choose "LAS 2023" from the main menu
2. **Verify Data**: Check that default values are loaded (integration Mode, seq values)
3. **Click Upload**: Press the "Upload" button
4. **Expected Result**: 
   - Console shows JSON being sent
   - Success popup with Record ID
   - Data saved to database

### Test 2: Element Information Upload

1. **Navigate**: Click "2.Next" button to go to Element Information page
2. **Verify Elements**: Check that elements like Fe, C, Si are present
3. **Click Upload**: Press the "Upload" button
4. **Expected Result**:
   - Success popup showing element count
   - Record ID displayed
   - Database record created

### Test 3: Channel Information Upload

1. **Navigate**: Click "2.Next" button from Element page
2. **Verify Channels**: Check wavelength data
3. **Click Upload**: Press the "Upload" button
4. **Expected Result**:
   - Success popup with channel count
   - Record saved to database

### Test 4: Attenuator Information Upload

1. **Navigate**: Use "3.Pre." button or direct navigation
2. **Verify Tables**: Check left and right table data
3. **Click Upload**: Press the "Upload" button
4. **Expected Result**:
   - Success popup with row counts
   - Both tables saved to database

## Verification

### Check Console Output

Look for this pattern in the terminal:

```
==================================================
ELEMENT INFORMATION - UPLOADING TO BACKEND:
==================================================
{
  "analytical_group": "LAS 2023",
  "page": "element_information",
  ...
}
==================================================
```

### Check Database

Using MySQL Workbench or command line:

```sql
USE `DAQ project`;

-- See latest uploads
SELECT * FROM analytical_conditions ORDER BY created_at DESC LIMIT 5;
SELECT * FROM element_information ORDER BY created_at DESC LIMIT 5;
SELECT * FROM channel_information ORDER BY created_at DESC LIMIT 5;
SELECT * FROM attenuator_information ORDER BY created_at DESC LIMIT 5;
```

## Success Indicators

✅ **Backend**: Server logs show POST requests
✅ **Frontend**: Success popups appear with Record IDs
✅ **Console**: JSON data printed before upload
✅ **Database**: New records with timestamps

## Common Issues

### Issue: "Connection refused"
**Solution**: Backend not running - start uvicorn

### Issue: "Module requests not found"
**Solution**: Run `pip install requests` in frontend directory

### Issue: "422 Unprocessable Entity"
**Solution**: Data format mismatch - check console JSON

### Issue: Empty success message
**Solution**: Check backend terminal for errors

## API Endpoints

All endpoints use: `http://localhost:8000/api`

- `POST /analytical-conditions/bulk` - Upload analytical conditions
- `POST /element-information/bulk` - Upload element information
- `POST /channel-information/bulk` - Upload channel information
- `POST /attenuator-information/bulk` - Upload attenuator information

## Architecture Summary

```
User Input (Tkinter GUI)
    ↓
collect_form_data()
    ↓
on_upload_clicked()
    ↓
DataManager.upload_xxx()
    ↓
HTTP POST → Backend API
    ↓
FastAPI Endpoint
    ↓
SQLAlchemy Model
    ↓
MySQL Database ("DAQ project")
    ↓
Return Response with ID
    ↓
Show Success Message
```

## Next Steps

After successful integration testing:

1. **Load Data**: Implement fetching existing records from database
2. **Edit Records**: Add update functionality 
3. **Delete Records**: Add delete operations for non-analytical-condition records
4. **Validation**: Add client-side validation before upload
5. **Error Recovery**: Implement retry logic for failed uploads

## Files Modified

- ✅ `frontend/utils/data_manager.py` - Added API integration methods
- ✅ `frontend/pages/analytical_condition.py` - Integrated upload
- ✅ `frontend/pages/element_information.py` - Integrated upload
- ✅ `frontend/pages/channel_information.py` - Integrated upload
- ✅ `frontend/pages/attenuator_information.py` - Integrated upload
- ✅ `frontend/requirements.txt` - Added requests library

Integration is complete! 🎉
