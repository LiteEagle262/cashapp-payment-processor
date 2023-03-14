import imaplib, email, re, json

DB_FILE = 'data.json'
MAIL_USER = ""
MAIL_PSW = ""
MAIL_SERVER = "imap.zoho.com"

class cashapp:
    def check_if_paid(invoice_id, price):
        with open(DB_FILE, 'r') as f:
            data = json.load(f)
        if invoice_id in data:
            if data[invoice_id] == price:
                return True
            else:
                return False
        else:
             return False

    def fetchmail(self):
        print("Fetched mail")
        try:
            mail = imaplib.IMAP4_SSL(MAIL_SERVER)
            mail.login(MAIL_USER, MAIL_PSW)
            mail.select('inbox')
            typ, data = mail.search(None, 'UNSEEN')
            for num in data[0].split():
                typ, data = mail.fetch(num, '(RFC822)')
                raw_email = data[0][1]
                raw_email_string = raw_email.decode('utf-8')
                email_message = email.message_from_string(raw_email_string)
                if "cash@square.com" in str(email_message):
                    for part in email_message.walk():
                        if part.get_content_type() == 'text/html':
                            html_content = part.get_payload(decode=True).decode('utf-8')
                            cash_raw = re.search(r'<div class="value">\s*\$(\d+\.\d+)\s*</div>', html_content)
                            note_raw = re.search(r'<div class="text note" style="color:#999999overflow: hidden;">\s*(.*?)\s*</div>',html_content)
                            if cash_raw and note_raw:
                                cash = cash_raw.group(1)
                                print(cash)
                                _note_ = note_raw.group(1)
                                note = _note_[4:]
                                print(note)
                                with open(DB_FILE, 'r') as f:
                                    cashapp_db = json.load(f)
                                if note not in cashapp_db:
                                    cashapp_db[note] = float(cash)
                                    with open(DB_FILE, 'w') as f:
                                        json.dump(cashapp_db, f)
                                        print("saved")
                                else:
                                    pass
            mail.close()
            mail.logout()
        except Exception as e:
            print(e)
