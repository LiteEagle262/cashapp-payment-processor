import asyncio
import random
import string
from cashapp import cashapp

async def gen_invoice(amt):
    def generate_invoice_id(length=15):
        chars = string.ascii_letters + string.digits
        invoice_id = ''.join(random.choices(chars, k=length))
        return invoice_id

    invoice_id = generate_invoice_id()
    print(invoice_id)
    # use invoice id as note
    pstatus = False
    for x in range(450):
        await asyncio.sleep(5)
        if cashapp.check_if_paid(invoice_id, amt):
            pstatus = True
            break
    if not pstatus:
        print("payment not detected within 30 mins!!")
    else:
        print("Payment Detected and complete!")

# Example usage
asyncio.run(gen_invoice(100))
