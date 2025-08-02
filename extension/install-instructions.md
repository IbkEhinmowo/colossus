<!-- @format -->

# Auto Marketplace Scanner - Installation Instructions

## Features

- **Automatic Page Refresh**: Refreshes the marketplace page every minute
- **Auto Data Collection**: Extracts marketplace listings automatically after each refresh
- **Real-time Status**: Shows scanning status, countdown timer, and item counts
- **Manual Scan**: Option to scan immediately without waiting
- **Modern UI**: Clean, gradient interface with status indicators

## Installation Steps

1. **Load Extension in Chrome**:

   - Open Chrome and go to `chrome://extensions/`
   - Enable "Developer mode" (toggle in top right)
   - Click "Load unpacked"
   - Select the `extension` folder from this project

2. **Start Backend Server**:

   ```bash
   cd pythonServer
   pip install -r requirements.txt  # if requirements.txt exists
   # or install manually: pip install fastapi uvicorn beautifulsoup4
   uvicorn app:app --reload --port 8000
   ```

3. **Usage**:
   - Navigate to a Facebook Marketplace page (or any marketplace with `/marketplace/item/` URLs)
   - Click the extension icon in Chrome toolbar
   - Click "Start Auto-Scan" to begin automatic scanning
   - The extension will refresh the page every minute and send data to the backend
   - View real-time status and countdown in the popup

## How It Works

1. **Auto-Refresh**: Every minute, the extension refreshes the current marketplace page
2. **Data Extraction**: After page loads, it scans for marketplace listing links
3. **Backend Processing**: Sends extracted HTML to FastAPI backend for parsing
4. **Real-time Updates**: Status and counts update in real-time

## Controls

- **Start/Stop Auto-Scan**: Toggle automatic scanning
- **Scan Now**: Perform immediate manual scan
- **Status Indicator**: Green dot = active, Red dot = inactive
- **Countdown Timer**: Shows time until next scan
- **Statistics**: Last scan time and item count

## Troubleshooting

- Make sure you're on a marketplace page before starting auto-scan
- Ensure backend server is running on http://127.0.0.1:8000
- Check Chrome DevTools console for any errors
- Extension will automatically stop if you navigate away from marketplace
