# How to Use Kallisti

### Deployment

The process to deploy Kallisti will be different depending on the
infrastructure, but fundamentally Kallisti is a self-contained service written
in Python, so it won't be overly complicated.

##### Requirements

* Python 3.6 or later version
* 1GB memory

##### Run Kallisti locally

Here are the steps to run Kallisti locally:

```bash
# clone the Kallisti project
git clone https://github.com/jpmorganchase/kallisti.git

# cd into the project root
cd kallisti

# install dependencies
pip install -r requirements.txt

# run migrations
python manage.py migrate

# export credential for chaos tests on k8s since we are running locally
# (service account token can be used if Kallisti is deployed to k8s)
export K8S_USERNAME='user-123'
export K8S_PASSWORD='my-password'

# start the worker process
python manage.py run_huey

# start the server process (in a different shell session)
python manage.py runserver
```

> **Note**
>
> Please refer to [Credentials for Chaos Steps page][step-credentials] for the
> details on the credentials.

##### Deploy Kallisti

As seen in the [steps to run Kallisti locally](#run-kallisti-locally) above, we
basically need to run a web server process and a worker process after installing
the dependencies to start Kallisti. However, for production use we strongly
recommend that you configure these two things below:

* Protecting the Kallisti API:<br /> As Kallisti would be controlling the
  infrastructure with the configured credentials, the access to Kallisti API
  should be protected. Please refer to [Access Control][access-control] page for
  controlling the access to Kallisti API.
  
* Process Monitoring:<br /> In production the processes for a service should be
  monitored with restart options. Also Django's default server is not for
  production use. `run.sh` would run the Kallisti processes with
  [gunicorn](https://gunicorn.org/) under
  [supervisord](http://supervisord.org/), so this file can be used as a startup
  script in your Docker image or your bundle for application container services.
  (Please note supervisord only supports UNIX-like systems.)

### Use Kallisti

Once Kallisti is deployed, you can visit its url and you'll land on the Swagger
UI of Kallisti API. These steps can be followed to execute your first experiment
on Kubernetes.

##### Authorize

You can authorize yourself by using the authorization prompt after clicking the
`Authorize` button on the right top of Swagger UI. (This step is not required
for the local testing without the access control on Kallisti API.)

##### Create an Experiment

By opening `POST /experiment` tab and clicking `Try it out` button on the
Swagger UI, the request body becomes editable. Here is the example experiment
data to fill it out with: (Please refer to the [Concept][concept-experiment]
page for the details of an experiment.)

```json
{
  "name": "Terminate a hello world pod",
  "description": "Terminate a pod and validate the status of the application's health endpoint.",
  "steps": [ 
    {
      "step": "Terminate pod",
      "do": "k8s.terminate_pods",
      "where": {
        "label_selector": "app=hello-world",
        "qty": 1,
        "ns": "my-namespace",
        "credentials": {
          "type": "ENV_VAR_USERNAME_PASSWORD",
          "password_key": "K8S_PASSWORD",
          "username_key": "K8S_USERNAME"
        }
      }
    },
    {
      "step": "HTTP health check",
      "do" : "cm.http_probe",
      "where": {
        "url" : "https://hello-world.com/health",
      }
    }
  ]
}
```

> **Note** 
>
> If your Kallisti is deployed to Kubernetes with a role-based
> access control configured for your namespace, `credentials` block above is not
> required since Kallisti's [k8s module][module-k8s] uses
> [Service Account Token File Credential][step-creds-k8s-svc-acc] as its default
> credential.

Once an experiment is created, you can find its `id` from the response of `POST
/experiment` API or `GET /experiment` API as below:

```json
{
    "id": "698e2183-fb16-478f-80c2-ea0080a89417",
    "name": "Terminate a hello world pod",
    ...
}
```

##### Run a Trial

You can run the created experiment by using `POST /trial` with the body as
below: (Please refer to the [Concept][concept-trial] page for the details of a
trial .)

```json
{
    "experiment" : "698e2183-fb16-478f-80c2-ea0080a89417"
}
```

Once the trial is created, `GET /trial` API can be used to check the status and
the log output. Also `GET /report` can be used for generating the
[report][report] file.

[access-control]: ./access-control.md
[concept-experiment]: ./concept.md#experiment
[concept-trial]: ./concept.md#trial
[step-credentials]: ./step-credentials.md
[module-k8s]: ./modules.md#kubernetes
[report]: ./reporting.md
[step-creds-k8s-svc-acc]: ./step-credentials.md#kubernetes-service-account-token-file
