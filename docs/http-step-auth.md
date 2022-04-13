# HTTP Step Authentication

Kallisti supports adding authentication to individual steps in a chaos
experiment.

You can use this feature by adding a `authentication` parameter to your steps
which require authentication or authorization.

Currently the feature is supported by the following Kallisti commands:

* `http_probe` of `Common` module (cm.http_probe): See more details about this
  command [here][http_probe].
* `http_request` of `Common` module (cm.http_request): See more details about
  this command [here][http_request].


#### Supported Authentication Types
 
Kallisti supports the following types of authentication for steps:

* OAuth2 Token:
  
  Executes OAuth2 token request and injects the retrieved token will be
  injected into `Authorization` header of the following request.
  
| Name        | Type | Default | Required | Description |
|-------------|------|---------|----------|-------------|
| type        | str  |         | Yes      | `oauth2_token` is currently only supported.
| url         | str  |         | Yes      | Token url of OAuth2 endpoint.
| credentials | Dict |         | Yes      | Credential config to be used. Refer to [Step Credential Handlers][step-creds-handler] for details.
| client      | Dict |         | Yes      | `id` and `secret` required. For public client, `secret` can be omitted or empty.
| resource    | str  |         | No       | Resource identifier for the client to access.
  
  For example:
  ```json
  "authentication": {
        "type": "oauth2_token",
        "url": "https://my-auth-server.com/oauth2/token",
        "credentials": {
          "type": "ENV_VAR_USERNAME_PASSWORD",
          "username_key": "SERVICE_USERNAME",
          "password_key": "SERVICE_PASSWORD"
        },
        "client": {
          "id": "your_oauth_client_id",
          "secret": "your_oauth_client_secret"
        },
        "resource": "your_resource_identifier"
      }
  ```

#### Usage

`authentication` key is placed inside the `where` key inside a [http_probe]
step. Token request of OAuth2 will be executed and the retrieved token will be
injected into "Authorization" header of the following probe request. See
example below:

```json
{
  "step": "POST fortune",
  "do": "cm.http_probe",
  "where": {
    "url": "https://fortune-teller-service.com/fortune",
    "method": "POST",
    "request_body": {"id": "1001", "text": "Fortune favors the brave"},
    "authentication": {
      "type": "oauth2_token",
      "url": "https://my-auth-server.com/oauth2/token",
      "credentials": {
        "type": "ENV_VAR_USERNAME_PASSWORD",
        "username_key": "SERVICE_USERNAME",
        "password_key": "SERVICE_PASSWORD"
      },
      "client": {
        "id": "your_oauth_client_id",
        "secret": "your_oauth_client_secret"
      },
      "resource": "your_resource_identifier"
    }
  }
}
```

[step-creds-handler]: ./step-credentials.md
[http_probe]: modules.md#http_probe
[http_request]: modules.md#http_request