# Expectations

Kallisti allows users to define expectations on output of probes. This allows
Kallisti's chaos tests to succeed or fail conditionally based on the
expectations.

Kallisti allows users to define a list of expectations in the `expect` block.
See the sample below:

```json
{
  "step": "HTTP health check",
  "do": "cm.http_probe",
  "where": {
    "url": "https://my-service.com/health"
  },
  "expect": [{
      "operator": "eq",
      "status_code": 200
    }, {
      "operator": "regex",
      "response_text": "(UP|RUNNING)"
    }, {
      "operator": "eq",
      "response.status": "UP"
    }
  ]
}
```

Each expectation in the list consists of two keys:

* **operator** key - See [operators](#types-of-operators) section for
  supported list of operators
* **field** key:

    * If probe outcome is an integer, string or a boolean value then field key
      is **value**. Example:
    
        ```json
        {
          "operator": "gt",
          "value": 1
        }
        ```

    * If probe outcome is a dictionary then field key indicates the key path. 
      Example: The following block will compare the key *instances* from the 
          result `{"entity": { "instances": 2}}`
    
        ```json
        {
          "operator": "gt",
          "entity.instances": 1
        }
        ```
        
    * If probe outcome is a dictionary including JSON response in
      `response_text`, `response` can be used in field key. Example: The
      following block will compare the value of `id` key inside `data` key
      from JSON response `{"data": { "id": 2}}`
    
        ```json
        {
          "operator": "eq",
          "response.data.id": 1
        }
        ```

## Types of Operators

* [Operator based](#operator-based)
* [Regular Expression based](#regular-expression-based)

### Operator based

You can use from the following operators to compare your probe outcome against
values you expect:

* **ne**: Not equal
* **eq**: Equal
* **le**: Less than and equal to
* **lt**: Less than
* **ge**: Greater than and equal to
* **gt**: Greater than

### Regular Expression based

You can use **regex** as an operator to compare strings against a specified
regular expression pattern.
