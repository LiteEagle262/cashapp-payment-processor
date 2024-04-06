import requests,re,string,random

your_cash_tag = "$LiteEagl"

'''
Create a json file called, processed.json and add the below to it


{
    "processed_invoices": [
        
    ]
}



(this just lets the program know what notes have already been processed)
'''

def generate_invoice_id(length=15):
    chars = string.ascii_letters + string.digits
    invoice_id = ''.join(random.choices(chars, k=length))
    return invoice_id

def is_invoice_processed(invoice_id: str):
    with open("processed.json", "r") as file:
        data = json.load(file)
        return invoice_id in data["processed_invoices"]

def add_invoice_to_processed(invoice_id: str):
    with open("processed.json", "r+") as file:
        data = json.load(file)
        data["processed_invoices"].append(invoice_id)
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()

def check(webrecipt: str, invoice_id: str, amount: float)
    try:
        if webrecipt.startswith("https://cash.app/payments/"):
            scraped_recipt = re.split("/payments/", webrecipt)[1]
            recipt_id = scraped_recipt.replace("/receipt", "")
            r = requests.get(f"https://cash.app/receipt-json/f/{recipt_id}").json()
            #getting note/invoice id
            note = r['notes']
            #getting reciver cashtag
            subtext = r['header_subtext']
            subtext2 = subtext[10:]
            cashtag = subtext2.strip()
            #getting payment value
            cash_value = r['detail_rows'][0]['value']
            value = float(cash_value[1:])
            if is_invoice_processed(invoice_id):
                return "This invoice has already been processed"        
            if cashtag != your_cash_tag:
                return "Wrong Recipient"
            if invoice_id != note:
                return "Invalid Note"
            if amount != value:
                return "You sent the wrong amount"
            add_invoice_to_processed(invoice_id)
            return True
        else:
            return "Invalid Web Recipt"
    except Exception as e:
        print("Server: Something went wrong: " + e)
        return "A Server Side error happened, please let the application developers know."
        
        

'''
Simple example of how you would use this below
'''
        
item_amount = float(50)
invoice_id = generate_invoice_id()
print("Your Note is: " + invoice_id)
print("Your Total is" + item_amount)
print("Please send the payment to: " + your_cash_tag")
webrecipt = input("Please enter your web recipt once sent :> ")
print("checking...")
ok = check(webrecipt, invoice_id, item_amount)
if ok == True:
    print("Payment Successfull")
else:
    print("Payment was not successfull, reason: " + ok)
