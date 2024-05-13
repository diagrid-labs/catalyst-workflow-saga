import string
import random

def flight(input: any):
    if input['location'] == "":
        raise Exception("Location is required")
    
    input['id'] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    return input

def car(input: any):
    if input['car_class'] == "compact":
        input['car'] = "xs car"

    return input