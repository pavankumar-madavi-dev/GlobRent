import time
import os
import json
import gspread
from google.oauth2.service_account import Credentials

# 1. Google Sheets Setup & Auth
creds_json = os.environ.get("GOOGLE_CREDS_JSON")

if creds_json:
    try:
        info = json.loads(creds_json)
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        credentials = Credentials.from_service_account_info(info, scopes=scopes)
        gc = gspread.authorize(credentials)
        
        # स्प्रेडशीट ओपन करणे
        SPREADSHEET_NAME = "MADAVI Complex Rent Manager"
        sh = gc.open(SPREADSHEET_NAME)
        print("✅ MADAVI COMPLEX - GLOBAL RENT MANAGER STARTED SUCCESSFULLY!")
        print("🚀 App is running in background mode for Glide/Render sync...")
    except Exception as e:
        print(f"❌ Error connecting to Google Sheets: {e}")
else:
    print("⚠️ WARNING: GOOGLE_CREDS_JSON Environment Variable missing!")
    print("👋 Running in Local Mode without Google Sheets Connection.")

# 2. Main Background Loop
try:
    while True:
        print(f"⏰ Server active: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        time.sleep(60)
except KeyboardInterrupt:
    print("🛑 Server stopped by user.")
