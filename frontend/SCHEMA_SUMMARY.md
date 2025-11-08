# Schema Documentation Summary

## 📋 What's Been Created

Complete backend integration documentation for the DAQ frontend application.

### 📁 Files Created

1. **BACKEND_SCHEMAS.md** (Main Documentation)
   - Complete field descriptions for all 4 pages
   - All dropdown options with allowed values
   - Example payloads (default and modified)
   - Integration notes and recommendations
   - ~450 lines of comprehensive documentation

2. **schemas/** (JSON Schema Files)
   - `analytical_condition_schema.json` - Formal JSON Schema with validation rules
   - `attenuator_information_schema.json` - Schema for attenuator data
   - `element_information_schema.json` - Schema for element data
   - `channel_information_schema.json` - Schema for channel data
   - Use these with validation libraries (Python: `jsonschema`, Node: `ajv`)

3. **examples/** (Test Payloads)
   - `analytical_condition_default.json` - Default values
   - `analytical_condition_modified.json` - Modified dropdown selections
   - `attenuator_information_example.json` - Attenuator table data
   - `element_information_example.json` - Element configurations
   - `channel_information_example.json` - Channel configurations
   - Ready for `curl` testing

4. **README_BACKEND.md** (Quick Start Guide)
   - Backend developer quick start
   - Endpoint structure recommendations
   - Python validation examples
   - Common integration issues
   - Testing commands

5. **DROPDOWN_REFERENCE.md** (Quick Lookup)
   - Visual dropdown option tables
   - Auto-fill behavior explanation
   - Comparison matrix
   - Test scenarios
   - API testing examples

---

## 🎯 Key Findings for Backend

### Pages with Dropdowns
**Only 1 page has dropdowns:** Analytical Condition Page

**8 dropdowns total:**
1. `analytical_method` - 2 options
2. `seq.source.seq1` - 6 options
3. `seq.source.seq2` - 6 options
4. `seq.source.seq3` - 6 options
5. `seq.source.clean` - 6 options
6. `level_out_information.monitor_element.element` - 9 options **WITH AUTO-FILL**
7. `level_out_information.monitor_element.option1` - 9 options
8. `level_out_information.monitor_element.option2` - 9 options

### Pages WITHOUT Dropdowns
- Attenuator Information Page - All text inputs
- Element Information Page - All text inputs
- Channel Information Page - All text inputs

### Critical Auto-fill Behavior
**Monitor Element Dropdown** has special behavior:
- When user selects an element (e.g., "FE"), the `value` field is automatically filled ("273.0")
- User can override this auto-filled value
- Backend must accept ANY numeric string in the value field (don't validate against mapping)

**Mapping:**
```
FE → 273.0
C → 193.0
Si → 212.4
MN → 293.3
P → 178.3
S → 180.7
V → 311.0
CR → 267.7 (or 298.9)
```

---

## 🔧 Backend Implementation Checklist

### Required Endpoints
```
POST /api/analytical-condition
POST /api/attenuator-information
POST /api/element-information
POST /api/channel-information
```

### Data Type Conversions
All fields arrive as **strings**. Backend must convert:
- Numeric values: `"273.0"` → `273.0` (float)
- Integer values: `"3"` → `3` (int)
- Arrays: `["0", "20", "0"]` → `[0, 20, 0]`

### Validation Requirements
1. **Dropdown values** - Validate against enum lists (see DROPDOWN_REFERENCE.md)
2. **Numeric strings** - Validate format before conversion
3. **Required fields** - Check all required fields exist
4. **Array lengths** - Validate reasonable sizes (h_level_percent: 9 items)

### Response Format
```json
{
  "success": true/false,
  "message": "Success or error description",
  "data": {
    "id": "generated-id",
    "analytical_group": "LAS 2023",
    "timestamp": "ISO-8601"
  }
}
```

---

## 📊 Schema Statistics

### Analytical Condition Page
- **Fields:** 28 individual fields
- **Dropdowns:** 8
- **Numeric inputs:** 13
- **Arrays:** 2 (9 items each)
- **Complexity:** HIGH (nested objects, multiple enums)

### Attenuator Information Page
- **Fields:** Dynamic (2 tables with variable rows)
- **Dropdowns:** 0
- **Tables:** 2 (left: 16 rows, right: 25+ rows with empties)
- **Complexity:** MEDIUM (array of objects)

### Element Information Page
- **Fields:** Dynamic (array of element configs)
- **Dropdowns:** 0
- **Default rows:** 23
- **Complexity:** MEDIUM (array of objects, 6 fields each)

### Channel Information Page
- **Fields:** Dynamic (array of channel configs)
- **Dropdowns:** 0
- **Default rows:** 22
- **Complexity:** MEDIUM (array of objects, 6 fields each)

---

## 🚀 Quick Start for Backend Developers

### 1. Read Documentation
Start here: `BACKEND_SCHEMAS.md` (comprehensive overview)

### 2. Review Schemas
Check: `schemas/*.json` (for validation library integration)

### 3. Test with Examples
Use: `examples/*.json` (copy-paste into Postman/curl)

### 4. Check Dropdown Reference
Quick lookup: `DROPDOWN_REFERENCE.md` (all allowed values)

### 5. Implement Endpoints
Follow: `README_BACKEND.md` (implementation guide)

---

## 🔍 How Dropdown Changes Affect JSON

### Example 1: Analytical Method Change
```json
// User selects "integration Mode" (default)
{"analytical_method": "integration Mode"}

// User changes to "PDA + Integration"
{"analytical_method": "PDA + Integration"}
```

### Example 2: Source Selection Change
```json
// Default state
{
  "seq": {
    "source": {
      "seq1": "3 Peak Spark",
      "seq2": "Normal Spark",
      "seq3": "Lamp"
    }
  }
}

// User changes all dropdowns
{
  "seq": {
    "source": {
      "seq1": "Normal Spark",      // Changed
      "seq2": "AD OFFSET",          // Changed
      "seq3": "3 Peak Spark"        // Changed
    }
  }
}
```

### Example 3: Monitor Element with Auto-fill
```json
// User selects "FE" → auto-fills value
{
  "monitor_element": {
    "element": "FE",
    "value": "273.0"  // Auto-filled
  }
}

// User selects "C" → auto-fills different value
{
  "monitor_element": {
    "element": "C",
    "value": "193.0"  // Auto-filled
  }
}

// User selects "C" but edits value manually
{
  "monitor_element": {
    "element": "C",
    "value": "200.0"  // User override (backend accepts this!)
  }
}
```

---

## 📝 Frontend Data Flow

```
User fills form
      ↓
Selects dropdowns (values populate JSON fields)
      ↓
Clicks "Upload" button
      ↓
Frontend calls collect_form_data()
      ↓
Reads all widget values (.get() on Entry/Combobox)
      ↓
Builds JSON object
      ↓
Saves to DataManager (Analytical & Attenuator pages)
      ↓
Prints JSON to console (POST not implemented yet)
      ↓
Shows messagebox with preview
```

**Note:** Element and Channel pages don't save to DataManager yet (TODO in code).

---

## ⚠️ Important Notes for Backend

1. **All values are strings** - Even numeric fields come as `"273.0"` not `273.0`

2. **Monitor element auto-fill** - Don't validate value against element mapping (user can override)

3. **Duplicate elements allowed** - CR appears twice (267.7 and 298.9), NI twice, MO twice

4. **Empty strings** - Fields can be empty `""`, decide how to handle (null vs default)

5. **Variable array lengths** - Tables can have different numbers of rows

6. **No frontend POST yet** - Current code only prints JSON, doesn't send to backend

---

## 📦 What You Can Do Now

### Test Validation
```bash
# Install jsonschema (Python)
pip install jsonschema

# Validate example payload
python -c "
import json, jsonschema
schema = json.load(open('schemas/analytical_condition_schema.json'))
data = json.load(open('examples/analytical_condition_default.json'))
jsonschema.validate(data, schema)
print('✓ Valid!')
"
```

### Mock Backend Test
```bash
# Create simple Flask endpoint
curl -X POST http://localhost:5000/api/analytical-condition \
  -H "Content-Type: application/json" \
  -d @examples/analytical_condition_default.json
```

### Generate Code from Schema
Use tools like:
- **Python:** `datamodel-code-generator` (generate Pydantic models)
- **TypeScript:** `json-schema-to-typescript`
- **Go:** `gojsonschema`

---

## 🎓 Next Steps

1. ✅ **Review** - Read BACKEND_SCHEMAS.md thoroughly
2. ✅ **Validate** - Test examples against schemas
3. ⏳ **Implement** - Build 4 POST endpoints
4. ⏳ **Test** - Use example JSON files
5. ⏳ **Connect** - Update frontend to call your endpoints

---

**Created:** November 7, 2025  
**Frontend Version:** Current codebase  
**Total Documentation:** ~1000+ lines across 5 files  
**JSON Schemas:** 4 formal schemas  
**Example Payloads:** 5 test files
