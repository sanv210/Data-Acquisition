# Backend API Schemas - DAQ Frontend

This document provides the complete JSON schemas for all pages in the DAQ frontend application. Use these schemas to build your backend API endpoints.

---

## Table of Contents
1. [Analytical Condition Page](#1-analytical-condition-page)
2. [Attenuator Information Page](#2-attenuator-information-page)
3. [Element Information Page](#3-element-information-page)
4. [Channel Information Page](#4-channel-information-page)
5. [Integration Notes](#5-integration-notes)

---

## 1. Analytical Condition Page

### Endpoint Suggestion
`POST /api/analytical-condition`

### Schema Structure

```json
{
  "analytical_group": "string",
  "analytical_method": "string (enum)",
  "seq": {
    "purge": {
      "seq1": "string (numeric)"
    },
    "source": {
      "seq1": "string (enum)",
      "seq2": "string (enum)",
      "seq3": "string (enum)",
      "clean": "string (enum)"
    },
    "preburn": {
      "seq1": "string (numeric)",
      "seq2": "string (numeric)",
      "seq3": "string (numeric)",
      "clean": "string (literal: 'Pulse')"
    },
    "integ": {
      "seq1": "string (numeric)",
      "seq2": "string (numeric)",
      "seq3": "string (numeric)",
      "clean": "string (literal: 'Pulse')"
    },
    "clean": {
      "value": "string (numeric)",
      "unit": "string (literal: 'Pulse')"
    }
  },
  "level_out_information": {
    "monitor_element": {
      "element": "string (enum)",
      "value": "string (numeric)",
      "option1": "string (enum)",
      "option2": "string (enum)"
    },
    "h_level_percent": ["string (numeric)", ...],
    "l_level_percent": ["string (numeric)", ...]
  }
}
```

### Dropdown Options (Enums)

#### `analytical_method` (dropdown options)
- `"integration Mode"`
- `"PDA + Integration"`

#### `seq.source.seq1` (dropdown options)
- `"3 Peak Spark"`
- `"Normal Spark"`
- `"Combined Spark"`
- `"Arclike Spark"`
- `"Cleaning"`
- `"High Voltage Spark"`

#### `seq.source.seq2` (dropdown options)
- `"Normal Spark"`
- `"Combined Spark"`
- `"Arclike Spark"`
- `"Cleaning"`
- `"High Voltage Spark"`
- `"AD OFFSET"`

#### `seq.source.seq3` (dropdown options)
- `"Lamp"`
- `"3 Peak Spark"`
- `"Normal Spark"`
- `"Combined Spark"`
- `"Arclike Spark"`
- `"Cleaning"`

#### `seq.source.clean` (dropdown options)
- `"Cleaning"`
- `"High Voltage Spark"`
- `"AD OFFSET"`
- `"ITG OFFSET"`
- `"MAIN OFFSET"`
- `"NOISE TEST"`

#### `level_out_information.monitor_element.element` (dropdown options with auto-fill values)
| Element | Auto-fill value for `monitor_element.value` |
|---------|---------------------------------------------|
| `"None"` | `""` (empty) |
| `"FE"` | `"273.0"` |
| `"C"` | `"193.0"` |
| `"Si"` | `"212.4"` |
| `"MN"` | `"293.3"` |
| `"P"` | `"178.3"` |
| `"S"` | `"180.7"` |
| `"V"` | `"311.0"` |
| `"CR"` | `"267.7"` or `"298.9"` (duplicate entry) |

**Note:** When `monitor_element.element` changes, the frontend automatically fills `monitor_element.value` with the corresponding value. User can override manually.

#### `level_out_information.monitor_element.option1` and `option2` (dropdown options)
- `"None"`
- `"FE"`
- `"C"`
- `"Si"`
- `"MN"`
- `"P"`
- `"S"`
- `"V"`
- `"CR"`

### Example Payloads

**Default Values:**
```json
{
  "analytical_group": "LAS 2023",
  "analytical_method": "integration Mode",
  "seq": {
    "purge": {
      "seq1": "3"
    },
    "source": {
      "seq1": "3 Peak Spark",
      "seq2": "Normal Spark",
      "seq3": "Lamp",
      "clean": "Cleaning"
    },
    "preburn": {
      "seq1": "100",
      "seq2": "300",
      "seq3": "0",
      "clean": "Pulse"
    },
    "integ": {
      "seq1": "300",
      "seq2": "23",
      "seq3": "0",
      "clean": "Pulse"
    },
    "clean": {
      "value": "0",
      "unit": "Pulse"
    }
  },
  "level_out_information": {
    "monitor_element": {
      "element": "FE",
      "value": "273.0",
      "option1": "None",
      "option2": "None"
    },
    "h_level_percent": ["0", "0", "0", "0", "0", "0", "0", "0", "0"],
    "l_level_percent": ["20", "20", "0", "0", "0", "0", "0", "0", "0"]
  }
}
```

**Modified Example (Different Dropdown Selections):**
```json
{
  "analytical_group": "SS 2023",
  "analytical_method": "PDA + Integration",
  "seq": {
    "purge": {
      "seq1": "5"
    },
    "source": {
      "seq1": "Normal Spark",
      "seq2": "Combined Spark",
      "seq3": "3 Peak Spark",
      "clean": "High Voltage Spark"
    },
    "preburn": {
      "seq1": "150",
      "seq2": "400",
      "seq3": "50",
      "clean": "Pulse"
    },
    "integ": {
      "seq1": "350",
      "seq2": "30",
      "seq3": "10",
      "clean": "Pulse"
    },
    "clean": {
      "value": "5",
      "unit": "Pulse"
    }
  },
  "level_out_information": {
    "monitor_element": {
      "element": "C",
      "value": "193.0",
      "option1": "FE",
      "option2": "Si"
    },
    "h_level_percent": ["10", "10", "5", "5", "0", "0", "0", "0", "0"],
    "l_level_percent": ["15", "15", "5", "5", "0", "0", "0", "0", "0"]
  }
}
```

---

## 2. Attenuator Information Page

### Endpoint Suggestion
`POST /api/attenuator-information`

### Schema Structure

```json
{
  "analytical_group": "string",
  "page": "string (literal: 'attenuator_information')",
  "left_table": [
    {
      "element": "string",
      "ele_value": "string (numeric)",
      "att_value": "string (numeric)"
    }
  ],
  "right_table": [
    {
      "element": "string",
      "ele_value": "string (numeric)",
      "att_value": "string (numeric)"
    }
  ]
}
```

### Field Details

#### Left Table (Pre-filled Elements)
Default 16 rows with these elements:
- FE (273.0, ATT: 77)
- C (193.0, ATT: 49)
- SI (212.4, ATT: 41)
- MN (293.3, ATT: 40)
- P (178.3, ATT: 81)
- S (180.7, ATT: 71)
- V (311.0, ATT: 44)
- CR (267.7, ATT: 26)
- CR (298.9, ATT: 0)
- MO (202.0, ATT: 46)
- MO (277.5, ATT: 0)
- NI (231.6, ATT: 93)
- NI (227.7, ATT: 0)
- AL (394.4, ATT: 26)
- CU (224.2, ATT: 61)
- TI (337.2, ATT: 93)

#### Right Table (Pre-filled + Empty Rows)
Default includes:
- W (220.4, ATT: 76)
- B (182.6, ATT: 90)
- NB (319.5, ATT: 54)
- CA (396.8, ATT: 48)
- CO (258.0, ATT: 47)
- SN (189.9, ATT: 62)
- N (174.5+2, ATT: 96)
- PB (405.7, ATT: 82)
- RH (421.8, ATT: 0)
- Plus ~16 empty rows (all fields empty or "0")

**Note:** Only `att_value` is user-editable for pre-filled rows. Empty rows allow full editing (element name, ele_value, att_value).

### Dropdown Interaction
**No dropdowns on this page.** All fields are text inputs or labels. Users can only edit ATT values for existing elements and add new elements in empty rows.

### Example Payload

```json
{
  "analytical_group": "LAS 2023",
  "page": "attenuator_information",
  "left_table": [
    {"element": "FE", "ele_value": "273.0", "att_value": "77"},
    {"element": "C", "ele_value": "193.0", "att_value": "49"},
    {"element": "SI", "ele_value": "212.4", "att_value": "41"},
    {"element": "MN", "ele_value": "293.3", "att_value": "40"},
    {"element": "P", "ele_value": "178.3", "att_value": "81"},
    {"element": "S", "ele_value": "180.7", "att_value": "71"},
    {"element": "V", "ele_value": "311.0", "att_value": "44"},
    {"element": "CR", "ele_value": "267.7", "att_value": "26"},
    {"element": "CR", "ele_value": "298.9", "att_value": "0"},
    {"element": "MO", "ele_value": "202.0", "att_value": "46"},
    {"element": "MO", "ele_value": "277.5", "att_value": "0"},
    {"element": "NI", "ele_value": "231.6", "att_value": "93"},
    {"element": "NI", "ele_value": "227.7", "att_value": "0"},
    {"element": "AL", "ele_value": "394.4", "att_value": "26"},
    {"element": "CU", "ele_value": "224.2", "att_value": "61"},
    {"element": "TI", "ele_value": "337.2", "att_value": "93"}
  ],
  "right_table": [
    {"element": "W", "ele_value": "220.4", "att_value": "76"},
    {"element": "B", "ele_value": "182.6", "att_value": "90"},
    {"element": "NB", "ele_value": "319.5", "att_value": "54"},
    {"element": "CA", "ele_value": "396.8", "att_value": "48"},
    {"element": "CO", "ele_value": "258.0", "att_value": "47"},
    {"element": "SN", "ele_value": "189.9", "att_value": "62"},
    {"element": "N", "ele_value": "174.5+2", "att_value": "96"},
    {"element": "PB", "ele_value": "405.7", "att_value": "82"},
    {"element": "RH", "ele_value": "421.8", "att_value": "0"},
    {"element": "", "ele_value": "", "att_value": "0"},
    {"element": "", "ele_value": "", "att_value": "0"}
    // ... more empty rows
  ]
}
```

---

## 3. Element Information Page

### Endpoint Suggestion
`POST /api/element-information`

### Schema Structure

```json
{
  "analytical_group": "string",
  "page": "string (literal: 'element_information')",
  "ch_value": "string (fixed: '22')",
  "elements": [
    {
      "ele_name": "string",
      "analytical_range_min": "string (numeric)",
      "analytical_range_max": "string (numeric)",
      "asterisk": "string",
      "chemic_ele": "string",
      "element": "string"
    }
  ]
}
```

### Field Details

#### Default Elements (23 rows)
| ele_name | range_min | range_max | asterisk | chemic_ele | element |
|----------|-----------|-----------|----------|------------|---------|
| Fe | .00000 | 100.00 | * | Fe | Fe |
| C | .00000 | 100.00 | * | C | C |
| Si | .00000 | 100.00 | * | Si | Si |
| Mn | .00000 | 100.00 | * | Mn | Mn |
| P | .00000 | 100.00 | * | P | P |
| S | .00000 | 100.00 | * | S | S |
| Cr | .00000 | 100.00 | * | Cr | Cr |
| Ni | .00000 | 100.00 | * | Ni | Ni |
| Mo | .00000 | 100.00 | * | Mo | Mo |
| Cu | .00000 | 100.00 | * | Cu | Cu |
| V | .00000 | 100.00 | * | V | V |
| Ti | .00000 | 100.00 | * | Ti | Ti |
| W | .00000 | 100.00 | * | W | W |
| B | .00000 | 100.00 | * | B | B |
| Nb | .00000 | 100.00 | * | Nb | Nb |
| Ca | .00000 | 100.00 | * | Ca | Ca |
| Co | .00000 | 100.00 | * | Co | Co |
| Sn | .00000 | 100.00 | * | Sn | Sn |
| N | .00000 | 100.00 | * | N | N |
| Pb | .00000 | 100.00 | * | Pb | Pb |
| Al | .00000 | 100.00 | * | Al | AL |
| CE | .00000 | .00000 | * | (empty) | (empty) |
| (empty) | .00000 | .00000 | (empty) | (empty) | (empty) |

**Note:** All fields are text entries—fully editable by the user. Users can add, modify, or delete elements.

### Dropdown Interaction
**No dropdowns on this page.** All fields are text inputs.

### Example Payload

```json
{
  "analytical_group": "LAS 2023",
  "page": "element_information",
  "ch_value": "22",
  "elements": [
    {
      "ele_name": "Fe",
      "analytical_range_min": ".00000",
      "analytical_range_max": "100.00",
      "asterisk": "*",
      "chemic_ele": "Fe",
      "element": "Fe"
    },
    {
      "ele_name": "C",
      "analytical_range_min": ".00000",
      "analytical_range_max": "100.00",
      "asterisk": "*",
      "chemic_ele": "C",
      "element": "C"
    },
    {
      "ele_name": "Si",
      "analytical_range_min": ".00000",
      "analytical_range_max": "100.00",
      "asterisk": "*",
      "chemic_ele": "Si",
      "element": "Si"
    }
    // ... 20 more elements
  ]
}
```

---

## 4. Channel Information Page

### Endpoint Suggestion
`POST /api/channel-information`

### Schema Structure

```json
{
  "analytical_group": "string",
  "page": "string (literal: 'channel_information')",
  "channels": [
    {
      "ele_name": "string",
      "w_lengh": "string (numeric)",
      "seq": "string (numeric)",
      "w_no": "string",
      "interval_element": "string",
      "interval_value": "string (numeric)"
    }
  ]
}
```

### Field Details

#### Default Channels (22 rows)
| ele_name | w_lengh | seq | w_no | interval_element | interval_value |
|----------|---------|-----|------|------------------|----------------|
| Fe | 396.8 | 1 | (empty) | FE | 273.0 |
| C | 193.0 | 2 | (empty) | FE | 273.0 |
| Si | 212.4 | 2 | (empty) | FE | 273.0 |
| Mn | 293.3 | 2 | (empty) | FE | 273.0 |
| P | 178.3 | 1 | (empty) | FE | 273.0 |
| S | 180.7 | 1 | (empty) | FE | 273.0 |
| Cr | 267.7 | 2 | (empty) | FE | 273.0 |
| Ni | 231.6 | 2 | (empty) | FE | 273.0 |
| Mo | 202.0 | 2 | (empty) | FE | 273.0 |
| Cu | 224.2 | 2 | (empty) | FE | 273.0 |
| V | 311.0 | 2 | (empty) | FE | 273.0 |
| Ti | 337.2 | 1 | (empty) | FE | 273.0 |
| W | 220.4 | 2 | (empty) | FE | 273.0 |
| B | 182.6 | 1 | (empty) | FE | 273.0 |
| Nb | 319.5 | 2 | (empty) | FE | 273.0 |
| Ca | 396.8 | 1 | (empty) | FE | 273.0 |
| Co | 258.0 | 2 | (empty) | FE | 273.0 |
| Sn | 189.9 | 2 | (empty) | FE | 273.0 |
| N | 174.5+2 | 2 | (empty) | FE | 273.0 |
| Pb | 405.7 | 1 | (empty) | FE | 273.0 |
| Al | 394.4 | 1 | (empty) | FE | 273.0 |
| CE | (empty) | 1 | (empty) | FE | 273.0 |

**Note:** All fields are text entries—fully editable. Users can add, modify, or delete channels.

### Dropdown Interaction
**No dropdowns on this page.** All fields are text inputs.

### Example Payload

```json
{
  "analytical_group": "LAS 2023",
  "page": "channel_information",
  "channels": [
    {
      "ele_name": "Fe",
      "w_lengh": "396.8",
      "seq": "1",
      "w_no": "",
      "interval_element": "FE",
      "interval_value": "273.0"
    },
    {
      "ele_name": "C",
      "w_lengh": "193.0",
      "seq": "2",
      "w_no": "",
      "interval_element": "FE",
      "interval_value": "273.0"
    },
    {
      "ele_name": "Si",
      "w_lengh": "212.4",
      "seq": "2",
      "w_no": "",
      "interval_element": "FE",
      "interval_value": "273.0"
    }
    // ... 19 more channels
  ]
}
```

---

## 5. Integration Notes

### Data Flow Summary
1. **User navigates pages**: Main App → Analytical Condition → Attenuator Information → Element Information → Channel Information
2. **Data persistence**: 
   - In-memory via singleton `DataManager` (utils/data_manager.py)
   - Only Analytical Condition and Attenuator pages currently save/load via DataManager
   - Element and Channel pages collect JSON but don't persist (TODO in code)
3. **Upload trigger**: Each page has an "Upload" button that:
   - Calls `collect_form_data()` to gather current form state
   - Converts to JSON
   - Prints to console (backend POST not implemented yet)
   - Shows preview in messagebox

### Dropdown-Driven Schema Changes

#### Page 1: Analytical Condition
**Dropdowns that affect JSON:**
- `analytical_method`: Changes top-level field
- `source.seq1/seq2/seq3/clean`: Changes nested seq.source object
- `monitor_element.element`: Changes element field AND auto-fills value field
- `monitor_element.option1/option2`: Changes additional monitor options

**Example:**
```javascript
// User selects monitor_element = "C"
// Frontend auto-fills monitor_value = "193.0"
{
  "level_out_information": {
    "monitor_element": {
      "element": "C",          // from dropdown
      "value": "193.0",        // auto-filled
      "option1": "None",
      "option2": "None"
    }
  }
}
```

#### Pages 2-4: No Dropdowns
- Attenuator, Element, and Channel pages use text inputs only
- Schema changes only when user manually edits fields

### Backend Recommendations

1. **Type Conversion**: All numeric fields are sent as strings. Convert to appropriate types:
   ```python
   # Example Python backend
   purge_seq1 = int(data['seq']['purge']['seq1'])
   monitor_value = float(data['level_out_information']['monitor_element']['value'])
   ```

2. **Validation**: 
   - Validate enum values against allowed options (see dropdown sections)
   - Check numeric string formats before conversion
   - Handle empty strings for optional fields

3. **Endpoints Structure**:
   ```
   POST /api/analytical-condition
   POST /api/attenuator-information
   POST /api/element-information
   POST /api/channel-information
   ```

4. **Response Format** (suggestion):
   ```json
   {
     "success": true,
     "message": "Data saved successfully",
     "data": {
       "id": "generated-id",
       "analytical_group": "LAS 2023",
       "timestamp": "2025-11-07T10:30:00Z"
     }
   }
   ```

5. **Error Handling**:
   ```json
   {
     "success": false,
     "error": "Invalid analytical_method value",
     "field": "analytical_method",
     "received": "InvalidMode",
     "allowed": ["integration Mode", "PDA + Integration"]
   }
   ```

### Analytical Groups (Available across all pages)
Common analytical groups that appear in the selection list:
- LAS 2023
- SS 2023
- LA 2021
- SS - 2022
- FERR 2022
- TOLL STEEL2021
- FERR 2020
- SS 2021
- LA 2021 S
- GLOBAL CAL
- LA 2020
- LA-WITH HI MN
- SS WITH HI MN
- Cast
- LOW-ALLOY-HS
- NI 2017
- INCONEL 17
- MONEL 17
- TEST GROUP
- LA 2021 WITH CA
- TEST LAS
- 26-11-22
- FERR 2023
- GHHaj

---

## Quick Reference: All Dropdown Enums

### Analytical Method
```json
["integration Mode", "PDA + Integration"]
```

### Source SEQ1
```json
["3 Peak Spark", "Normal Spark", "Combined Spark", "Arclike Spark", "Cleaning", "High Voltage Spark"]
```

### Source SEQ2
```json
["Normal Spark", "Combined Spark", "Arclike Spark", "Cleaning", "High Voltage Spark", "AD OFFSET"]
```

### Source SEQ3
```json
["Lamp", "3 Peak Spark", "Normal Spark", "Combined Spark", "Arclike Spark", "Cleaning"]
```

### Source Clean
```json
["Cleaning", "High Voltage Spark", "AD OFFSET", "ITG OFFSET", "MAIN OFFSET", "NOISE TEST"]
```

### Monitor Elements (with auto-fill mapping)
```json
{
  "None": "",
  "FE": "273.0",
  "C": "193.0",
  "Si": "212.4",
  "MN": "293.3",
  "P": "178.3",
  "S": "180.7",
  "V": "311.0",
  "CR": "267.7"
}
```

### Monitor Options 1 & 2
```json
["None", "FE", "C", "Si", "MN", "P", "S", "V", "CR"]
```

---

**Document Version:** 1.0  
**Last Updated:** November 7, 2025  
**Frontend Version:** Based on current codebase state
