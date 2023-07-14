import asyncio
import random
import string
from cashapp import cashapp

def generate_invoice_id(length=15):
    chars = string.ascii_letters + string.digits
    invoice_id = ''.join(random.choices(chars, k=length))
    return invoice_id

invoiceid = geninvoice()
amount = 20 #20
print(f"Invoice ${amount}, Invoice ID (NOTE): {invoiceid}")
cashapp.fetchmail()
print(cashapp.check_if_paid(invoiceid, amount))
