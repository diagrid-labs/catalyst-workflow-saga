import string
import random

from dapr.clients import DaprClient

def flight(input: any):
    if input['payment_processed'] is True:
        input['order_completed'] = True
    else:
        raise Exception("Payment missing")
    
    return input

def car(input: any):
    if input['car'] != "":
        input['car_reservation_id'] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

    return input