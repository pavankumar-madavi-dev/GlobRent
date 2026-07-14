import time
import os
import json
import gspread
from google.oauth2.service_account import Credentials

# 1. Google Sheets Setup & Auth
# Render वरील Environment Variable मधून क्रेडेंशियल्स वाचणे
creds_json = os.environ.get("GOOGLE_CREDS_JSON")

if creds_json:
    info = json.loads(creds_json)
else:
    # लोकल टेस्टिंगसाठी बॅकअप फाईल
    with open('service_account.json') as f:
        info = json.load(f)

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_info(info, scopes=scopes)
gc = gspread.authorize(credentials)

# तुमच्या स्प्रेडशीटचे नाव
SPREADSHEET_NAME = "MADAVI Complex Rent Manager"
sh = gc.open(SPREADSHEET_NAME)

print("✅ MADAVI COMPLEX - GLOBAL RENT MANAGER STARTED SUCCESSFULLY!")
print("🚀 App is running in background mode for Glide/Render sync...")

# 2. Main Background Loop
# सर्व्हर चालू ठेवण्यासाठी आणि बॅकग्राउंड टास्क रन करण्यासाठी लूप
try:
    while True:
        # सर्व्हर ॲक्टिव्ह ठेवण्यासाठी दर ६० सेकंदांनी प्रिंट करेल
        print(f"⏰ Server active: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # जर फ्युचरमध्ये ऑटोमॅटिक कामे करायची असतील (उदा. ऑटो-पेनल्टी), 
        # तर त्याचे लॉजिक इथे लिहिता येईल.
        
        time.sleep(60)
except KeyboardInterrupt:
    print("🛑 Server stopped by user.")
