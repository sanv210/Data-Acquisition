# Backend Integration Guide

This directory contains all schemas and examples needed to build the backend API for the DAQ frontend.

## Quick Start

### 1. Review Schemas
- **`BACKEND_SCHEMAS.md`** - Comprehensive documentation with all field descriptions and dropdown options
- **`schemas/*.json`** - JSON Schema files for validation (use with libraries like `jsonschema` in Python)
- **`examples/*.json`** - Example payloads for testing

### 2. Implement Endpoints

Required endpoints:
```
POST /api/analytical-condition       → Accept analytical_condition_schema.json
POST /api/attenuator-information     → Accept attenuator_information_schema.json
POST /api/element-information        → Accept element_information_schema.json
POST /api/channel-information        → Accept channel_information_schema.json
```

### 3. Dropdown-Affected Fields

Only **Analytical Condition** page has dropdowns that affect the JSON:

| Field Path | Dropdown Options | Auto-fill Behavior |
|-----------|------------------|-------------------|
| `analytical_method` | 2 options | None |
| `seq.source.seq1` | 6 options | None |
| `seq.source.seq2` | 6 options | None |
| `seq.source.seq3` | 6 options | None |
| `seq.source.clean` | 6 options | None |
| `level_out_information.monitor_element.element` | 9 options | **Auto-fills `value` field** |
| `level_out_information.monitor_element.option1` | 9 options | None |
| `level_out_information.monitor_element.option2` | 9 options | None |

**Important:** When `monitor_element.element` changes, the frontend auto-fills `monitor_element.value` with a predefined numeric value (see mapping in BACKEND_SCHEMAS.md section 1).

### 4. Data Types

All fields are sent as **strings**. Backend must convert:
- Numeric fields: `"273.0"` → `273.0` (float) or `"3"` → `3` (int)
- Enum validation: Check against allowed dropdown values
- Empty strings: Handle as `null` or default values

### 5. Example Backend Validation (Python)

```python
import jsonschema
import json

# Load schema
with open('schemas/analytical_condition_schema.json') as f:
    schema = json.load(f)

# Validate request
def validate_analytical_condition(data):
    try:
        jsonschema.validate(instance=data, schema=schema)
        return True, None
    except jsonschema.ValidationError as e:
        return False, str(e)

# Convert types
def convert_analytical_condition(data):
    # Convert numeric strings
    data['seq']['purge']['seq1'] = int(data['seq']['purge']['seq1'])
    data['seq']['preburn']['seq1'] = int(data['seq']['preburn']['seq1'])
    # ... etc
    
    data['level_out_information']['monitor_element']['value'] = float(
        data['level_out_information']['monitor_element']['value']
    )
    
    # Convert arrays
    data['level_out_information']['h_level_percent'] = [
        int(x) for x in data['level_out_information']['h_level_percent']
    ]
    
    return data
```

### 6. Test with Example Files

```bash
# Test POST with curl
curl -X POST http://localhost:5000/api/analytical-condition \
  -H "Content-Type: application/json" \
  -d @examples/analytical_condition_default.json

curl -X POST http://localhost:5000/api/attenuator-information \
  -H "Content-Type: application/json" \
  -d @examples/attenuator_information_example.json
```

### 7. Expected Response Format

```json
{
  "success": true,
  "message": "Data saved successfully",
  "data": {
    "id": "uuid-or-generated-id",
    "analytical_group": "LAS 2023",
    "timestamp": "2025-11-07T10:30:00Z"
  }
}
```

Error response:
```json
{
  "success": false,
  "error": "Validation failed",
  "details": {
    "field": "analytical_method",
    "message": "Invalid value",
    "received": "InvalidMode",
    "allowed": ["integration Mode", "PDA + Integration"]
  }
}
```

## Dropdown Behavior Details

### Monitor Element Auto-fill Mapping

When user selects a monitor element, frontend automatically fills the value field:

```javascript
const MONITOR_ELEMENT_VALUES = {
  "None": "",
  "FE": "273.0",
  "C": "193.0",
  "Si": "212.4",
  "MN": "293.3",
  "P": "178.3",
  "S": "180.7",
  "V": "311.0",
  "CR": "267.7"  // or "298.9" - duplicate in source
};
```

**Backend should:**
1. Accept any numeric string in the `value` field (user can override auto-fill)
2. NOT validate against the mapping (user input takes precedence)
3. Store exactly what the frontend sends

### Source Options by SEQ

Different SEQ positions have different source options:

**SEQ1 Sources:**
- 3 Peak Spark
- Normal Spark
- Combined Spark
- Arclike Spark
- Cleaning
- High Voltage Spark

**SEQ2 Sources:**
- Normal Spark
- Combined Spark
- Arclike Spark
- Cleaning
- High Voltage Spark
- AD OFFSET

**SEQ3 Sources:**
- Lamp
- 3 Peak Spark
- Normal Spark
- Combined Spark
- Arclike Spark
- Cleaning

**Clean Source:**
- Cleaning
- High Voltage Spark
- AD OFFSET
- ITG OFFSET
- MAIN OFFSET
- NOISE TEST

## Files Structure

```
frontend/
├── BACKEND_SCHEMAS.md              # Main documentation (READ THIS FIRST)
├── schemas/                        # JSON Schema files for validation
│   ├── analytical_condition_schema.json
│   ├── attenuator_information_schema.json
│   ├── element_information_schema.json
│   └── channel_information_schema.json
├── examples/                       # Example payloads for testing
│   ├── analytical_condition_default.json
│   ├── analytical_condition_modified.json
│   ├── attenuator_information_example.json
│   ├── element_information_example.json
│   └── channel_information_example.json
└── README_BACKEND.md              # This file
```

## Common Integration Issues

### 1. String vs Number Types
**Problem:** All fields are strings, backend expects numbers  
**Solution:** Convert in backend after validation, example above

### 2. Empty Strings
**Problem:** Empty fields sent as `""`  
**Solution:** Treat as null/default or validate with `minLength: 1`

### 3. Duplicate Elements
**Problem:** CR appears twice (267.7 and 298.9)  
**Solution:** Backend should handle multiple entries for same element

### 4. Dynamic Arrays
**Problem:** Tables can have variable number of rows  
**Solution:** Use `minItems: 0` in schema, validate reasonable max

### 5. Monitor Element Override
**Problem:** User can override auto-filled value  
**Solution:** Don't validate against mapping, accept any numeric string

## Frontend Update Status

- ✅ Analytical Condition: Saves/loads via DataManager
- ✅ Attenuator Information: Saves/loads via DataManager
- ⚠️ Element Information: Collects JSON but doesn't persist (TODO)
- ⚠️ Channel Information: Collects JSON but doesn't persist (TODO)

All pages generate correct JSON on "Upload" button click.

## Next Steps

1. Read `BACKEND_SCHEMAS.md` for complete field documentation
2. Implement 4 POST endpoints with validation
3. Test with example JSON files
4. Return expected response format
5. Handle type conversions (string → number)
6. Implement error responses with field-level details

## Questions?

Refer to the source code:
- `pages/analytical_condition.py` → See `collect_form_data()` method
- `pages/attenuator_information.py` → See `collect_form_data()` method
- `pages/element_information.py` → See `collect_form_data()` method
- `pages/channel_information.py` → See `collect_form_data()` method
- `utils/data_manager.py` → See data persistence logic
