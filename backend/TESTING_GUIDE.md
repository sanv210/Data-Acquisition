# DAQ Backend API - Testing Guide

## Overview
The backend now has **4 complete endpoints** with bulk POST and GET operations:

1. **Analytical Conditions** - `/api/analytical-conditions/bulk`
2. **Element Information** - `/api/element-information/bulk`
3. **Channel Information** - `/api/channel-information/bulk`
4. **Attenuator Information** - `/api/attenuator-information/bulk`

---

## Database Tables Created

After restarting the server, these tables will be created in the `DAQ project` database:

1. `analytical_conditions` - stores analytical condition configurations
2. `element_information` - stores element configurations with ranges
3. `channel_information` - stores channel configurations with wavelengths
4. `attenuator_information` - stores attenuator data for left/right tables

---

## How to Restart and Test

### Step 1: Drop existing tables (if any issues)
```sql
USE `DAQ project`;
DROP TABLE IF EXISTS analytical_conditions;
DROP TABLE IF EXISTS element_information;
DROP TABLE IF EXISTS channel_information;
DROP TABLE IF EXISTS attenuator_information;
SHOW TABLES;
```

### Step 2: Restart the FastAPI server
```powershell
# Stop current server (Ctrl+C in uvicorn terminal)
cd d:\Data-Acquisition\backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Step 3: Verify tables were created
```sql
USE `DAQ project`;
SHOW TABLES;
-- Should show 4 tables

DESCRIBE analytical_conditions;
DESCRIBE element_information;
DESCRIBE channel_information;
DESCRIBE attenuator_information;
```

---

## API Endpoints

### Base URL
```
http://localhost:8000
```

### Interactive API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## Testing Each Endpoint

### 1. Analytical Conditions

#### POST - Create Records
```powershell
$body = Get-Content "d:\Data-Acquisition\backend\test_data_analytical_conditions.json" -Raw
$response = Invoke-RestMethod -Uri "http://localhost:8000/api/analytical-conditions/bulk" -Method POST -Body $body -ContentType "application/json"
$response | ConvertTo-Json -Depth 10
```

#### GET - Retrieve All Records
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/analytical-conditions/bulk" -Method GET | ConvertTo-Json -Depth 10
```

#### GET - Filter by Analytical Group
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/analytical-conditions/bulk?analytical_group=LAS%202023" -Method GET | ConvertTo-Json -Depth 10
```

---

### 2. Element Information

#### POST - Create Records
```powershell
$body = @"
{
  "records": [
    {
      "analytical_group": "LAS 2023",
      "page": "element_information",
      "ch_value": "22",
      "elements": [
        {
          "ele_name": "Fe",
          "analytical_range_min": "0.001",
          "analytical_range_max": "99.999",
          "asterisk": "*",
          "chemic_ele": "FE",
          "element": "Iron"
        },
        {
          "ele_name": "C",
          "analytical_range_min": "0.001",
          "analytical_range_max": "5.000",
          "asterisk": "",
          "chemic_ele": "C",
          "element": "Carbon"
        }
      ]
    }
  ]
}
"@
$response = Invoke-RestMethod -Uri "http://localhost:8000/api/element-information/bulk" -Method POST -Body $body -ContentType "application/json"
$response | ConvertTo-Json -Depth 10
```

#### GET - Retrieve All Records
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/element-information/bulk" -Method GET | ConvertTo-Json -Depth 10
```

---

### 3. Channel Information

#### POST - Create Records
```powershell
$body = @"
{
  "records": [
    {
      "analytical_group": "LAS 2023",
      "page": "channel_information",
      "channels": [
        {
          "ele_name": "Fe",
          "w_lengh": "259.940",
          "seq": "1",
          "w_no": "1",
          "interval_element": "Ar",
          "interval_value": "0.015"
        },
        {
          "ele_name": "C",
          "w_lengh": "193.091",
          "seq": "2",
          "w_no": "",
          "interval_element": "Fe",
          "interval_value": "0.020"
        }
      ]
    }
  ]
}
"@
$response = Invoke-RestMethod -Uri "http://localhost:8000/api/channel-information/bulk" -Method POST -Body $body -ContentType "application/json"
$response | ConvertTo-Json -Depth 10
```

#### GET - Retrieve All Records
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/channel-information/bulk" -Method GET | ConvertTo-Json -Depth 10
```

---

### 4. Attenuator Information

#### POST - Create Records
```powershell
$body = @"
{
  "records": [
    {
      "analytical_group": "LAS 2023",
      "page": "attenuator_information",
      "left_table": [
        {
          "element": "FE",
          "ele_value": "259.940",
          "att_value": "0"
        },
        {
          "element": "C",
          "ele_value": "193.091",
          "att_value": "2"
        }
      ],
      "right_table": [
        {
          "element": "SI",
          "ele_value": "251.611",
          "att_value": "1"
        },
        {
          "element": "MN",
          "ele_value": "257.610",
          "att_value": "0"
        }
      ]
    }
  ]
}
"@
$response = Invoke-RestMethod -Uri "http://localhost:8000/api/attenuator-information/bulk" -Method POST -Body $body -ContentType "application/json"
$response | ConvertTo-Json -Depth 10
```

#### GET - Retrieve All Records
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/attenuator-information/bulk" -Method GET | ConvertTo-Json -Depth 10
```

---

## Common Query Parameters (for GET endpoints)

All bulk GET endpoints support these optional query parameters:

- `analytical_group` - Filter by analytical group name (e.g., "LAS 2023")
- `limit` - Maximum number of records to return

### Example with filters:
```powershell
# Get only LAS 2023 records, limit to 10
Invoke-RestMethod -Uri "http://localhost:8000/api/element-information/bulk?analytical_group=LAS%202023&limit=10" -Method GET
```

---

## Response Format

All bulk responses follow this structure:

```json
{
  "success": true,
  "message": "Successfully created X record(s)" or "Retrieved X record(s)",
  "count": 2,
  "records": [
    {
      "id": 1,
      "analytical_group": "LAS 2023",
      // ... other fields specific to the endpoint
      "created_at": "2025-11-08T13:45:00Z",
      "updated_at": "2025-11-08T13:45:00Z"
    }
  ]
}
```

---

## Error Handling

All endpoints return descriptive error messages:

- **400 Bad Request** - Validation errors or data issues
- **404 Not Found** - Record not found (for single record endpoints)
- **500 Internal Server Error** - Database or server issues

Example error response:
```json
{
  "detail": "Error creating records: <specific error message>"
}
```

---

## Database Schema Reference

### All Tables Include:
- `id` - Primary key (auto-increment)
- `analytical_group` - VARCHAR(100), indexed
- `created_at` - Timestamp (auto-generated)
- `updated_at` - Timestamp (auto-updated)

### Analytical Conditions Table:
- `analytical_method` - VARCHAR(50)
- `seq` - JSON (purge, source, preburn, integ, clean)
- `level_out_information` - JSON (monitor_element, h_level_percent, l_level_percent)

### Element Information Table:
- `page` - VARCHAR(50) = "element_information"
- `ch_value` - VARCHAR(10)
- `elements` - JSON array

### Channel Information Table:
- `page` - VARCHAR(50) = "channel_information"
- `channels` - JSON array

### Attenuator Information Table:
- `page` - VARCHAR(50) = "attenuator_information"
- `left_table` - JSON array
- `right_table` - JSON array

---

## Next Steps

1. **Drop old tables** (if any errors with columns)
2. **Restart server** (creates tables automatically)
3. **Test each endpoint** using the PowerShell commands above
4. **Verify in MySQL** that data is stored correctly
5. **Test GET endpoints** to retrieve the stored data

---

## Tips

- Use the interactive docs at http://localhost:8000/docs to test endpoints visually
- Check server logs for detailed error messages
- Verify JSON payload matches the schema exactly
- Use `ConvertTo-Json -Depth 10` to see nested objects in PowerShell
- Filter by `analytical_group` to separate different project data
