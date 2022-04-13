# Chaos Step Credentials

Kallisti supports using different credentials for different modules by adding
parameters to the `step` field during a chaos experiment. This simplifies the
controls around running chaos experiments in controlled environments, limiting
the failure radius.

You can use this feature by adding a `credentials` parameter to those steps that
require authentication or authorization.

#### Credential Types
 
Kallisti supports the following types of credentials: 

##### Environment Variables

Type value: `ENV_VAR_USERNAME_PASSWORD`
 
Used to retrieve username and password from application's environment variables.
It can be used for any module.
  
For example:
```json
  "credentials": {
    "type": "ENV_VAR_USERNAME_PASSWORD",
    "username_key": "USERNAME",
    "password_key": "PASSWORD"
  }
```
would use the `USERNAME` (See `echo $USERNAME`) and `PASSWORD` (See `echo
$PASSWORD`) from the environment variables set locally.
  
>  **Note:**
>
>  The fields `username_key` and `password_key` contain keywords. Please be
>  careful **NOT** to replace these with your actual ID or password.
 
##### Token File

Type value: `TOKEN_FILE`

Used to retrieve an authentication token from a file in the provided path. It
can be used for any module.
  
For example: 
```json
  "credentials": {
    "type": "TOKEN_FILE",
    "token_path": "/path/to/token/file"
  }
```
 
##### Kubernetes Service Account Token File 

Type value: `K8S_SVC_ACC_TOKEN_FILE`

Used to retrieve an authentication token from the service account token file in
the default location (`/var/run/secrets/kubernetes.io/serviceaccount/token`). It
can be used for `k8s` module and `istio` module.
  
For example: 
```json
  "credentials": {
    "type": "K8S_SVC_ACC_TOKEN_FILE"
  }
```

#### Usage

`credentials` key is placed in the `where` key inside a [step]. They represent
the k8s credentials with developer access to the k8s cluster where you want to
inject Chaos in. See example below:

```json
{
  "step": "Terminate pod",
  "do": "k8s.terminate_pods",
  "where": {
    "label_selector": "app=hello-world",
    "qty": 1,
    "ns": "my-namespace",
    "platform": "EKS",
    "cluster_name": "my-eks-1",
    "region": "us-east-1",
    "credentials": {
      "type": "K8S_SVC_ACC_TOKEN_FILE"
    }
  }
}
```

[Kubernetes]: ./modules.md#kubernetes
[step]: ./concepts.md#step
