from WebApp import db
from WebApp.model import Transaction
import requests
import json


def CheckTransactionStatus(trans: Transaction):
    url = f"https://api.sandbox.midtrans.com/v2/{trans.id}/status"
    response = requests.get(url, headers={
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "U0ItTWlkLXNlcnZlci1VS29vNHd1WFBrcGtvT3g4ZEZXbGFfQlM6",
    })
    jsonResponse = json.loads(response.text)
    transaction_status = jsonResponse['transaction_status']
    fraud_status = jsonResponse['fraud_status']
    if (transaction_status == 'capture' or transaction_status == 'settlement'):
        if (fraud_status == 'challenge' or fraud_status == 'accept'):
            trans.status = transaction_status
            trans.data = json.dumps(jsonResponse)
            db.session.commit()
    elif (transaction_status == 'cancel' or transaction_status == 'deny' or transaction_status == 'expire'):
        book_info = trans.book_info
        try:
            trans.status = transaction_status
            trans.data = json.dumps(jsonResponse)
            for book in book_info:
                db.session.delete(book)
            db.session.commit()
        except:
            pass
    elif (transaction_status == 'pending'):
        pass
    print(transaction_status)
