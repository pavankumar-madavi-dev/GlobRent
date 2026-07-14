# -*- coding: utf-8 -*-
import os
import json
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# फाईल पाथ
CRED_PATH = "credentials/google_creds.json"
CONFIG_PATH = "credentials/sheet_config.json"

LANGUAGES = {
    "1": {  # मराठी
        "welcome": "\n=============================================\n    MADAVI COMPLEX - GLOBAL RENT MANAGER   \n=============================================",
        "menu_1": "१. नवीन मालक नोंदणी (Add Owner)",
        "menu_2": "२. नवीन भाडेकरू नोंदणी (Add Tenant)",
        "menu_3": "३. नवीन प्रॉपर्टी जोडा (Add Property)",
        "menu_4": "४. नवीन डिजिटल ॲग्रीमेंट (Create Agreement)",
        "menu_5": "५. भाडे पेमेंट करा व PDF रिसिप्ट मिळवा (Rent Payment & PDF)",
        "menu_6": "६. बाहेर पडा (Exit)",
        "choice": "तुमचा पर्याय निवडा (1-6): ",
        "success": "[SUCCESS] डेटा गुगल शीटमध्ये यशस्वीरित्या सेव्ह झाला!",
        "sheet_prompt": "तुमच्या गुगल शीटची (Google Sheet) लिंक पेस्ट करा: ",
        "pdf_success": "[SUCCESS] पीडीएफ रिसिप्ट यशस्वीरित्या जनरेट झाली! (receipt.pdf)",
        "fields": ["नाव", "संपर्क", "ओळखपत्र/आधार", "पत्ता", "रक्कम (चलन सह)", "तारीख (DD-MM-YYYY)"]
    },
    "2": {  # English
        "welcome": "\n=============================================\n    MADAVI COMPLEX - GLOBAL RENT MANAGER   \n=============================================",
        "menu_1": "1. Add New Owner",
        "menu_2": "2. Add New Tenant",
        "menu_3": "3. Add New Property",
        "menu_4": "4. Create Digital Agreement",
        "menu_5": "5. Pay Rent & Generate PDF Receipt",
        "menu_6": "6. Exit",
        "choice": "Enter your choice (1-6): ",
        "success": "[SUCCESS] Data saved to Google Sheet successfully!",
        "sheet_prompt": "Paste your Google Sheet Link: ",
        "pdf_success": "[SUCCESS] PDF Receipt generated successfully! (receipt.pdf)",
        "fields": ["Name", "Contact", "ID Proof/Passport", "Address", "Amount (with Currency)", "Date (DD-MM-YYYY)"]
    }
}

current_lang = "2"
sheet = None

def init_google_sheet():
    global sheet
    msg = LANGUAGES[current_lang]
    if not os.path.exists(CRED_PATH):
        print(f"\n[INFO] कृपया '{CRED_PATH}' मध्ये तुमची Google Service Account JSON फाईल ठेवा.")
        return False
    
    # शीट लिंक सेव्ह करणे/लोड करणे
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as f:
            sheet_url = json.load(f).get("url")
    else:
        sheet_url = input(msg["sheet_prompt"])
        with open(CONFIG_PATH, 'w') as f:
            json.dump({"url": sheet_url}, f)

    try:
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_file(CRED_PATH, scopes=scopes)
        client = gspread.authorize(creds)
        sheet = client.open_by_url(sheet_url)
        return True
    except Exception as e:
        print(f"[ERROR] गुगल शीटशी जोडता आले नाही: {e}")
        return False

def get_next_id(worksheet, prefix):
    try:
        records = worksheet.get_all_values()
        if len(records) <= 1:
            return f"{prefix}_1001"
        last_id = records[-1][0]
        last_num = int(last_id.split("_")[1])
        return f"{prefix}_{last_num + 1}"
    except:
        return f"{prefix}_1001"

def generate_pdf_receipt(tx_id, tenant, amount, prop):
    msg = LANGUAGES[current_lang]
    pdf_filename = f"receipt_{tx_id}.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "MADAVI COMPLEX - RENT RECEIPT")
    c.setFont("Helvetica", 12)
    c.drawString(100, 720, f"Transaction ID: {tx_id}")
    c.drawString(100, 700, f"Date: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
    c.drawString(100, 660, f"Tenant Name: {tenant}")
    c.drawString(100, 640, f"Property Details: {prop}")
    c.drawString(100, 620, f"Amount Paid: {amount}")
    c.drawString(100, 580, "Status: PAID / यशस्वी")
    c.drawString(100, 540, "Thank you for using our Global Rent Manager App!")
    c.save()
    print(f"{msg['pdf_success']} -> {pdf_filename}")

def main_menu():
    global current_lang, sheet
    msg = LANGUAGES[current_lang]
    print(msg["welcome"])
    print(msg["menu_1"])
    print(msg["menu_2"])
    print(msg["menu_3"])
    print(msg["menu_4"])
    print(msg["menu_5"])
    print(msg["menu_6"])
    print("=============================================")
    
    choice = input(msg["choice"])
    
    if choice in ['1', '2', '3', '4', '5'] and not sheet:
        if not init_google_sheet():
            return

    if choice == '1':
        ws = sheet.get_worksheet(0) # Owners Sheet
        o_id = get_next_id(ws, "OWNER")
        name = input(msg["fields"][0] + ": ")
        phone = input(msg["fields"][1] + ": ")
        id_no = input(msg["fields"][2] + ": ")
        addr = input(msg["fields"][3] + ": ")
        ws.append_row([o_id, name, phone, id_no, addr])
        print(msg["success"])

    elif choice == '2':
        ws = sheet.get_worksheet(1) # Tenants Sheet
        t_id = get_next_id(ws, "TEN")
        name = input(msg["fields"][0] + ": ")
        phone = input(msg["fields"][1] + ": ")
        id_no = input(msg["fields"][2] + ": ")
        addr = input(msg["fields"][3] + ": ")
        ws.append_row([t_id, name, phone, id_no, addr])
        print(msg["success"])

    elif choice == '5':
        ws = sheet.get_worksheet(4) # Transactions Sheet
        tx_id = get_next_id(ws, f"TXN_{datetime.now().year}")
        tenant = input(msg["fields"][0] + " (Tenant Name): ")
        prop = input("Property Type/ID: ")
        amount = input(msg["fields"][4] + ": ")
        date_str = datetime.now().strftime('%d-%m-%Y')
        ws.append_row([tx_id, tenant, prop, amount, date_str, "PAID"])
        generate_pdf_receipt(tx_id, tenant, amount, prop)

    elif choice == '6':
        exit()

if __name__ == "__main__":
    print("\n1. मराठी | 2. English")
    lang_ch = "2"
    if lang_ch in LANGUAGES:
        current_lang = lang_ch
    while True:
        main_menu()
