# Customizing Kallisti

Parts of Kallisti are customizable to provide more flexibility in targeting 
different types of platforms for chaos testing. There are also some observers
and hooks useful for things like usage analytics or any other custom events.

* [Authentication and Permission](#authentication-and-permission)
* [Database](#database)
* [Chaos Module Map](#chaos-module-map)
* [Credential Handlers for Chaos Steps](#credential-handlers-for-chaos-steps)
* [Trial Observer](#trial-observer)
* [Trial Creation Hook](#trial-creation-hook)

### Authentication and Permission

Please refer to [access control page][access-control].

### Database

Kallisti uses [Django Rest Framework](https://www.django-rest-framework.org/)
internally for REST API portion. Therefore it is fairly straightforward to
switch the database to other RDBMS. By default the database is SQLite specified
in `settings.py`. Please refer to
[Django documentation](https://docs.djangoproject.com/en/2.2/topics/db/) for the
details of databases and models.

### Chaos Module Map

Kallisti comes with a mapping of chaos injection modules and it is customizable,
which allows us to add custom chaos injection modules for our own needs such as
the chaos injection to internally managed services.

The default mapping is as below. The keys are the module names and the values
are the Python module paths. This map can be edited to enable custom modules.

`kallisticore/config/settings.py`

```python
KALLISTI_MODULE_MAP = {
    'cf': 'kallisticore.modules.cloud_foundry',
    'cm': 'kallisticore.modules.common',
    'k8s': 'kallisticore.modules.kubernetes',
    'istio': 'kallisticore.modules.kubernetes',
    'prom': 'kallisticore.modules.prometheus',
    'aws': 'kallisticore.modules.aws'
}
```

The mechanism for the chaos injection modules to be loaded and for the actions
to be executed is as below. Please refer to `kallisticore/lib/action.py` for the
source code.

* A chaos injection module is loadable as a Python module in the Python
  environment in use.
* The action function is exported with `__all__` list in the module.
* If an action function exists in the dependency of a module, declaring its
  module path in `__actions_modules__` list would expand the modules to be
  searched for the function.
* By default, a step is mapped to the action function as follows: 
  * key-value pairs in `where` clause of a step would be passed to an action
    function as `arguments`
  * `credentials` block of a step would be processed and passed to the action
    function as a `Credential` class
* If additional processing of parameters is required, `__action_class__` can
  be defined in the `__init__.py` of a module and custom `Action` class can be
  specified there. (see `kallisticore/modules/prometheus/__init__.py` as an 
  example.)
  
### Credential Handlers for Chaos Steps

Kallisti comes with a mapping of credential handlers for the chaos injection
steps and it is customizable, which allows us to add custom credential handlers
for our own needs such as the internally-managed identity providers or vault
systems.

The default mapping is as below. The keys are the credential type and the values
are the Python class path. This map can be edited to enable custom credential 
handlers.

`kallisticore/config/settings.py`

```python
KALLISTI_CREDENTIAL_CLASS_MAP = {
    'ENV_VAR_USERNAME_PASSWORD': 'kallisticore.lib.credential.'
                                 'EnvironmentUserNamePasswordCredential',
    'TOKEN_FILE': 'kallisticore.lib.credential.TokenFileCredential',
    'K8S_SVC_ACC_TOKEN_FILE': 'kallisticore.lib.credential.'
                              'KubernetesServiceAccountTokenCredential'
}
```

Custom credential handlers should implement `Credential` base class in
`kallisticore/lib/credential.py`.

### Trial Observer

When one or more custom events are desired to be generated upon the completion
of chaos [trials], the trial observer can be used in Kallisti.

To enable the custom trial observers, `TRIAL_OBSERVERS` variable in
`settings.py` can be used.

`kallisti/config/settings.py`

```python
import MyCustomObserver
#...
# Custom trial observer classes to be executed at trial completion
# They need to implement kallisticore.lib.observe.observer.Observer
TRIAL_OBSERVERS = [MyCustomObserver]
```

As the comment in the above snippet states, custom observers must implement the
`Observer` class in `kalllisticore/lib/observe/observer.py`.

### Trial Creation Hook

When one or more custom events are desired to be generated upon the creation of
chaos [trials] before its execution, the trial creation hook can be used in
Kallisti. The hook functions will take a created trial object as a parameter, so
they can be used to tweak the property of the trial before the execution.

To enable the custom hook upon the creation of [trials],
`TRIAL_TASK_CREATION_HOOKS` variable in `settings.py` can be used.

```python
from my_custom_module import my_hook_func
# Custom trial creation hook functions to be executed at trial creation
TRIAL_TASK_CREATION_HOOKS = [
    # add_token_to_task etc...
    my_hook_func
]
```

[access-control]: ./access-control.md
[step-credentials]: ./step-credentials.md
[trials]: :/concept.md#trial
