# Dropdown Options Reference - Quick Lookup

This document provides a quick reference for all dropdown fields and their allowed values.

---

## Analytical Condition Page Dropdowns

### 1. Analytical Method
**Field:** `analytical_method`  
**Type:** Dropdown (2 options)

```
┌─────────────────────────────────┐
│ Dropdown Options:               │
├─────────────────────────────────┤
│ • integration Mode              │
│ • PDA + Integration             │
└─────────────────────────────────┘
```

**Example JSON:**
```json
{"analytical_method": "integration Mode"}
{"analytical_method": "PDA + Integration"}
```

---

### 2. Source SEQ1
**Field:** `seq.source.seq1`  
**Type:** Dropdown (6 options)

```
┌─────────────────────────────────┐
│ Dropdown Options:               │
├─────────────────────────────────┤
│ • 3 Peak Spark                  │
│ • Normal Spark                  │
│ • Combined Spark                │
│ • Arclike Spark                 │
│ • Cleaning                      │
│ • High Voltage Spark            │
└─────────────────────────────────┘
```

**Default:** `"3 Peak Spark"`

---

### 3. Source SEQ2
**Field:** `seq.source.seq2`  
**Type:** Dropdown (6 options)

```
┌─────────────────────────────────┐
│ Dropdown Options:               │
├─────────────────────────────────┤
│ • Normal Spark                  │
│ • Combined Spark                │
│ • Arclike Spark                 │
│ • Cleaning                      │
│ • High Voltage Spark            │
│ • AD OFFSET                     │
└─────────────────────────────────┘
```

**Default:** `"Normal Spark"`

---

### 4. Source SEQ3
**Field:** `seq.source.seq3`  
**Type:** Dropdown (6 options)

```
┌─────────────────────────────────┐
│ Dropdown Options:               │
├─────────────────────────────────┤
│ • Lamp                          │
│ • 3 Peak Spark                  │
│ • Normal Spark                  │
│ • Combined Spark                │
│ • Arclike Spark                 │
│ • Cleaning                      │
└─────────────────────────────────┘
```

**Default:** `"Lamp"`

---

### 5. Source Clean
**Field:** `seq.source.clean`  
**Type:** Dropdown (6 options)

```
┌─────────────────────────────────┐
│ Dropdown Options:               │
├─────────────────────────────────┤
│ • Cleaning                      │
│ • High Voltage Spark            │
│ • AD OFFSET                     │
│ • ITG OFFSET                    │
│ • MAIN OFFSET                   │
│ • NOISE TEST                    │
└─────────────────────────────────┘
```

**Default:** `"Cleaning"`

---

### 6. Monitor Element ⚠️ AUTO-FILL
**Field:** `level_out_information.monitor_element.element`  
**Type:** Dropdown (9 options) **WITH AUTO-FILL BEHAVIOR**

```
┌─────────────────────────────────────────────────────────┐
│ Element  │  Auto-fills value field with:                │
├──────────┼──────────────────────────────────────────────┤
│ None     │  ""  (empty string)                          │
│ FE       │  "273.0"  ← DEFAULT                          │
│ C        │  "193.0"                                     │
│ Si       │  "212.4"                                     │
│ MN       │  "293.3"                                     │
│ P        │  "178.3"                                     │
│ S        │  "180.7"                                     │
│ V        │  "311.0"                                     │
│ CR       │  "267.7"  (or "298.9" - duplicate entry)    │
└──────────┴──────────────────────────────────────────────┘
```

**Behavior:**
- When user selects element, `value` field is **automatically populated**
- User can override the auto-filled value manually
- Backend receives final value (auto-filled OR user-edited)

**Example JSON transformations:**
```json
// User selects "FE"
{
  "monitor_element": {
    "element": "FE",
    "value": "273.0"  // ← Auto-filled
  }
}

// User selects "C"
{
  "monitor_element": {
    "element": "C",
    "value": "193.0"  // ← Auto-filled
  }
}

// User selects "C" but manually edits value to "200.0"
{
  "monitor_element": {
    "element": "C",
    "value": "200.0"  // ← User override
  }
}
```

---

### 7. Monitor Element Option 1
**Field:** `level_out_information.monitor_element.option1`  
**Type:** Dropdown (9 options)

```
┌─────────────────────────────────┐
│ Dropdown Options:               │
├─────────────────────────────────┤
│ • None                          │
│ • FE                            │
│ • C                             │
│ • Si                            │
│ • MN                            │
│ • P                             │
│ • S                             │
│ • V                             │
│ • CR                            │
└─────────────────────────────────┘
```

**Default:** `"None"`  
**Behavior:** No auto-fill, just stores selected value

---

### 8. Monitor Element Option 2
**Field:** `level_out_information.monitor_element.option2`  
**Type:** Dropdown (9 options)

```
┌─────────────────────────────────┐
│ Dropdown Options:               │
├─────────────────────────────────┤
│ • None                          │
│ • FE                            │
│ • C                             │
│ • Si                            │
│ • MN                            │
│ • P                             │
│ • S                             │
│ • V                             │
│ • CR                            │
└─────────────────────────────────┘
```

**Default:** `"None"`  
**Behavior:** No auto-fill, just stores selected value

---

## Other Pages

### Attenuator Information Page
**Dropdowns:** None  
**Fields:** All text inputs (element name, ele_value, att_value)

### Element Information Page
**Dropdowns:** None  
**Fields:** All text inputs (ele_name, ranges, asterisk, etc.)

### Channel Information Page
**Dropdowns:** None  
**Fields:** All text inputs (ele_name, w_lengh, seq, etc.)

---

## Dropdown Comparison Matrix

| Dropdown | Location | Options Count | Auto-fill? | Default |
|----------|----------|---------------|------------|---------|
| analytical_method | Top level | 2 | No | "integration Mode" |
| source.seq1 | SEQ section | 6 | No | "3 Peak Spark" |
| source.seq2 | SEQ section | 6 | No | "Normal Spark" |
| source.seq3 | SEQ section | 6 | No | "Lamp" |
| source.clean | SEQ section | 6 | No | "Cleaning" |
| monitor_element.element | Level Out | 9 | **YES** | "FE" → "273.0" |
| monitor_element.option1 | Level Out | 9 | No | "None" |
| monitor_element.option2 | Level Out | 9 | No | "None" |

---

## Backend Validation Pseudocode

```python
# Allowed values for each dropdown
ALLOWED_VALUES = {
    "analytical_method": [
        "integration Mode",
        "PDA + Integration"
    ],
    "source_seq1": [
        "3 Peak Spark",
        "Normal Spark",
        "Combined Spark",
        "Arclike Spark",
        "Cleaning",
        "High Voltage Spark"
    ],
    "source_seq2": [
        "Normal Spark",
        "Combined Spark",
        "Arclike Spark",
        "Cleaning",
        "High Voltage Spark",
        "AD OFFSET"
    ],
    "source_seq3": [
        "Lamp",
        "3 Peak Spark",
        "Normal Spark",
        "Combined Spark",
        "Arclike Spark",
        "Cleaning"
    ],
    "source_clean": [
        "Cleaning",
        "High Voltage Spark",
        "AD OFFSET",
        "ITG OFFSET",
        "MAIN OFFSET",
        "NOISE TEST"
    ],
    "monitor_element": [
        "None",
        "FE",
        "C",
        "Si",
        "MN",
        "P",
        "S",
        "V",
        "CR"
    ]
}

def validate_dropdown(field_name, value):
    """Validate dropdown value against allowed options"""
    if value not in ALLOWED_VALUES[field_name]:
        raise ValidationError(
            f"Invalid {field_name}: '{value}'. "
            f"Allowed: {ALLOWED_VALUES[field_name]}"
        )
```

---

## Quick Test Scenarios

### Scenario 1: Default State
User doesn't change any dropdowns. Backend receives:
```json
{
  "analytical_method": "integration Mode",
  "seq": {
    "source": {
      "seq1": "3 Peak Spark",
      "seq2": "Normal Spark",
      "seq3": "Lamp",
      "clean": "Cleaning"
    }
  },
  "level_out_information": {
    "monitor_element": {
      "element": "FE",
      "value": "273.0",
      "option1": "None",
      "option2": "None"
    }
  }
}
```

### Scenario 2: All Dropdowns Changed
User selects different options:
```json
{
  "analytical_method": "PDA + Integration",
  "seq": {
    "source": {
      "seq1": "Normal Spark",
      "seq2": "AD OFFSET",
      "seq3": "3 Peak Spark",
      "clean": "NOISE TEST"
    }
  },
  "level_out_information": {
    "monitor_element": {
      "element": "C",
      "value": "193.0",  // Auto-filled
      "option1": "FE",
      "option2": "Si"
    }
  }
}
```

### Scenario 3: Monitor Element Override
User selects "FE" (auto-fills "273.0") then edits to "280.0":
```json
{
  "level_out_information": {
    "monitor_element": {
      "element": "FE",
      "value": "280.0"  // User edited!
    }
  }
}
```

**Backend must accept "280.0" even though auto-fill would be "273.0"**

---

## API Testing Commands

```bash
# Test with default dropdown values
curl -X POST http://localhost:5000/api/analytical-condition \
  -H "Content-Type: application/json" \
  -d @examples/analytical_condition_default.json

# Test with modified dropdown values
curl -X POST http://localhost:5000/api/analytical-condition \
  -H "Content-Type: application/json" \
  -d @examples/analytical_condition_modified.json

# Test with invalid dropdown value (should fail)
curl -X POST http://localhost:5000/api/analytical-condition \
  -H "Content-Type: application/json" \
  -d '{"analytical_method":"INVALID_MODE"}'
```

**Expected error response:**
```json
{
  "success": false,
  "error": "Validation failed",
  "field": "analytical_method",
  "received": "INVALID_MODE",
  "allowed": ["integration Mode", "PDA + Integration"]
}
```
