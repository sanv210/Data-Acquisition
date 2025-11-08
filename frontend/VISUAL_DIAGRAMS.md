# Visual Schema Flow Diagrams

ASCII diagrams showing how data flows from UI to JSON for each page.

---

## Analytical Condition Page - Data Flow

```
┌──────────────────────────────────────────────────────────────────────┐
│                    ANALYTICAL CONDITION PAGE                          │
│                                                                       │
│  ┌─────────────────────┐                                             │
│  │ Analytical Method   │────────┐                                    │
│  │ [Dropdown: 2 opts]  │        │                                    │
│  └─────────────────────┘        │                                    │
│                                  │                                    │
│  ┌──────────────────────────────▼───────────────────────┐            │
│  │              SEQ SECTION                             │            │
│  │  ┌──────────────┐  ┌──────────────┐                 │            │
│  │  │ Source SEQ1  │  │ Source SEQ2  │                 │            │
│  │  │ [Dropdown:6] │  │ [Dropdown:6] │                 │            │
│  │  └──────────────┘  └──────────────┘                 │            │
│  │                                                      │            │
│  │  ┌──────────────┐  ┌──────────────┐                 │            │
│  │  │ Source SEQ3  │  │ Source Clean │                 │            │
│  │  │ [Dropdown:6] │  │ [Dropdown:6] │                 │            │
│  │  └──────────────┘  └──────────────┘                 │            │
│  │                                                      │            │
│  │  Purge, Preburn, Integ fields [Numeric Inputs]     │            │
│  └──────────────────────────────────────────────────────┘            │
│                                  │                                    │
│  ┌──────────────────────────────▼───────────────────────┐            │
│  │       LEVEL OUT INFORMATION                          │            │
│  │                                                       │            │
│  │  ┌─────────────────┐                                 │            │
│  │  │ Monitor Element │──┐ AUTO-FILL                    │            │
│  │  │  [Dropdown: 9]  │  │ TRIGGER!                     │            │
│  │  └─────────────────┘  │                              │            │
│  │                       │                              │            │
│  │  ┌────────────────────▼──┐                           │            │
│  │  │ Monitor Value         │ ← Automatically filled    │            │
│  │  │ [Numeric Input]       │   when dropdown changes   │            │
│  │  └───────────────────────┘   (but user can edit!)    │            │
│  │                                                       │            │
│  │  ┌─────────────────┐  ┌─────────────────┐            │            │
│  │  │ Option 1        │  │ Option 2        │            │            │
│  │  │ [Dropdown: 9]   │  │ [Dropdown: 9]   │            │            │
│  │  └─────────────────┘  └─────────────────┘            │            │
│  │                                                       │            │
│  │  H Level % [9 numeric inputs]                        │            │
│  │  L Level % [9 numeric inputs]                        │            │
│  └───────────────────────────────────────────────────────┘            │
│                                  │                                    │
│                    ┌─────────────▼──────────────┐                    │
│                    │   [Upload Button]          │                    │
│                    └─────────────┬──────────────┘                    │
└──────────────────────────────────┼───────────────────────────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────┐
                    │ collect_form_data()      │
                    │ Reads all widget values  │
                    └──────────────┬───────────┘
                                   │
                                   ▼
                    ┌──────────────────────────┐
                    │ Build JSON Object        │
                    │ - analytical_group       │
                    │ - analytical_method      │
                    │ - seq {...}              │
                    │ - level_out_info {...}   │
                    └──────────────┬───────────┘
                                   │
                                   ▼
                    ┌──────────────────────────┐
                    │ Save to DataManager      │
                    │ (in-memory storage)      │
                    └──────────────┬───────────┘
                                   │
                                   ▼
                    ┌──────────────────────────┐
                    │ json.dumps()             │
                    │ Convert to JSON string   │
                    └──────────────┬───────────┘
                                   │
                                   ▼
                    ┌──────────────────────────┐
                    │ Print to Console         │
                    │ Show MessageBox Preview  │
                    └──────────────────────────┘
                                   │
                          (Future: POST to backend)
```

---

## Monitor Element Auto-fill Flow

```
USER ACTION: Selects "FE" from dropdown
     │
     ▼
┌─────────────────────────────────┐
│ on_monitor_ele_changed()        │
│ Event handler triggered         │
└─────────────────┬───────────────┘
                  │
                  ▼
┌─────────────────────────────────┐
│ Get selected value              │
│ selected_ele = "FE"             │
└─────────────────┬───────────────┘
                  │
                  ▼
┌─────────────────────────────────┐
│ Lookup in monitor_ele_values    │
│ {"FE": "273.0", "C": "193.0"..} │
└─────────────────┬───────────────┘
                  │
                  ▼
┌─────────────────────────────────┐
│ Update monitor_value Entry      │
│ monitor_value.delete(0, END)    │
│ monitor_value.insert(0, "273.0")│
└─────────────────┬───────────────┘
                  │
                  ▼
┌─────────────────────────────────┐
│ User sees "273.0" in value field│
│ (Can manually edit if needed)   │
└─────────────────────────────────┘

RESULT IN JSON:
{
  "monitor_element": {
    "element": "FE",
    "value": "273.0"  ← Auto-filled (or user-edited)
  }
}
```

---

## Attenuator Information Page - Data Flow

```
┌──────────────────────────────────────────────────────────────────────┐
│                   ATTENUATOR INFORMATION PAGE                         │
│                                                                       │
│  ┌────────────────────────┐     ┌────────────────────────┐           │
│  │   LEFT TABLE           │     │   RIGHT TABLE          │           │
│  │  (16 pre-filled rows)  │     │  (9 filled + empties)  │           │
│  │                        │     │                        │           │
│  │  Element | Ele | ATT   │     │  Element | Ele | ATT   │           │
│  │  ─────────────────────  │     │  ─────────────────────  │           │
│  │  FE      |273.0| [77]  │     │  W       |220.4| [76]  │           │
│  │  C       |193.0| [49]  │     │  B       |182.6| [90]  │           │
│  │  SI      |212.4| [41]  │     │  NB      |319.5| [54]  │           │
│  │  ...     | ... | ...   │     │  ...     | ... | ...   │           │
│  │                        │     │  [____]  |[___]| [__]  │ ← Editable│
│  │  [Only ATT editable]   │     │  [All fields editable]  │           │
│  └────────────────────────┘     └────────────────────────┘           │
│                                                                       │
│                    ┌─────────────────────────┐                       │
│                    │   [Upload Button]       │                       │
│                    └─────────────┬───────────┘                       │
└──────────────────────────────────┼───────────────────────────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────┐
                    │ collect_form_data()      │
                    │ Loop through entries:    │
                    │ - left_att_entries       │
                    │ - right_att_entries      │
                    └──────────────┬───────────┘
                                   │
                                   ▼
                    ┌──────────────────────────┐
                    │ Build JSON Arrays        │
                    │ left_table: [{...}, ...] │
                    │ right_table: [{...}, ...] │
                    └──────────────┬───────────┘
                                   │
                                   ▼
                    ┌──────────────────────────┐
                    │ JSON Output              │
                    │ {                        │
                    │   "left_table": [...],   │
                    │   "right_table": [...]   │
                    │ }                        │
                    └──────────────────────────┘
```

---

## Element & Channel Information Pages - Data Flow

```
┌──────────────────────────────────────────────────────────────────────┐
│            ELEMENT / CHANNEL INFORMATION PAGE                         │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────┐         │
│  │                     DATA TABLE                          │         │
│  │  Scrollable with multiple rows                         │         │
│  │                                                         │         │
│  │  Row 1: [Field1] [Field2] [Field3] [Field4] [Field5]  │         │
│  │  Row 2: [Field1] [Field2] [Field3] [Field4] [Field5]  │         │
│  │  Row 3: [Field1] [Field2] [Field3] [Field4] [Field5]  │         │
│  │  ...                                                    │         │
│  │  Row N: [Field1] [Field2] [Field3] [Field4] [Field5]  │         │
│  │                                                         │         │
│  │  All fields are text inputs (NO DROPDOWNS)             │         │
│  └─────────────────────────────────────────────────────────┘         │
│                                                                       │
│                    ┌─────────────────────────┐                       │
│                    │   [Upload Button]       │                       │
│                    └─────────────┬───────────┘                       │
└──────────────────────────────────┼───────────────────────────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────┐
                    │ collect_form_data()      │
                    │ Loop through row entries │
                    └──────────────┬───────────┘
                                   │
                                   ▼
                    ┌──────────────────────────┐
                    │ Build JSON Array         │
                    │ elements: [{...}, ...]   │
                    │ OR                       │
                    │ channels: [{...}, ...]   │
                    └──────────────┬───────────┘
                                   │
                                   ▼
                    ┌──────────────────────────┐
                    │ JSON Output              │
                    │ (Currently not saved to  │
                    │  DataManager - TODO)     │
                    └──────────────────────────┘
```

---

## Dropdown Options Visualization

```
ANALYTICAL METHOD
┌────────────────────────────┐
│ Select:                    │
│ ┌────────────────────────┐ │
│ │ integration Mode       │◄├─ Default
│ │ PDA + Integration      │ │
│ └────────────────────────┘ │
└────────────────────────────┘

SOURCE SEQ1
┌────────────────────────────┐
│ Select:                    │
│ ┌────────────────────────┐ │
│ │ 3 Peak Spark           │◄├─ Default
│ │ Normal Spark           │ │
│ │ Combined Spark         │ │
│ │ Arclike Spark          │ │
│ │ Cleaning               │ │
│ │ High Voltage Spark     │ │
│ └────────────────────────┘ │
└────────────────────────────┘

MONITOR ELEMENT (with auto-fill)
┌────────────────────────────┐
│ Select Element:            │
│ ┌────────────────────────┐ │
│ │ None                   │ │
│ │ FE → Auto-fills 273.0  │◄├─ Default
│ │ C  → Auto-fills 193.0  │ │
│ │ Si → Auto-fills 212.4  │ │
│ │ MN → Auto-fills 293.3  │ │
│ │ P  → Auto-fills 178.3  │ │
│ │ S  → Auto-fills 180.7  │ │
│ │ V  → Auto-fills 311.0  │ │
│ │ CR → Auto-fills 267.7  │ │
│ └────────────────────────┘ │
│                            │
│ Value: [273.0]             │◄─ Auto-filled (editable)
└────────────────────────────┘
```

---

## JSON Transformation Flow

```
STEP 1: USER INTERACTION
┌─────────────────────────────────────┐
│ User fills form fields              │
│ User selects dropdown options       │
│ (Monitor element auto-fills value)  │
└─────────────────┬───────────────────┘
                  │
                  ▼
STEP 2: COLLECT DATA
┌─────────────────────────────────────┐
│ collect_form_data()                 │
│ - Read Entry.get()                  │
│ - Read Combobox.get()               │
│ - Iterate arrays                    │
└─────────────────┬───────────────────┘
                  │
                  ▼
STEP 3: BUILD STRUCTURE
┌─────────────────────────────────────┐
│ form_data = {                       │
│   "analytical_group": "...",        │
│   "analytical_method": "...",       │
│   "seq": {...},                     │
│   "level_out_information": {...}    │
│ }                                   │
└─────────────────┬───────────────────┘
                  │
                  ▼
STEP 4: PERSIST (for some pages)
┌─────────────────────────────────────┐
│ DataManager.save_*()                │
│ Stores in memory (_data dict)       │
│ Available to other pages            │
└─────────────────┬───────────────────┘
                  │
                  ▼
STEP 5: SERIALIZE
┌─────────────────────────────────────┐
│ json.dumps(form_data, indent=2)     │
│ Convert Python dict to JSON string  │
└─────────────────┬───────────────────┘
                  │
                  ▼
STEP 6: OUTPUT
┌─────────────────────────────────────┐
│ print(json_data)  ← Console         │
│ messagebox.showinfo()  ← UI Preview │
│ [Future: requests.post()]           │
└─────────────────────────────────────┘
```

---

## Backend Integration Flow (Future)

```
FRONTEND                      BACKEND
┌──────────┐                 ┌──────────┐
│  Upload  │                 │  Flask   │
│  Button  │                 │  FastAPI │
│  Clicked │                 │  Django  │
└─────┬────┘                 └────┬─────┘
      │                           │
      │ collect_form_data()       │
      ▼                           │
┌──────────────┐                  │
│  JSON Data   │                  │
└─────┬────────┘                  │
      │                           │
      │ requests.post()           │
      ├───────────────────────────▶
      │   POST /api/analytical-   │
      │        condition          │
      │   Content-Type:           │
      │   application/json        │
      │   Body: {...}             │
      │                           │
      │                           ▼
      │                    ┌─────────────┐
      │                    │  Validate   │
      │                    │  JSON Schema│
      │                    └──────┬──────┘
      │                           │
      │                           ▼
      │                    ┌─────────────┐
      │                    │  Convert    │
      │                    │  Types      │
      │                    └──────┬──────┘
      │                           │
      │                           ▼
      │                    ┌─────────────┐
      │                    │  Save to DB │
      │                    └──────┬──────┘
      │                           │
      │   Response {success:true} │
      ◀───────────────────────────┤
      │                           │
      ▼                           ▼
┌──────────────┐          ┌─────────────┐
│  Show        │          │  Return     │
│  Success     │          │  {id, ...}  │
│  Message     │          └─────────────┘
└──────────────┘
```

---

## Error Handling Flow

```
FRONTEND SENDS:
{
  "analytical_method": "INVALID_MODE"  ← Invalid!
}
      │
      ▼
BACKEND VALIDATES:
┌─────────────────────────────────────┐
│ if value not in ALLOWED_VALUES:     │
│     return error_response()         │
└─────────────────┬───────────────────┘
                  │
                  ▼
BACKEND RESPONDS:
{
  "success": false,
  "error": "Invalid analytical_method value",
  "field": "analytical_method",
  "received": "INVALID_MODE",
  "allowed": ["integration Mode", "PDA + Integration"]
}
      │
      ▼
FRONTEND DISPLAYS:
┌─────────────────────────────────────┐
│  [ERROR]                            │
│  Invalid analytical_method value    │
│  Received: INVALID_MODE             │
│  Allowed: integration Mode,         │
│           PDA + Integration         │
└─────────────────────────────────────┘
```

---

**Use these diagrams for:** Understanding data flow, debugging, team communication, documentation
