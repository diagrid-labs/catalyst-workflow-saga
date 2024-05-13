from flask import Flask, request
app = Flask(__name__)

import dapr.ext.workflow as wf
import activities
import activities.confirm
import activities.pay
import activities.reserve
import activities.success

wfr = wf.WorkflowRuntime()
wf_client = wf.DaprWorkflowClient()

wfr.start()

@app.route("/reserveFlight", methods=['POST'])
def reserve_flight_api():
    req = request.get_json()

    instance_id = wf_client.schedule_new_workflow(workflow=task_chain_workflow, input=req)
    wf_client.wait_for_workflow_completion(instance_id)

    return "Done"

@wfr.workflow(name='reserveflight')
def task_chain_workflow(ctx: wf.DaprWorkflowContext, wf_input: any):
    try:
        reserveFlightResponse = yield ctx.call_activity(reserve_flight, input=wf_input)
        reserveCarResponse = yield ctx.call_activity(reserve_car, input=reserveFlightResponse)
        processPaymentResponse = yield ctx.call_activity(process_payment, input=reserveCarResponse)
        confirmFlightResponse = yield ctx.call_activity(confirm_flight, input=processPaymentResponse)
        confirmCarResponse = yield ctx.call_activity(confirm_car, input=confirmFlightResponse)
        notifyResponse = yield ctx.call_activity(notify_success, input=confirmCarResponse)

        print(notifyResponse, flush=True)
    except Exception as e:
        yield ctx.call_activity(error_handler, input=str(e))
        raise
    return [reserveFlightResponse, reserveCarResponse, processPaymentResponse, confirmFlightResponse, confirmCarResponse, notifyResponse]


@wfr.activity
def reserve_flight(ctx, activity_input):
    print(f'Reserve Flight: Received input: {activity_input}.')
    return activities.reserve.flight(activity_input)

@wfr.activity
def reserve_car(ctx, activity_input):
    print(f'Reserve Car: Received input: {activity_input}.')
    return activities.reserve.car(activity_input)

@wfr.activity
def process_payment(ctx, activity_input):
    print(f'Process Payment: Received input: {activity_input}.')
    return activities.pay.process(activity_input)

@wfr.activity
def confirm_flight(ctx, activity_input):
    print(f'Confirm Flight: Received input: {activity_input}.')
    return activities.confirm.flight(activity_input)

@wfr.activity
def confirm_car(ctx, activity_input):
    print(f'Confirm Car: Received input: {activity_input}.')
    return activities.confirm.car(activity_input)

@wfr.activity
def notify_success(ctx, activity_input):
    print(f'Notify On Success: Received input: {activity_input}.')
    return activities.success.notify(activity_input)

@wfr.activity
def error_handler(ctx, error):
    print(f'Executing error handler: {error}.')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
