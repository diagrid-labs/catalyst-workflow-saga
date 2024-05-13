import json

from dapr.clients import DaprClient

def notify(input: any):
    name = input['first_name'] + input['last_name']

    with DaprClient() as d:
        d.save_state(store_name="statestore", key=name, value=json.dumps(input))
        d.publish_event("pubsub", "onreservationsuccess", json.dumps({ 'message': 'Reservation successful for ' + name}))

    return input