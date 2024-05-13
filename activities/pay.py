import json

from dapr.clients import DaprClient

def process(input: any):
    input['payment_processed'] = True
    try:
        with DaprClient() as d:
            d.save_state(store_name="statestore", key=input['id'] + "-payment", value=json.dumps(input))
    except Exception as e:
        print(e, flush=True)
        
    return input