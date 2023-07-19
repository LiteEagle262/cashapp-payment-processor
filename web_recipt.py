import requests #I dont think is needed but will add just incase im wrong cus im posting this at 12 am and im tired asf
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


'''
The reason this needs selenium is because cashapp is dynamicly loaded, I know there is a way around this without using selenium
but it was easier just to use for then since for the project I origionaly made this for that didnt matter.
'''

'''
Make processed_invoices.json file and put the below in file contents
{
    "processed_invoices": [
        "tpDQfBXChTecddj",
        "rGjNgEakPNxzwcu"
    ]
}
'''

def is_invoice_processed(invoice_id):
    with open("processed_invoices.json", "r") as file:
        data = json.load(file)
        return invoice_id in data["processed_invoices"]

def add_invoice_to_processed(invoice_id):
    with open("processed_invoices.json", "r+") as file:
        data = json.load(file)
        data["processed_invoices"].append(invoice_id)
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()

def generate_invoice_id(length=15):
    chars = string.ascii_letters + string.digits
    invoice_id = ''.join(random.choices(chars, k=length))
    return invoice_id

def checkpayment(url, amount, invoice_id):
    if url.startswith("https://cash.app/payments/"):
        if not is_invoice_processed(invoice_id):
            driver = webdriver.Chrome()
            try:
                driver.get(url)
                time.sleep(2)
                html = driver.page_source
                soup = BeautifulSoup(html, "html.parser")
                driver.quit()

                # Extract payment amount
                payment_amount_div = soup.find("div", class_="css-c01kul")
                payment_amount = payment_amount_div.text.strip("$")
                if float(payment_amount) != float(amount):
                    return "amount"

                # Extract cashtag
                cashtag_element = soup.find("h4", class_="css-1enpufc")
                if cashtag not in cashtag_element.text:
                    return "cashtag"

                # Extract completion status
                completion_status_div = soup.find("div", class_="css-1f4nnn0")
                if completion_status_div.text.strip().lower() != "completed":
                    return "incomplete"

                # Extract payment source
                payment_sources = soup.find_all("dd", class_="css-1o1jbxi")
                if len(payment_sources) >= 2:
                    payment_source = payment_sources[1].text.strip()
                    if payment_source.lower() != "cash":
                        return "source"
                else:
                    return "source"
            
                # Extract Note
                note_element = soup.find("p", class_="css-1b5gxht")
                if note_element is not None:
                    note = note_element.text.strip().replace("For", "").strip()
                    if note != invoice_id:
                        return "note"
                else:
                    return "note"
                
                add_invoice_to_processed(invoice_id)
                return True
            except Exception as e:
                print("Error: " + str(e))
                return None
        else:
            return "already"
    else:
        return None

#web recipt, payment amount, invoice id
payment = checkpayment("webrecipt", 10, generate_invoice_id())
if payment == True:
    await print("Payment Confirmed.")
elif payment == "amount":
    await print("You sent the incorrect payment amount")
elif payment == "cashtag":
    await print("You sent the payment to the incorrect cashtag")
elif payment == "incomplete":
    await print("Payment hasnt been accepted yet")
elif payment == "source":
    await print("we only accept payments from balance.")
elif payment == "already":
    await print("This payment has already been processed.")
elif payment == "note":
    await print("The note specified does not apear to be the invoice id.")
