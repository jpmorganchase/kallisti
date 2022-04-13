# Access Control on Kallisti API

The Kallisti API enables disruptive activities such as terminating
infrastructure for the critical process of chaos experiments, hence in highly
regulated environments we need to ensure there is a robust access control
mechanism.

Kallisti delegates user management and the generation of access token to
external identity providers in order to meet the control requirements it
typically operates in. There are two ways of protecting Kallisti API using such
external identity providers.

> **Note**
>
> Without setting up any of these options, Kallisti API is NOT protected by
> default. Authentication setup is strongly recommended before deploying
> Kallisti with the credentials for chaos tests.

## Built-in JWT Verification Authentication Class 

There is a built-in authentication class that verifies JWT in the authentication
header upon the request to Kallisti APIs. The token issuer can be any custom
OAuth2/OIDC service or other public user management services such as AWS
Cognito, Okta, Firebase and Auth0.

#### How to Setup

These two environment variables need to be exported for Kallisti's process or
set in the `kallisti/config/settings.py` file:

* `KALLISTI_AUTH_JWKS_URI`: Endpoint to the JWK (JSON Web Key) list.
* `KALLISTI_AUTH_JWT_AUDIENCE`: Audience for the token to be verified on. For
  OIDC this is usually the client ID.
  
Additional parameters can be used in the same `settings.py` file as below for
configuring the authentication on Swagger UI:

* `KALLISTI_AUTH_JWT_TOKEN_ENDPOINT`: OAuth2 token endpoint.
* `KALLISTI_AUTH_URL`: OAuth2 authentication endpoinit.
* `KALLISTI_AUTH_TOKEN_NAME`: OAuth2 token parameter name.
* `KALLISTI_AUTH_CLIENT_ID`: OAuth2 client ID.
* `KALLISTI_AUTH_CLIENT_SECRET`: OAuth2 client secret.

## Custom Authentication Class

In the case where custom authentication type is desired for protecting Kallisti
API, a custom authentication class can be used.

#### How to Setup

The custom authentication class needs to be imported and specified as below in
`kallisti/config/settings.py`:

```
import MyCustomAuthClass
...
# Custom authentication class
KALLISTI_API_AUTH_CLASS = MyCustomAuthClass
```

The parameters for configuring the authentication on Swagger UI can also be used
for the case of custom authentication class.

## Additional Permission

If more granular access control is desired, a custom permission class can be
specified in `kallisti/config/settings.py` as below:

```
import MyCustomPermissionClass
...
# Custom permission class
# KALLISTI_API_PERMISSION_CLASS = MyCustomPermissionClass
```
