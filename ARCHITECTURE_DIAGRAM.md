# Frontend-Backend Integration Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                               │
│                      (Tkinter Desktop App)                          │
└─────────────────────────────────────────────────────────────────────┘
                                 │
                                 │ User clicks Upload
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     FRONTEND APPLICATION                             │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐ │
│  │ Analytical       │  │ Element          │  │ Channel          │ │
│  │ Condition Page   │  │ Information Page │  │ Information Page │ │
│  └────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘ │
│           │                     │                      │            │
│           └─────────────────────┼──────────────────────┘            │
│                                 │                                    │
│                    ┌────────────▼────────────┐                      │
│                    │  Attenuator Info Page   │                      │
│                    └────────────┬────────────┘                      │
│                                 │                                    │
│                    ┌────────────▼────────────┐                      │
│                    │   Data Manager          │                      │
│                    │   (API Client)          │                      │
│                    │                         │                      │
│                    │ - upload_xxx()          │                      │
│                    │ - fetch_xxx()           │                      │
│                    │ - API_BASE_URL          │                      │
│                    └────────────┬────────────┘                      │
└─────────────────────────────────┼───────────────────────────────────┘
                                  │
                                  │ HTTP POST/GET
                                  │ JSON payload
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     BACKEND API (FastAPI)                           │
│                    http://localhost:8000/api                        │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐│
│  │                      API ENDPOINTS                              ││
│  │                                                                  ││
│  │  POST /analytical-conditions/bulk                               ││
│  │  GET  /analytical-conditions/bulk                               ││
│  │  GET  /analytical-conditions/{id}                               ││
│  │                                                                  ││
│  │  POST /element-information/bulk                                 ││
│  │  GET  /element-information/bulk                                 ││
│  │  GET  /element-information/{id}                                 ││
│  │                                                                  ││
│  │  POST /channel-information/bulk                                 ││
│  │  GET  /channel-information/bulk                                 ││
│  │  GET  /channel-information/{id}                                 ││
│  │                                                                  ││
│  │  POST /attenuator-information/bulk                              ││
│  │  GET  /attenuator-information/bulk                              ││
│  │  GET  /attenuator-information/{id}                              ││
│  └────────────────────────────┬─────────────────────────────────────┘│
│                                │                                      │
│  ┌────────────────────────────▼─────────────────────────────────────┐│
│  │                   PYDANTIC SCHEMAS                                ││
│  │                  (Data Validation)                                ││
│  │                                                                   ││
│  │  - AnalyticalConditionCreate/Response                            ││
│  │  - ElementInformationCreate/Response                             ││
│  │  - ChannelInformationCreate/Response                             ││
│  │  - AttenuatorInformationCreate/Response                          ││
│  │  - BulkCreate/BulkResponse schemas                               ││
│  └────────────────────────────┬─────────────────────────────────────┘│
│                                │                                      │
│  ┌────────────────────────────▼─────────────────────────────────────┐│
│  │                   SQLAlchemy MODELS                               ││
│  │                  (ORM Layer)                                      ││
│  │                                                                   ││
│  │  - AnalyticalCondition                                           ││
│  │  - ElementInformation                                            ││
│  │  - ChannelInformation                                            ││
│  │  - AttenuatorInformation                                         ││
│  └────────────────────────────┬─────────────────────────────────────┘│
└─────────────────────────────────┼───────────────────────────────────┘
                                  │
                                  │ SQL Queries
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   MySQL DATABASE                                     │
│                   Database: "DAQ project"                            │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐│
│  │ analytical_conditions                                           ││
│  │ ├─ id (PK)                                                      ││
│  │ ├─ analytical_group                                             ││
│  │ ├─ analytical_method                                            ││
│  │ ├─ seq (JSON)                                                   ││
│  │ ├─ level_out_information (JSON)                                 ││
│  │ ├─ created_at                                                   ││
│  │ └─ updated_at                                                   ││
│  └────────────────────────────────────────────────────────────────┘│
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐│
│  │ element_information                                             ││
│  │ ├─ id (PK)                                                      ││
│  │ ├─ analytical_group                                             ││
│  │ ├─ ch_value                                                     ││
│  │ ├─ elements (JSON Array)                                        ││
│  │ ├─ created_at                                                   ││
│  │ └─ updated_at                                                   ││
│  └────────────────────────────────────────────────────────────────┘│
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐│
│  │ channel_information                                             ││
│  │ ├─ id (PK)                                                      ││
│  │ ├─ analytical_group                                             ││
│  │ ├─ channels (JSON Array)                                        ││
│  │ ├─ created_at                                                   ││
│  │ └─ updated_at                                                   ││
│  └────────────────────────────────────────────────────────────────┘│
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐│
│  │ attenuator_information                                          ││
│  │ ├─ id (PK)                                                      ││
│  │ ├─ analytical_group                                             ││
│  │ ├─ left_table (JSON Array)                                      ││
│  │ ├─ right_table (JSON Array)                                     ││
│  │ ├─ created_at                                                   ││
│  │ └─ updated_at                                                   ││
│  └────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────┘
```

## Data Flow Sequence

### Upload Flow (Frontend → Backend → Database)

```
1. User Input
   ├─ User fills form fields
   └─ User clicks "Upload" button

2. Data Collection
   ├─ collect_form_data() gathers values
   └─ Returns JSON object

3. API Call
   ├─ on_upload_clicked() triggered
   ├─ DataManager.upload_xxx(data)
   ├─ Wraps: {"records": [data]}
   └─ POST to backend endpoint

4. Backend Processing
   ├─ FastAPI receives request
   ├─ Pydantic validates schema
   ├─ SQLAlchemy creates model
   └─ SQL INSERT executed

5. Database Storage
   ├─ MySQL stores record
   ├─ Auto-generates ID
   └─ Sets timestamps

6. Response
   ├─ Backend returns JSON
   ├─ Includes ID and timestamps
   └─ Frontend displays success
```

## Request/Response Example

### Frontend Sends:

```json
POST http://localhost:8000/api/element-information/bulk
Content-Type: application/json

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
          "analytical_range_max": "5.000",
          "asterisk": "",
          "chemic_ele": "Fe",
          "element": "Fe"
        }
      ]
    }
  ]
}
```

### Backend Returns:

```json
HTTP/1.1 200 OK
Content-Type: application/json

{
  "records": [
    {
      "id": 1,
      "analytical_group": "LAS 2023",
      "page": "element_information",
      "ch_value": "22",
      "elements": [
        {
          "ele_name": "Fe",
          "analytical_range_min": "0.001",
          "analytical_range_max": "5.000",
          "asterisk": "",
          "chemic_ele": "Fe",
          "element": "Fe"
        }
      ],
      "created_at": "2025-11-08T10:30:00",
      "updated_at": "2025-11-08T10:30:00"
    }
  ]
}
```

## Component Interactions

### DataManager Class

```python
class DataManager:
    API_BASE_URL = "http://localhost:8000/api"
    
    def upload_element_information(self, data):
        bulk_data = {"records": [data]}
        response = requests.post(
            f"{self.API_BASE_URL}/element-information/bulk",
            json=bulk_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        return response.json()
```

### Page Upload Method

```python
def on_upload_clicked(self):
    # 1. Collect form data
    form_data = self.collect_form_data()
    
    # 2. Upload to backend
    response = self.data_manager.upload_element_information(form_data)
    
    # 3. Show success
    if response and 'records' in response:
        record_id = response['records'][0].get('id')
        messagebox.showinfo("Success", f"Record ID: {record_id}")
```

### Backend Endpoint

```python
@app.post("/api/element-information/bulk")
def bulk_create_element_information(
    bulk_data: ElementInformationBulkCreate,
    db: Session = Depends(get_db)
):
    created_records = []
    for record_data in bulk_data.records:
        db_record = ElementInformation(**record_data.model_dump())
        db.add(db_record)
        db.commit()
        db.refresh(db_record)
        created_records.append(db_record)
    
    return ElementInformationBulkResponse(records=created_records)
```

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend UI | Tkinter | Desktop GUI forms |
| Frontend Logic | Python 3.x | Form handling, validation |
| HTTP Client | requests | API communication |
| API Framework | FastAPI | REST endpoints |
| Data Validation | Pydantic v2 | Schema validation |
| ORM | SQLAlchemy | Database operations |
| Database Driver | mysql-connector-python | MySQL connection |
| Database | MySQL 8.0+ | Data storage |
| Server | Uvicorn | ASGI server |

## File Responsibilities

```
Frontend Files:
├─ pages/analytical_condition.py     → Analytical Condition UI & upload
├─ pages/element_information.py      → Element Information UI & upload
├─ pages/channel_information.py      → Channel Information UI & upload
├─ pages/attenuator_information.py   → Attenuator Information UI & upload
└─ utils/data_manager.py             → API client & HTTP communication

Backend Files:
├─ main.py                           → FastAPI app & endpoints
├─ schemas.py                        → Pydantic validation schemas
├─ models.py                         → SQLAlchemy ORM models
└─ database.py                       → MySQL connection & session
```

## Integration Points

1. **API URL**: `http://localhost:8000/api` (configurable in DataManager)
2. **Authentication**: None (add JWT if needed)
3. **Timeout**: 10 seconds per request
4. **Error Handling**: Exception catching with user-friendly messages
5. **Logging**: Console output for debugging
6. **Data Format**: JSON with bulk wrapper
7. **Response Parsing**: Extract Record ID from response

## Future Enhancements

- [ ] Load existing data from database
- [ ] Update/Edit functionality
- [ ] Delete operations for all resources
- [ ] Search and filter capabilities
- [ ] Batch uploads (multiple groups)
- [ ] Progress bars for uploads
- [ ] Offline mode with queue
- [ ] Authentication & authorization
- [ ] Audit logging
- [ ] Export to Excel/CSV

---

**Status**: ✅ Integration Complete
**Version**: 1.0.0
**Date**: November 8, 2025
