# Kallisti

Chaos Engineering Framework across Private / Public / Hybrid Cloud Environments

[![Build Status](https://github.com/jpmorganchase/kallisti/actions/workflows/build.yml/badge.svg)](https://github.com/jpmorganchase/kallisti/actions/workflows/build.yml)

##### Manage Chaos Engineering Practices as Data

Kallisti is a decentralized control plane to test the resiliency of cloud-native
applications by helping you define, execute and manage the chaos experiments. It
abstracts chaos testing capabilities and credential handlers as steps/modules,
allowing the flexible design of chaos testing scenarios in a secure manner.

<img src="./docs/images/kallisti-overview.png" width="600" alt="kallisti experiment overview"/>

###### Background

Project Kallisti is the open-source fork of a chaos engineering framework that
originally started within JPMorgan Chase in 2018. Today, Kallisti is used by a
number of applications for chaos testing within JPMorgan Chase. It is now the
upstream source of our internal chaos engine and continues to be actively
maintained. Keep an eye on our [roadmap][roadmap] for more to come!

#### Chaos Injection Capabilities

Kallisti ships with a number of chaos injection capabilities in various modules
based on the different [Chaostoolkit](https://github.com/chaostoolkit) libraries.
Additional chaos injection can also be developed and imported into Kallisti.
Check out the [customization page][customization] for more details.

| Component            | Module | Capabilities                                              |
|----------------------|--------|-----------------------------------------------------------|
| Kubernetes / AWS EKS | k8s    | Pod / replicaset termination, network drop and more.      |
| Istio                | istio  | Envoy's HTTP fault / latency filters.                     |
| AWS                  | aws    | EC2/ECS/RDS/ELB termination, Lambda restriction and more. |
| Cloud Foundry        | cf     | Container / service termination, network drop and more.   |
| Prometheus           | prom   | Metrics data retrieval with PromQL.                       |
| Common               | cm     | HTTP probe/requests and wait.                             |

### List of Contents

#### Project

* [Concept][concept]: overview and concept of Kallisti.
* [Road Map][roadmap]: what is planned for Kallisti in future.
* [Contribution to Kallisti][contribution]: guideline for contribution.

#### Getting Started

* [How to Use Kallisti][how-to-use]: deployment to chaos test execution.
* [Chaos Modules][modules]: chaos injection modules and capabilities.
* [Credentials for Chaos Steps][step-credentials]: credentials for chaos testing
  steps.
* [Access Control][access-control]: controlling the access to Kallisti API
  through OAuth2/OIDC integration (via JWT tokens) or any other authentication
  mechanism through a custom configuration.
* [Customization][customization]: custom modules, credentials, hooks and more.

#### Other Features

* [Result Validation][expectation]: result of each step in a chaos experiment
  can be verified to specific values or range expected.
* [Experiment Templating][experiment-template]: experiment definition can be
  interpolated with parameters.
* [Authentication for HTTP steps][http-step-auth]: auth for HTTP request steps.
* [Scheduling][scheduling]: recurring experiments with cron expression.
* [Reporting][reporting]: xml export through API.
<!--* [Notification][notification]: email upon completion of an experiment.-->

[access-control]: ./docs/access-control.md
[contribution]: ./docs/contribution.md
[customization]: ./docs/customization.md
[expectation]: ./docs/expectation.md
[experiment-template]: ./docs/experiment-template.md
[how-to-use]: ./docs/how-to-use.md
[modules]: ./docs/modules.md
[notification]: ./docs/notification.md
[concept]: ./docs/concept.md
[reporting]: ./docs/reporting.md
[roadmap]: ./docs/roadmap.md
[scheduling]: ./docs/scheduling.md
[http-step-auth]: ./docs/http-step-auth.md
[step-credentials]: ./docs/step-credentials.md
