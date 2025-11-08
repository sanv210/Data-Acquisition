# Frontend-Backend Integration Guide

This guide explains how the frontend Tkinter application integrates with the FastAPI backend to upload and retrieve data.

## Overview

The integration connects the frontend GUI forms with the backend REST API endpoints. Data flows from user input → form collection → API upload → database storage.

## Architecture

```
Frontend (Tkinter)          Backend (FastAPI)         Database (MySQL)
─────────────────           ─────────────────         ─────────────────
│                           │                         │
│  User fills form          │                         │
│       ↓                   │                         │
│  collect_form_data()      │                         │
│       ↓                   │                         │
│  on_upload_clicked()      │                         │
│       ↓                   │                         │
│  DataManager              │                         │
│   .upload_xxx()  ────────→│ POST /api/xxx/bulk      │
│                           │       ↓                 │
│                           │  Create record  ────────→│ INSERT
│                           │       ↓                 │
│  ←────────────────────────│  Return response        │
│  Show success message     │   with ID               │
│                           │                         │
```

## Components

### 1. DataManager (`frontend/utils/data_manager.py`)

Central API client that handles all HTTP communication:

**API Methods:**
- `upload_analytical_condition(data)` - Upload analytical conditions
- `upload_element_information(data)` - Upload element information
- `upload_channel_information(data)` - Upload channel information
- `upload_attenuator_information(data)` - Upload attenuator information
- `fetch_xxx(analytical_group)` - Fetch records (for future use)

**Configuration:**
- Base URL: `http://localhost:8000/api`
- Timeout: 10 seconds
- Content-Type: application/json

### 2. Frontend Pages

Each page has an integrated upload button:

**Analytical Condition** (`pages/analytical_condition.py`)
- Endpoint: `POST /api/analytical-conditions/bulk`
- Collects: analytical_method, seq data, level_out_information
- Success: Shows Record ID and method

**Element Information** (`pages/element_information.py`)
- Endpoint: `POST /api/element-information/bulk`
- Collects: elements array with analytical ranges
- Success: Shows Record ID and element count

**Channel Information** (`pages/channel_information.py`)
- Endpoint: `POST /api/channel-information/bulk`
- Collects: channels array with wavelengths
- Success: Shows Record ID and channel count

**Attenuator Information** (`pages/attenuator_information.py`)
- Endpoint: `POST /api/attenuator-information/bulk`
- Collects: left_table and right_table arrays
- Success: Shows Record ID and table row counts

## Data Flow

### 1. User Action
User fills form fields and clicks "Upload" button

### 2. Data Collection
`collect_form_data()` gathers all form values into JSON structure:
```python
{
    "analytical_group": "LAS 2023",
    "page": "element_information",
    "elements": [...]
}
```

### 3. API Upload
`on_upload_clicked()` calls DataManager method:
```python
response = self.data_manager.upload_element_information(form_data)
```

### 4. Backend Processing
Backend wraps in bulk format and creates database record:
```python
bulk_data = {"records": [data]}
# POST to /api/element-information/bulk
```

### 5. Response Handling
Frontend displays success message with:
- Record ID from database
- Analytical group name
- Item counts (elements, channels, etc.)

## Error Handling

### Connection Errors
If backend is not running:
```
Upload Failed
Failed to upload data to backend:

API Error: [Connection details]

Please ensure the backend server is running on http://localhost:8000
```

### Validation Errors
If data doesn't match schema:
```
Upload Failed
Failed to upload data to backend:

API Error: 422 Unprocessable Entity
```

### Network Timeouts
After 10 seconds without response:
```
Upload Failed
Failed to upload data to backend:

API Error: Timeout
```

## Testing the Integration

### Prerequisites
1. **Backend running:**
   ```powershell
   cd backend
   uvicorn main:app --reload
   ```

2. **Frontend dependencies installed:**
   ```powershell
   cd frontend
   pip install -r requirements.txt
   ```

### Test Procedure

1. **Start Backend Server**
   ```powershell
   cd D:\Data-Acquisition\backend
   uvicorn main:app --reload
   ```
   Verify: http://localhost:8000/docs

2. **Run Frontend Application**
   ```powershell
   cd D:\Data-Acquisition\frontend
   python app.py
   ```

3. **Test Each Screen**

   **Analytical Condition:**
   - Select "LAS 2023" from main menu
   - Verify default values are loaded
   - Click "Upload" button
   - Expected: Success message with Record ID
   - Verify in console: JSON printed before upload
   - Check database: New record in `analytical_conditions` table

   **Element Information:**
   - Click "2.Next" to navigate to Element page
   - Fill in element data (or verify defaults)
   - Click "Upload" button
   - Expected: Success with element count
   - Check database: New record in `element_information` table

   **Channel Information:**
   - Click "2.Next" to navigate to Channel page
   - Fill in channel wavelength data
   - Click "Upload" button
   - Expected: Success with channel count
   - Check database: New record in `channel_information` table

   **Attenuator Information:**
   - Click "3.Pre." to go back or navigate to Attenuator page
   - Verify left and right table data
   - Click "Upload" button
   - Expected: Success with row counts
   - Check database: New record in `attenuator_information` table

### Verify in Database

Using MySQL Workbench or command line:

```sql
-- Check analytical conditions
SELECT id, analytical_group, analytical_method, created_at 
FROM `DAQ project`.analytical_conditions 
ORDER BY created_at DESC LIMIT 5;

-- Check element information
SELECT id, analytical_group, JSON_LENGTH(elements) as element_count, created_at
FROM `DAQ project`.element_information
ORDER BY created_at DESC LIMIT 5;

-- Check channel information
SELECT id, analytical_group, JSON_LENGTH(channels) as channel_count, created_at
FROM `DAQ project`.channel_information
ORDER BY created_at DESC LIMIT 5;

-- Check attenuator information
SELECT id, analytical_group, 
       JSON_LENGTH(left_table) as left_count,
       JSON_LENGTH(right_table) as right_count, 
       created_at
FROM `DAQ project`.attenuator_information
ORDER BY created_at DESC LIMIT 5;
```

## API Endpoints Reference

### Analytical Conditions
- **POST** `/api/analytical-conditions/bulk` - Create records
- **GET** `/api/analytical-conditions/bulk` - Retrieve all
- **GET** `/api/analytical-conditions/{id}` - Get by ID
- **DELETE** `/api/analytical-conditions/{id}` - Delete record

### Element Information
- **POST** `/api/element-information/bulk` - Create records
- **GET** `/api/element-information/bulk` - Retrieve all
- **GET** `/api/element-information/{id}` - Get by ID

### Channel Information
- **POST** `/api/channel-information/bulk` - Create records
- **GET** `/api/channel-information/bulk` - Retrieve all
- **GET** `/api/channel-information/{id}` - Get by ID

### Attenuator Information
- **POST** `/api/attenuator-information/bulk` - Create records
- **GET** `/api/attenuator-information/bulk` - Retrieve all
- **GET** `/api/attenuator-information/{id}` - Get by ID

## Console Output

When uploading, check the terminal/console for detailed JSON:

```
==================================================
ELEMENT INFORMATION - UPLOADING TO BACKEND:
==================================================
{
  "analytical_group": "LAS 2023",
  "page": "element_information",
  "ch_value": "22",
  "elements": [
    {
      "ele_name": "Fe",
      "analytical_range_min": "0.001",
      ...
    }
  ]
}
==================================================
```

## Troubleshooting

### "Connection refused" error
- Backend server is not running
- Solution: Start uvicorn in backend directory

### "Import requests could not be resolved"
- requests library not installed
- Solution: `pip install requests`

### "422 Unprocessable Entity"
- Data doesn't match backend schema
- Check console JSON output
- Verify field names and types

### "Module 'utils' not found"
- Wrong working directory
- Solution: Run from frontend directory

### Empty response or timeout
- Backend processing issue
- Check backend terminal for errors
- Verify database connection

## Future Enhancements

1. **Data Loading**: Implement fetch methods to load existing data
2. **Update Operations**: Add PUT endpoints for editing records
3. **Validation**: Client-side validation before upload
4. **Progress Indicators**: Loading spinners during API calls
5. **Offline Mode**: Queue uploads when backend unavailable
6. **Batch Operations**: Upload multiple analytical groups at once

## Configuration

To change the backend URL, edit `frontend/utils/data_manager.py`:

```python
class DataManager:
    # Change this if backend runs on different host/port
    API_BASE_URL = "http://localhost:8000/api"
```

For production, use environment variables:
```python
import os
API_BASE_URL = os.getenv('BACKEND_URL', 'http://localhost:8000/api')
```

## Summary

✅ All 4 frontend pages integrated with backend
✅ Upload button sends data to REST API
✅ Success/error messages with details
✅ JSON printed to console for debugging
✅ Database records created with IDs
✅ Proper error handling for all scenarios

The integration is complete and ready for testing!
