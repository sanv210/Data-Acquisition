# DAQ Desktop Application

## Folder Structure

```
frontend/
├── app.py              # Main entry point - Landing page (Analytical Group Information)
├── pages/              # All subsequent pages
│   ├── __init__.py
│   └── next_page.py    # Placeholder for next page (to be implemented)
├── utils/              # Utility functions and helpers
│   └── __init__.py
├── assets/             # Images, icons, and other static resources
└── requirements.txt    # Python dependencies
```

## Running the Application

1. Install dependencies (if any):
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python app.py
   ```

## Building Executable

To create a standalone executable:

```bash
pyinstaller --onefile --windowed app.py
```

The executable will be created in the `dist/` folder.

## Features

- **Landing Page**: Analytical Group Information with list of groups and action buttons
- **Navigation**: Select button leads to next page (to be implemented)
- All buttons functional with placeholder handlers

## Next Steps

Share the design for the next page to complete the navigation flow.
