# Master Schema Comparison - All Pages

Quick visual comparison of all 4 page schemas side-by-side.

---

## High-Level Comparison

| Feature | Analytical Condition | Attenuator Info | Element Info | Channel Info |
|---------|---------------------|-----------------|--------------|--------------|
| **Endpoint** | `/api/analytical-condition` | `/api/attenuator-information` | `/api/element-information` | `/api/channel-information` |
| **Has Dropdowns?** | ✅ YES (8 dropdowns) | ❌ NO | ❌ NO | ❌ NO |
| **Auto-fill Behavior?** | ✅ YES (monitor element) | ❌ NO | ❌ NO | ❌ NO |
| **Data Structure** | Nested objects | 2 arrays | 1 array | 1 array |
| **Complexity** | HIGH | MEDIUM | MEDIUM | MEDIUM |
| **Field Count** | ~28 fields | 3 fields × N rows | 6 fields × N rows | 6 fields × N rows |
| **Default Rows** | N/A (fixed structure) | Left: 16, Right: 25 | 23 | 22 |
| **User-Editable Rows** | N/A | Right table empties | All rows | All rows |
| **Requires Validation** | Enum validation | String format | String format | String format |
| **DataManager Support** | ✅ YES | ✅ YES | ⚠️ TODO | ⚠️ TODO |

---

## Schema Structures Side-by-Side

### Page 1: Analytical Condition
```
analytical_condition/
├── analytical_group         [string]
├── analytical_method        [enum: 2 options] ← DROPDOWN
└── seq/
    ├── purge/
    │   └── seq1             [numeric string]
    ├── source/
    │   ├── seq1             [enum: 6 options] ← DROPDOWN
    │   ├── seq2             [enum: 6 options] ← DROPDOWN
    │   ├── seq3             [enum: 6 options] ← DROPDOWN
    │   └── clean            [enum: 6 options] ← DROPDOWN
    ├── preburn/
    │   ├── seq1             [numeric string]
    │   ├── seq2             [numeric string]
    │   ├── seq3             [numeric string]
    │   └── clean            [literal: "Pulse"]
    ├── integ/
    │   ├── seq1             [numeric string]
    │   ├── seq2             [numeric string]
    │   ├── seq3             [numeric string]
    │   └── clean            [literal: "Pulse"]
    └── clean/
        ├── value            [numeric string]
        └── unit             [literal: "Pulse"]
└── level_out_information/
    ├── monitor_element/
    │   ├── element          [enum: 9 options] ← DROPDOWN + AUTO-FILL
    │   ├── value            [numeric string] ← AUTO-FILLED
    │   ├── option1          [enum: 9 options] ← DROPDOWN
    │   └── option2          [enum: 9 options] ← DROPDOWN
    ├── h_level_percent      [array of 9 numeric strings]
    └── l_level_percent      [array of 9 numeric strings]
```

### Page 2: Attenuator Information
```
attenuator_information/
├── analytical_group         [string]
├── page                     [literal: "attenuator_information"]
├── left_table               [array]
│   └── [0..N]
│       ├── element          [string]
│       ├── ele_value        [numeric string]
│       └── att_value        [numeric string]
└── right_table              [array]
    └── [0..N]
        ├── element          [string]
        ├── ele_value        [numeric string]
        └── att_value        [numeric string]
```

### Page 3: Element Information
```
element_information/
├── analytical_group         [string]
├── page                     [literal: "element_information"]
├── ch_value                 [string: typically "22"]
└── elements                 [array]
    └── [0..N]
        ├── ele_name         [string]
        ├── analytical_range_min [numeric string]
        ├── analytical_range_max [numeric string]
        ├── asterisk         [string]
        ├── chemic_ele       [string]
        └── element          [string]
```

### Page 4: Channel Information
```
channel_information/
├── analytical_group         [string]
├── page                     [literal: "channel_information"]
└── channels                 [array]
    └── [0..N]
        ├── ele_name         [string]
        ├── w_lengh          [numeric string]
        ├── seq              [numeric string]
        ├── w_no             [string]
        ├── interval_element [string]
        └── interval_value   [numeric string]
```

---

## Dropdown Matrix (Complete)

| Page | Field Path | Options | Default | Auto-fill? |
|------|-----------|---------|---------|-----------|
| **Analytical Condition** | `analytical_method` | 2 | integration Mode | No |
| **Analytical Condition** | `seq.source.seq1` | 6 | 3 Peak Spark | No |
| **Analytical Condition** | `seq.source.seq2` | 6 | Normal Spark | No |
| **Analytical Condition** | `seq.source.seq3` | 6 | Lamp | No |
| **Analytical Condition** | `seq.source.clean` | 6 | Cleaning | No |
| **Analytical Condition** | `level_out_information.monitor_element.element` | 9 | FE | **YES → value** |
| **Analytical Condition** | `level_out_information.monitor_element.option1` | 9 | None | No |
| **Analytical Condition** | `level_out_information.monitor_element.option2` | 9 | None | No |
| Attenuator Info | - | - | - | - |
| Element Info | - | - | - | - |
| Channel Info | - | - | - | - |

---

## Example Payloads (Minimal)

### Analytical Condition (Minimal Required Fields)
```json
{
  "analytical_group": "LAS 2023",
  "analytical_method": "integration Mode",
  "seq": {
    "purge": {"seq1": "3"},
    "source": {"seq1": "3 Peak Spark", "seq2": "Normal Spark", "seq3": "Lamp", "clean": "Cleaning"},
    "preburn": {"seq1": "100", "seq2": "300", "seq3": "0", "clean": "Pulse"},
    "integ": {"seq1": "300", "seq2": "23", "seq3": "0", "clean": "Pulse"},
    "clean": {"value": "0", "unit": "Pulse"}
  },
  "level_out_information": {
    "monitor_element": {"element": "FE", "value": "273.0", "option1": "None", "option2": "None"},
    "h_level_percent": ["0","0","0","0","0","0","0","0","0"],
    "l_level_percent": ["20","20","0","0","0","0","0","0","0"]
  }
}
```

### Attenuator Information (Minimal)
```json
{
  "analytical_group": "LAS 2023",
  "page": "attenuator_information",
  "left_table": [
    {"element": "FE", "ele_value": "273.0", "att_value": "77"}
  ],
  "right_table": [
    {"element": "W", "ele_value": "220.4", "att_value": "76"}
  ]
}
```

### Element Information (Minimal)
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
    }
  ]
}
```

### Channel Information (Minimal)
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
    }
  ]
}
```

---

## JSON Size Comparison (Typical Payloads)

| Page | Typical Size | Fields | Arrays | Nested Levels |
|------|-------------|--------|--------|---------------|
| Analytical Condition | ~1.5 KB | 28 | 2 (9 items each) | 3 levels |
| Attenuator Info | ~2-3 KB | 3 × 25-40 rows | 2 | 2 levels |
| Element Info | ~2-3 KB | 6 × 23 rows | 1 | 2 levels |
| Channel Info | ~2-3 KB | 6 × 22 rows | 1 | 2 levels |

---

## Validation Complexity

| Page | Enum Validation | Format Validation | Array Validation | Overall |
|------|----------------|-------------------|------------------|---------|
| Analytical Condition | HIGH (8 enums) | MEDIUM (numeric strings) | LOW (fixed 9 items) | **HIGH** |
| Attenuator Info | NONE | MEDIUM (numeric strings) | HIGH (variable length) | **MEDIUM** |
| Element Info | NONE | MEDIUM (numeric strings) | HIGH (variable length) | **MEDIUM** |
| Channel Info | NONE | MEDIUM (numeric strings) | HIGH (variable length) | **MEDIUM** |

---

## Backend Endpoint Summary

```
POST /api/analytical-condition
├── Validates: 8 enum fields + numeric strings
├── Converts: 13+ numeric strings to int/float
├── Returns: {success, message, data: {id, analytical_group, timestamp}}
└── Error: {success: false, error, field, received, allowed}

POST /api/attenuator-information
├── Validates: Numeric string formats
├── Converts: ele_value, att_value to float/int
├── Accepts: Variable-length arrays
└── Returns: Same format as above

POST /api/element-information
├── Validates: Numeric string formats
├── Converts: analytical_range_min/max to float
├── Accepts: Variable-length array
└── Returns: Same format as above

POST /api/channel-information
├── Validates: Numeric string formats
├── Converts: w_lengh, seq, interval_value to appropriate types
├── Accepts: Variable-length array
└── Returns: Same format as above
```

---

## Testing Priority

### 1. Analytical Condition (HIGHEST)
- Most complex schema
- Most dropdown validations
- Auto-fill behavior to test
- **Test scenarios:**
  - Default values
  - All dropdowns changed
  - Monitor element auto-fill
  - Monitor element override

### 2. Attenuator Information (MEDIUM)
- Two arrays to handle
- Simpler structure
- **Test scenarios:**
  - Standard full payload
  - Empty right table rows
  - User-added elements

### 3. Element Information (MEDIUM)
- Single array
- 6 fields per item
- **Test scenarios:**
  - Standard 23 elements
  - Modified ranges
  - Added/removed elements

### 4. Channel Information (MEDIUM)
- Single array
- 6 fields per item
- **Test scenarios:**
  - Standard 22 channels
  - Modified SEQ values
  - Added/removed channels

---

## Quick Decision Matrix

**Need to validate dropdown choices?**
- YES → Use Analytical Condition schema
- NO → Use other schemas

**Need to handle auto-fill?**
- YES → Monitor element.element → auto-fills element.value
- NO → Direct value storage

**Need variable-length arrays?**
- YES → Attenuator, Element, Channel pages
- NO → Analytical Condition (fixed structure)

**Need nested validation?**
- YES → Analytical Condition (3 levels deep)
- NO → Others (2 levels max)

---

## File Reference Quick Guide

```
📁 Documentation Files:
├── BACKEND_SCHEMAS.md         ← START HERE (comprehensive)
├── DROPDOWN_REFERENCE.md      ← Dropdown quick lookup
├── README_BACKEND.md          ← Implementation guide
├── SCHEMA_SUMMARY.md          ← Overview summary
└── MASTER_SCHEMA_COMPARISON.md ← This file (visual comparison)

📁 Schema Files:
└── schemas/
    ├── analytical_condition_schema.json
    ├── attenuator_information_schema.json
    ├── element_information_schema.json
    └── channel_information_schema.json

📁 Example Files:
└── examples/
    ├── analytical_condition_default.json
    ├── analytical_condition_modified.json
    ├── attenuator_information_example.json
    ├── element_information_example.json
    └── channel_information_example.json
```

---

**Use this file for:** Quick side-by-side comparison, endpoint planning, testing prioritization
