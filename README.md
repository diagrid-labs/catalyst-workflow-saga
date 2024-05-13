# Catalyst Workflow on AWS

This repo contains a Python app that shows you how to implement the [AWS reference architecture for Saga orchestration](https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/implement-the-serverless-saga-pattern-by-using-aws-step-functions.html?did=pg_card&trk=pg_card) using Catalyst Workflow.

Catalyst Workflow is a fully managed durable exection engine built on top of the [open-source Dapr project](https://dapr.io/). With Catalyst Workflow on AWS you can implement the saga pattern via orchestration and get the following benefits:

* Use any AWS compute service available, including ECS, AppRunner, EC2 etc.
* Use a fully managed Diagrid state store for workflow execution state, or bring your own
* Use any messaging service for downstream notifications, from Diagrid's managed pub/sub to your own Kafka, SQS etc.
* End to end observability with API logs, metrics and more
* A workflow execution UI that allows you to dig into each activity's execution status
* A single and consistent polyglot programming model that runs anywhere
* Local debugging without needing emulators or Docker containers

*Note: You can run Catalyst Workflow on any cloud or compute environment including your local machine*

## Running the sample

### Prerequisites

The following services, tools, and frameworks are required for this demo:

- [Diagrid Catalyst](https://www.diagrid.io/catalyst) account ([sign up](https://pages.diagrid.io/catalyst-early-access-waitlist) for private beta access) and the [Diagrid CLI](https://docs.diagrid.io/catalyst/references/cli-reference/intro)
- [Python 3.8](https://www.python.org/downloads/) or later

### Getting started

Create a new Catalyst project named `catalyst-workflow` and use the Diagrid managed pub/sub broker & KV store, and enable the managed workflow API:

```bash
diagrid project create catalyst-workflow --deploy-managed-pubsub --deploy-managed-kv --enable-managed-workflow --wait
```

To set this project as the default in the CLI run:

```bash
diagrid project use catalyst-workflow
```

Create a new App ID for our reservations app:

```bash
diagrid appid create reservations
```

In the root of the Python app, set the project URLs and API token for Catalyst:

```bash
export DAPR_HTTP_ENDPOINT=$(diagrid project get -o json | jq -r '.status.endpoints.http.url')
export DAPR_GRPC_ENDPOINT=$(diagrid project get -o json | jq -r '.status.endpoints.http.url')
export DAPR_API_TOKEN=$(diagrid appid get reservations -o json | jq -r '.status.apiToken')
```

All done! Now you can run the app, issue a JSON request and see the workflow run to completion:

```bash
python3 app.py

curl -XPOST -H "Content-type: application/json" -d '{"first_name": "hello", "last_name": "there", "location": "spain", "car_class": "compact"}' 'http://localhost:5000/reserveFlight'
```

### Running in a container

You can containerize this code and run it on any container based environment:

```
docker built -t <REPO>/<NAME>:latest .
```

*Note: make sure to supply the container with the environment variables for the http, grpc endpoints and the API token*

### Bringing your own database and messaging services

This example uses the Catalyst fully managed database and pub/sub brokers for ease of use and easy set up experience. If you want to use your own cloud services, [read here](https://docs.diagrid.io/catalyst/how-to-guides/connect-to-external-infrastructure).
