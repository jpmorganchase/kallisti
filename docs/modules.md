# Chaos Injection Modules

Kallisti modules are organized by namespaces. Each namespace has a short-form
(e.g. cf for Cloud Foundry).

* [Cloud Foundry (cf)](#cloud-foundry) 
* [Kubernetes (k8s)](#kubernetes)
* [Istio (istio)](#istio) 
* [Common (cm)](#common)
* [Prometheus (prom)](#prometheus)
* [AWS (aws)](#amazon-web-service)
* [Module Exceptions](#module-exceptions)

## Cloud Foundry

**Namespace:** `cf`

Kallisti supports the full set of commands provided by
[ChaosToolkit Cloud Foundry driver](https://docs.chaostoolkit.org/drivers/cloudfoundry/#exported-activities).
There are variety of actions to inject chaos on Cloud Foundry including:

* [terminate_app_instance](https://docs.chaostoolkit.org/drivers/cloudfoundry/#terminate_app_instance):
  Terminates an application's instance at a given index.
* [stop_app](https://docs.chaostoolkit.org/drivers/cloudfoundry/#stop_app):
  Stops an application.
* [stop_all_apps](https://docs.chaostoolkit.org/drivers/cloudfoundry/#stop_all_apps):
  Stops all applications for a specified org.
* [start_all_apps](https://docs.chaostoolkit.org/drivers/cloudfoundry/#start_all_apps):
  Starts all application for a specified org.
* [terminate_some_random_instances](https://docs.chaostoolkit.org/drivers/cloudfoundry/#start_all_apps):
  Terminate a random instance of an application.

In Kallisti, these ChaosToolkit CF commands can be used in the following way:

* `cf_api_url` is an argument required in the `where` clause.
* `credentials` is an optional argument. If provided, it overrides the default
  credential of [Environment Variables credential][step-credentials-env] which
  uses the keys of `CF_USERNAME` and `CF_PASSWORD`.
* The `configuration` and `secrets` parameters of ChaosToolkit commands are not 
  needed.

For example: 

the ChaosToolkit command
[terminate_app_instance](https://docs.chaostoolkit.org/drivers/cloudfoundry/#terminate_app_instance)
has the following interface:

```python
def terminate_app_instance(app_name: str,
                           instance_index: int,
                           configuration: Dict[str, Dict[str, str]],
                           secrets: Dict[str, Dict[str, str]],
                           org_name: str = None,
                           space_name: str = None):
    pass
```

When used in Kallisti, the command should be specified as the following, which
effectively asks Kallisti to terminate the first application instance of
"your-app-name" running in org "your-org-name" and "dev" space.

```json
{
  "step": "terminate app instance",
  "do": "cf.terminate_app_instance",
  "where": {
    "cf_api_url": "https://my-cf-api.com",
    "app_name": "your-app-name",
    "instance_index": 0,
    "org_name": "your-org-name",
    "space_name": "dev"
  }
}
```

**Arguments:**

| Name           | Type     | Default | Required | Description |
|----------------|----------|---------|----------|-------------|
| cf_api_url     | str      |         | Yes      | CF API endpoint of the target environment. 
| app_name       | str      |         | Yes      | The name of app to terminate.
| org_name       | str      |         | Yes      | The name of the CF org to search the app. If not specified, all available orgs are searched.
| space_name     | str      |         | Yes      | The name of space to be targeted.
| credentials    | dict     |         | No       | The credentials used to access the CF org of the target application. See [Chaos Step Credentials page][step-credentials] for more details.

## Kubernetes

**Namespace:** `k8s`

Kallisti supports the majority of commands provided by
[ChaosToolkit Kubernetes driver](https://docs.chaostoolkit.org/drivers/kubernetes/#exported-activities)
with the appropriate privilege. There are variety of actions to inject chaos on
Kubernetes including:

* [terminate_pods](https://docs.chaostoolkit.org/drivers/kubernetes/#terminate_pods):
  Terminates the selected pod(s) gracefully. Pods can be selected with label
  and/or name patterns.
* [delete_service](https://docs.chaostoolkit.org/drivers/kubernetes/#delete_service):
  Delete a service by name.
* [delete_replicaset](https://docs.chaostoolkit.org/drivers/kubernetes/#delete_replica_set):
  Delete a replicaset by name in a namespace.
* [delete_deployment | scale_deployment](https://docs.chaostoolkit.org/drivers/kubernetes/#delete_deployment):
  Delete a deployment / scale a deployment up or down in a namespace. 
* [remove_statefulset | scale_statefulset](https://docs.chaostoolkit.org/drivers/kubernetes/#remove_statefulset):
  Delete a statefulset / scale a statefulset up or down in a namespace.
* [deny_all_egress](https://docs.chaostoolkit.org/drivers/kubernetes/#deny_all_egress):
  Deny all egress network from all pods in a namespace.
* [remove_network_policy](https://docs.chaostoolkit.org/drivers/kubernetes/#remove_network_policy):
  Remove a network policy by name in a namespace.

In Kallisti, these ChaosToolkit Kubernetes commands can be used in the following
way:

* `k8s_api_host` is a required argument in `where` clause.
* Though the value would default to `k8s` when not specified, the `platform`
  parameter can be specified with `eks` in `where` clause to target AWS EKS. In
  this case, Kallisti will use `boto3` for the authentication on AWS service, so
  [necessary environment parameters](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html#using-environment-variables)
  should be exported in the Kallisti environment. There should also be
  additional parameters in `where` clause to specify the region and cluster.
  Please see the example below.
* `credentials` is an optional argument. If provided, it overriders the default
  credential of
  [Kubernetes Service Account Token File][step-credentials-k8s-svc-acc].
* The `configuration` and `secrets` parameters of ChaosToolkit commands are not 
  needed.

For example:

The ChaosToolkit command
[terminate_pods](https://docs.chaostoolkit.org/drivers/kubernetes/#terminate_pods)
has the following interface:

```python
def terminate_pods(label_selector: str = None,
                   name_pattern: str = None,
                   all: bool = False,
                   rand: bool = False,
                   mode: str = 'fixed',
                   qty: int = 1,
                   grace_period: int = -1,
                   ns: str = 'default',
                   secrets: Dict[str, Dict[str, str]] = None):
    pass
```

When used in Kallisti, the command should be specified as the following, which
effectively asks Kallisti to terminate 1 pod of the app matching the
"label_selector" running in "your-namespace".

```json
{
  "step": "Terminate pods",
  "do": "k8s.terminate_pods",
  "where": {
    "ns": "your-namespace",
    "label_selector": "selector-of-target-pods",
    "qty": 1,
    "k8s_api_host": "https://api.your-kubernetes.com"
  }
}
```

| Name           | Type     | Default | Required     | Description |
|----------------|----------|---------|--------------|-------------|
| ns             | str      |         | Yes          | The namespace where the target pods are deployed in.
| label_selector | str      |  None   | No           | Filter out the pods based on the given label.
| name_pattern   | str      |  None   | No           | Filter out the pods based on the given pattern. If neither label_selector nor name_pattern are provided, **all** pods in the namespace will be *selected* for termination.
| all            | bool     |  false  | No           | If all is set to True, all matching pods will be terminated.
| rand           | bool     |  false  | No           | If rand is set to True, n random pods will be terminated Otherwise, the first retrieved n pods will be terminated.
| mode           | str      | "fixed" | No           | If mode is set to fixed, then qty refers to number of pods to be terminated. If mode is set to percentage, then qty refers to percentage of pods, from 1 to 100, to be terminated.
| qty            | int      |    1    | No           | Value of qty varies based on mode.
| grace_period   | int      |   -1    | No           | If grace_period is greater than or equal to 0, it will be used as the grace period (in seconds) to terminate the pods. Otherwise, the default pod’s grace period will be used.
| k8s_api_host   | str      |         | Yes for K8s  | Kube API endpoint of target Kubernetes cluster.
| cluster_name   | str      |         | Yes for EKS  | Kubernetes cluster name on EKS.
| region         | str      |         | Yes for EKS  | AWS region of target EKS cluster.

Example for AWS EKS:

The ChaosToolkit command
[scale_microservice](https://docs.chaostoolkit.org/drivers/kubernetes/#scale_microservice)
has the following interface:

```python
def scale_microservice(name: str,
                       replicas: int,
                       ns: str = 'default',
                       secrets: Dict[str, Dict[str, str]] = None):
    pass
```

When used in Kallisti, the command should be specified as the following, which
effectively asks Kallisti to scale the deployment, "your-deployment-name" to `0`
in "your-namespace" of EKS.

```json
{
  "step": "Scale microservice",
  "do": "k8s.scale_microservice",
  "where": {
    "platform": "eks",
    "region": "us-east-1",
    "cluster_name": "my-service-cluster",
    "role": "arn:aws:iam:...",
    "ns": "my-namespace",
    "name": "my-deployment-name",
    "replicas": 0
  }
}
```

| Name           | Type     | Default | Required     | Description |
|----------------|----------|---------|--------------|-------------|
| ns             | str      |         | Yes          | The namespace where the target pods are deployed in.
| name           | str      |         | No           | The name of the deployment.
| replicas       | int      |         | No           | Number of replicas to be scaled to.
| k8s_api_host   | str      |         | Yes for GKP  | Kube API host for GKP such as `https://api.your-kubernetes.com`.
| cluster_name   | str      |         | Yes for EKS  | Kubernetes cluster name on EKS.
| region         | str      |         | Yes for EKS  | AWS region of target EKS cluster.
| role           | str      |         | No           | If you need specify the role for the authorization on EKS.


## Istio

**Namespace:** `istio`

Kallisti supports all the commands provided by
[ChaosToolkit Istio driver](https://docs.chaostoolkit.org/drivers/istio/#exported-activities)
with the appropriate privilege. There are variety of actions to inject chaos on
Istio's virtual service routes including:

* [add_abort_fault](https://docs.chaostoolkit.org/drivers/istio/#add_abort_fault):
  Sets the request fault on the specified routes in a virtual service.
* [add_delay_fault](https://docs.chaostoolkit.org/drivers/istio/#add_delay_fault):
  Sets the delay fault on the specified routes in a virtual service.

In Kallisti, these ChaosToolkit commands can be used in the following way. Istio
is controlled through K8s resources, so these setups below are exactly the same
as the Kubernetes module above:

* `k8s_api_host` is an additional required argument in `where` clause.
* `platform` parameter can be specified with `eks` in `where` clause to target
  AWS EKS. In this case, Kallisti will use `boto3` for the authentication on AWS
  service, so
  [necessary environment parameters](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html#using-environment-variables)
  should be exported in the Kallisti environment. There should also be
  additional parameters in `where` clause to specify the region and cluster.
  Please see the example below.
* `credentials` is an optional argument. If provided, it overriders the default
  credential of
  [Kubernetes Service Account Token File][step-credentials-k8s-svc-acc].
* The `configuration` and `secrets` parameters of ChaosToolkit commands are not 
  needed.

For example:

The ChaosToolkit command
[add_delay_fault](https://docs.chaostoolkit.org/drivers/istio/#add_delay_fault)
has the following interface:

```python
def add_delay_fault(
        virtual_service_name: str,
        fixed_delay: str,
        routes: List[Dict[str, str]],
        percentage: float = None,
        ns: str = 'default',
        version: str = 'networking.istio.io/v1alpha3',
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass
```

When used in Kallisti, the command should be specified as the following, which
effectively asks Kallisti to add latency of 5 seconds for 100% of traffic on the
specified route in the virtual service matching the "virtual_service_name"
running in "your-namespace".

```json
{
      "step": "Add delay fault",
      "do": "istio.add_delay_fault",
      "where": {
        "virtual_service_name": "my-virtual-service",
        "fixed_delay": "5s",
        "percent": 100,
        "routes": [
          {
            "destination": {
              "host": "my-upstream-service",
              "subset": "v1"
            }
          }
        ],
        "ns": "my-namespace",
        "k8s_api_host": "https://api.my-kubernetes.com"
      }
    }
```

| Name                 | Type     | Default | Required     | Description |
|----------------------|----------|---------|--------------|-------------|
| ns                   | str      |         | Yes          | The namespace where the target routes and virtual service are defined in.
| virtual_service_name | str      |  None   | No           | The virtual service name that includes the target routes.
| routes               | list     |  None   | No           | Target routes for the fault injection.
| k8s_api_host         | str      |         | Yes for K8s  | Kube API host for GKP such as `https://api.your-kubernetes.com`. 
| cluster_name         | str      |         | Yes for EKS  | Kubernetes cluster name on EKS.
| region               | str      |         | Yes for EKS  | AWS region of target EKS cluster. 
| role                 | str      |         | No           | If you need specify the role for the authorization on EKS.

## Common

**Namespace:** `cm`

#### http_probe

This command makes an HTTP GET or POST request to the specified URL, including
any HTTP request body and headers that are provided as options. If the response
for the request is not HTTP status code 4xx or 5xx then the step succeeds and
returns the output (see below), else raises a `FailedAction` exception.

> **Note:** 
>
> A 4xx or 5xx status code in the `http_probe` step output will mark the step as
> failed, regardless of whether there is expect condition provided (Refer to
> [Setting Expectations][expectation]). None of the other status codes in the
> `http_probe` step output lead to failure unless a specific status code is
> provided as part of an expect condition. For steps expecting a 4xx or 5xx
> status code, please use [http_request](#http_request) which is not opinionated
> on the step output.

**Arguments:**

| Name            | Type     | Default | Required |
|-----------------|----------|---------|----------|
| url             | str      |         | Yes      |
| method          | str      | "GET"   | Yes      |
| request_body    | Dict     | None    | No       |
| headers         | Dict     | None    | No       |
| authentication* | Dict     | None    | No       |

*Refer to [HTTP Step Authentication][http-step-auth] for details.

**Usage:**

*Example 1:* Simple GET

```json
{
  "step": "HTTP health check",
  "do": "cm.http_probe",
  "where": {
    "url": "https://your-service.com/health"
  }
}
```

*Example 2:* GET with Headers

```json
{
  "step": "HTTP health check",
  "do": "cm.http_probe",
  "where": {
    "url": "https://your-service.com/health",
    "headers": {
      "Content-Type": "text/html; charset=utf-8",
      "Content-Length": "15"
    }
  }
}
```

*Example 3:* POST with Body and Headers

```json
{
  "step": "POST fortune",
  "do": "cm.http_probe",
  "where": {
    "url": "https://your-service.com/fortune",
    "method": "POST",
    "request_body": {"id": "1001", "text": "Fortune favors the brave"},
    "headers": {"Content-Type": "application/json"}
  }
}
```

**Output:**

| Name                     | Type     | Description                      |
|--------------------------|----------|----------------------------------|
| status_code              | int      | Response HTTP status code        |
| response_text            | str      | Response body in string format   |
| response_headers         | dict     | Response HTTP headers            |
| response_time_in_seconds | float    | Time taken between sending the first byte of the request and finishing parsing the headers. |
| response                 | dict     | Parsed response body as an object when response_text is parsable as JSON |


```json
{
  "status_code": 200,
  "response_text": "{\"status\": \"UP\"}",
  "response_headers": {
    "Content-Type": "application/vnd.spring-boot.actuator.v1+json;charset=UTF-8", 
    "Date": "Thu, 14 Feb 2019 03:15:47 GMT", 
    "X-Application-Context": "go-web:cloud:0", 
    "X-Vcap-Request-Id": "b22efa0c-5bb6-488c-62d7-5e36593440f6", 
    "Content-Length": "15"
  },
  "response_time_in_seconds": 1.2,
  "response": {"status": "UP"}
}
```

#### http_request

This command can perform one of following HTTP method for a specified URL:

* GET
* POST
* PUT
* PATCH
* DELETE

The command also allows to specify - request body, headers and authentication
method (See table below for more details).

The command does not fail on any response HTTP status code. In case users want
experiment to fail on certain outcome of response body or HTTP status code they
can:

1. Leverage [expectations][expectation]. Or
2. Use [http_probe](#http_probe). This command enforces opinion to fail on all
   4xx and 5xx requests.

**Arguments:**

| Name            | Type     | Default | Required |
|-----------------|----------|---------|----------|
| url             | str      |         | Yes      |
| method          | str      | "GET"   | Yes      |
| request_body    | Dict     | None    | No       |
| headers         | Dict     | None    | No       |
| authentication* | Dict     | None    | No       |

*Refer to [HTTP Step Authentication][http-step-auth] for details.

**Usage:**

*Example:*

```json
{
  "step": "Check if a fortune message can be updated",
  "do": "cm.http_request",
  "where": {
    "method": "PUT",
    "url": "https://my-fortune-teller-service.com/fortune",
    "request_body": {"id": "1001", "text": "Keep your eye out for someone special."},
    "headers": {"Content-Type": "application/json"}
  },
  "expect": [{
      "operator": "eq",
      "status_code": 200
    }
  ]
}
```

**Output:**

| Name                     | Type     | Description                      |
|--------------------------|----------|----------------------------------|
| status_code              | int      | Response HTTP status code        |
| response_text            | str      | Response body in string format   |
| response_headers         | dict     | Response HTTP headers            |
| response_time_in_seconds | float    | Time taken between sending the first byte of the request and finishing parsing the headers. |
| response                 | dict     | Parsed response body as an object when response_text is parsable as JSON |


```json
{
  "status_code": 200,
  "response_text": "{\"Message\": \"Fortune message updated\"}",
  "response_headers": {
    "Content-Type": "application/json; charset=utf-8", 
    "Date": "Mon, 14 Oct 2019 14:32:39 GMT", 
    "X-Application-Context": "go-web:cloud:0", 
    "X-Vcap-Request-Id": "b22efa0c-5bb6-488c-62d7-5e36593440f6", 
    "Content-Length": "42"
  },
  "response_time_in_seconds": 1.7,
  "response": {"Message": "Fortune message updated"}
}
```

#### wait

Introduces specified wait period (in seconds) during an ongoing trial execution.
The step raises a `FailedAction` exception if invalid arguments are supplied.

**Arguments:**

| Name            | Type     | Default | Required |
|-----------------|----------|---------|----------|
| time_in_seconds | int      |         | Yes      |

**Usage:**
```json
{
  "step": "Wait for 15 seconds",
  "do": "cm.wait",
  "where": {
    "time_in_seconds": 15
  }
}
```

> **Note:** 
> 
> Currently Kallisti supports only synchronous execution of experiments
> (creation of trial). Hence please choose your wait time wisely.

## Prometheus

**Namespace:** `prom`

Kallisti supports the full set of commands provided by
[ChaosToolkit Prometheus driver](https://docs.chaostoolkit.org/drivers/prometheus/#exported-activities).

All commands provided by ChaosToolkit are available in Kallisti and can be used
in the following way:

#### query

Queries Prometheus instance for metrics for a specified time.

**Arguments:**

| Name           | Type     | Default | Required | Description |
|----------------|----------|---------|----------|-------------|
| base_url       | str      |         | Yes      | The base url of prometheus instance.
| query          | str      |         | Yes      | Query for prometheus API.
| when           | str      |         | Yes      | Specifier of time for the query. RFC 3339 date or colloquial expression such as "5 minutes ago" or "now". Check [Date Parser](https://dateparser.readthedocs.io/en/latest/) for details.

**Usage:**
```json
{
  "step": "Query CPU Percentage",
  "do": "prom.query",
  "where": {
    "base_url": "https://your.prometheus.net",
    "query": "firehose_container_metric_cpu_percentage",
    "when": "5 minutes ago"
  }
}
```

#### query_interval

Queries Prometheus instance for metrics for a specified time interval at
specified granularity.

**Arguments:**

| Name           | Type     | Default | Required | Description |
|----------------|----------|---------|----------|-------------|
| base_url       | str      |         | Yes      | The base url of prometheus instance.
| query          | str      |         | Yes      | Query for prometheus API.
| start          | str      |         | Yes      | Specifier of start time for the query. RFC 3339 date or colloquial expression such as "5 minutes ago" or "now". Check [Date Parser](https://dateparser.readthedocs.io/en/latest/) for details.
| end            | str      |         | Yes      | Specifier of end time for the query. RFC 3339 date or colloquial expression such as "5 minutes ago" or "now". Check [Date Parser](https://dateparser.readthedocs.io/en/latest/) for details.
| step           | str      |         | Yes      | Step specifier for granularity of metrics. 

**Usage:**
```json
{
  "step": "Query CPU Percentage for Interval",
  "do": "prom.query_interval",
  "where": {
    "base_url": "https://your.prometheus.net",
    "query": "firehose_container_metric_cpu_percentage",
    "start": "5 minutes ago",
    "end":  "now",
    "step":  50
  }
}
```

## Amazon Web Service

**Namespace:** `aws`

#### ECS | EC2 | Lambda | ELBv2 | ElastiCache | RDS | IAM

Kallisti supports the full set of commands provided by
[ChaosToolkit AWS driver](https://docs.chaostoolkit.org/drivers/aws/). There are
variety of actions to inject chaos on AWS including:

* ECS: [deregister_container_instance](https://docs.chaostoolkit.org/drivers/aws/#deregister_container_instance): Deregisters a given ECS container.
* ECS: [stop_random_tasks](https://docs.chaostoolkit.org/drivers/aws/#stop_random_tasks): Stops a random number of tasks on ECS.
* EC2: [detach_random_volume](https://docs.chaostoolkit.org/drivers/aws/#detach_random_volume): Detaches a random ebs volume (non root) from one or more EC2 instances.
* EC2: [stop_instance](https://docs.chaostoolkit.org/drivers/aws/#stop_instance): Stops a single EC2 instance.
* Lambda: [delete_function_concurrency](https://docs.chaostoolkit.org/drivers/aws/#delete_function_concurrency): Removes concurrency limit applied to the specified Lambda.
* Lambda: [put_function_memory_size](https://docs.chaostoolkit.org/drivers/aws/#put_function_memory_size): Sets the function memory size.
* Lambda: [put_function_timeout](https://docs.chaostoolkit.org/drivers/aws/#put_function_timeout): Sets the function timeout.
* ELBv2: [deregister_target](https://docs.chaostoolkit.org/drivers/aws/#deregister_target): Deregisters one random target from target group.
* RDS: [failover_db_cluster](https://docs.chaostoolkit.org/drivers/aws/#failover_db_cluster): Forces a failover for a DB cluster.
* RDS: [stop_db_instance](https://docs.chaostoolkit.org/drivers/aws/#stop_db_instance): Stops a RDS DB instance.
* and more.

(For chaos testing at K8s-level on EKS, please refer to our
[Kubernetes module](#kubernetes).)

In Kallisti, all the commands can be used in the following way:

* `do` is in `aws.<service>.<action>` format. Examples would be
  `aws.ec2.stop_instance` or `aws.ecs.stop_random_tasks`.
* Kallisti uses `boto3` for the authentication on AWS service, so
  [necessary environment parameters](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html#using-environment-variables)
  should be exported in the Kallisti environment. 
* `credentials` is an optional argument. Refer to 
  [our credential doc page][step-credentials] for details.
* The `configuration` and `secrets` parameters of ChaosToolkit commands are not
  needed.

For example: The ChaosToolkit command
[stop_instance](https://docs.chaostoolkit.org/drivers/aws/#stop_instance) has
the following interface:

```python
def stop_instance(
        instance_id: str = None,
        az: str = None,
        force: bool = False,
        filters: List[Dict[str, Any]] = None,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> List[Dict[str, Any]]:
    pass
```

When used in Kallisti, the command should be specified as the following, which
effectively asks Kallisti to terminate the instance of "your-instance-id" running
in available zone of "your-az-id".

```json
{
  "step": "Stop an EC2 instance in your-za-id",
  "do": "aws.ec2.stop_instance",
  "where": {
    "region": "us-east-1",
    "instance_id": "your-instance-id",
    "az": "your-az-id"
  }
}
```

| Name                          | Type     | Default                                      | Required | Description |
|-------------------------------|----------|----------------------------------------------|----------|-------------|
| region                        | str      |                                              | Yes      | AWS region for the target EC2.
| instance_id                   | str      |                                              | No       | The id of a specific EC2 instance.
| az                            | str      |                                              | No       | The name of availability zone to target.
| role                          | str      |                                              | No       | AWS IAM Role to authenticate for.

> One or both of `instance_id` or `az` will be required. If you only specify the
> `az` parameter, a random instance will be selected under the `az`.

Another example: The ChaosToolkit command
[failover_db_cluster](https://docs.chaostoolkit.org/drivers/aws/#failover_db_cluster)
has the following interface:

```python
def failover_db_cluster(
        db_cluster_identifier: str,
        target_db_instance_identifier: str = None,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass
```
    
When used in Kallisti, the command should be specified as the following, which
effectively asks Kallisti to force the failover on the database instance of
"your-target-db-instance-id" running in the cluster, "your-db-cluster-id".

```json
{
  "step": "Force database failover on RDS",
  "do": "aws.rds.failover_db_cluster",
  "where": {
    "region": "us-east-1",
    "db_cluster_identifier": "your-db-cluster-id",
    "target_db_instance_identifier": "your-target-db-instance-id"
  }
}
```

On top of this, there are overridable parameters for AWS steps as below:

| Name                          | Type     | Default                                      | Required | Description |
|-------------------------------|----------|----------------------------------------------|----------|-------------|
| region                        | str      |                                              | Yes      | AWS region for the target RDS.
| db_cluster_identifier         | str      |                                              | Yes      | The id of RDS cluster.
| target_db_instance_identifier | str      |                                              | Yes      | The id of the target database instance in RDS cluster.
| role                          | str      |                                              | No       | AWS IAM Role to authenticate for.


## Module Exceptions

#### UnknownModuleName
Raised when Kallisti could not find the namespace specified in step definition.

#### CouldNotFindFunction
Raised when Kallisti could not find the command specified in step definition.

#### FailedAction
Raised when Kallisti action execution fails.

[step-credentials]: ./step-credentials.md
[step-credentials-env]: ./step-credentials.md#environment-variables
[step-credentials-k8s-svc-acc]: ./step-credentials.md#kubernetes-service-account-token-file
[expectation]: ./expectation.md
[http-step-auth]: ./http-step-auth.md
