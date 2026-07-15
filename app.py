import os
import json
import gspread
from flask import Flask, render_template, jsonify
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# 1. Google Sheets Setup & Auth
creds_json = os.environ.get("GOOGLE_CREDS_JSON")
sh = None

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
        print("✅ MADAVI COMPLEX - Google Sheets connected successfully!")
    except Exception as e:
        print(f"❌ Error connecting to Google Sheets: {e}")
else:
    print("⚠️ WARNING: GOOGLE_CREDS_JSON Environment Variable missing!")

# 2. Web App Route (मुख्य डॅशबोर्ड दाखवण्यासाठी)
@app.route('/')
def home():
    # हे 'templates/index.html' फाईल मोबाईलवर लोड करेल
    return render_template('index.html')

# 3. API Route (भविष्यात डेटा गुगल शीटमधून ॲपमध्ये ओढण्यासाठी)
@app.route('/api/status')
def status():
    if sh:
        return jsonify({"status": "connected", "database": "MADAVI Complex Rent Manager"})
    return jsonify({"status": "local_mode", "database": "Disconnected"})

if __name__ == '__main__':
    # लोकल टेस्टिंगसाठी पोर्ट ५००० वर रन होईल
    app.run(host='0.0.0.0', port=5000, debug=True)

