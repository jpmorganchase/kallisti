# Scheduling Experiment Execution

Kallisti allows you to schedule the execution of your chaos experiments.

## Create a Schedule

It is assumed that you have created an experiment to be scheduled. Please
refer to our tech primer documents to find out how to create experiments.

1. Go to Swagger UI of your deployed Kallisti application.
2. Go to `experiment` > `POST /experiment/{experiment_id}/schedule`
3. Press `Try it out` button.
4. Enter the `ID of your experiment` which is retrievable from
   `GET /experiment` into `experiment_id` parameter box.
5. Fill out the `data` text box and press `Execute` button.

**Arguments:**

| Name                 | Type | Default | Required | Description |
|--------------------- | ---- | --------| ---------| ------------|
| [metadata][metadata] | dict |         | No       | Key value pairs that can be used to label a set of schedules.
| recurrence_pattern   | str  |         | Yes      | Cron expression for the schedule.
| recurrence_count     | int  |         | No       | Recurrence count which gets decremented at each execution from schedule.
| parameters           | dict |         | No       | Run-time parameters for scheduled experiments.
| ticket               | dict |         | No       | Ticket data for scheduled experiments.

> **Note:** 
>
> When `recurrence_count` is not set, schedule will keep executing the
> experiments. Scheduling experiments indefinitely should be considered
> carefully. This setting can be updated from `PUT` or
> `PATCH /experiment/{experiment_id}/schedule/{schedule_id}`.

## Retrieve Schedules and Trials Executed

Schedule entries can be retrieved via these two endpoints.
- `GET /experiment/{experiment_id}/schedule`
- `GET /experiment/{experiment_id}/schedule/{schedule_id}`

When `schedule_id` is specified in the url, the response will be an object of
schedule while the response will be a list of schedules when `schedule_id` is
not specified.

The schedule object in the response will have `trials` parameter including the
brief information of the trials executed under the schedule. To retrieve the
log record, `GET /trial/{id}` can be used with the `trial_id` in `trials`
parameter. 

```json
{
  "id": "73919897-0835-4ad6-bfc6-2b332c9d615f",
  "experiment_id": "d4e4a9cd-d97a-472c-977b-9f92338db2e1",
  "parameters": {},
  "ticket": {},
  "recurrence_pattern": "*/5 * * * *",
  "recurrence_count": 1,
  "recurrence_left": 0,
  "created_by": "a123456",
  "created_at": "2019-06-17T04:34:07.014023Z",
  "trials": [
    {
      "id": "1cb25d87-a126-4d4f-8ac6-77d8922f3001",
      "status": "Succeeded",
      "executed_at": "2019-06-17T04:34:15.132562Z"
    }
  ]
}
```

## Update & Delete a Schedule

Endpoints:

- `PUT /experiment/{experiment_id}/schedule/{schedule_id}`
- `PATCH /experiment/{experiment_id}/schedule/{schedule_id}`
- `DELETE /experiment/{experiment_id}/schedule/{schedule_id}`

are available to update or delete a schedule.

> **Notes:** 
>
> * When `recurrence_count` is updated with a new number, `recurrence_left`
> (remaining recurrence count) will be reset with the new number no matter how
> many trials have been executed or are left till then.
>
> * When an experiment entity is deleted, the schedule(s) for the deleted
>   experiment will also be deleted in a cascading manner.

## Limitation

* Kallisti runs single worker process to execute experiments at the moment. This
  is to avoid the complexity and risks of concurrent trial execution, therefore
  experiments will be executed in scheduled order sequentially when schedules
  and execution overlap. E.g. when a trial takes 30 minutes from 0:00AM and
  another experiment is scheduled at 0:15AM, this scheduled trial will be only
  executed at 0:30AM.

[metadata]: ./concepts.md#metadata