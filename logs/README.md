### logs service

**Purpose**

The logs service is responsible for orchestrating the full lifecycle of log processing, from data retrieval to optional persistence and external delivery.

It performs the following tasks:
- fetches raw nginx logs from the nginx service
- parses and validates logs into structured models
- returns processed logs to the user
- optionally exports logs to files (CSV / JSON)
- optionally uploads exported files to external destinations (GitHub)
- enforces request consistency and validation rules

---

### Request processing flow

The main entry point of the logs service is the endpoint: POST /logs

The request is processed step by step according to the provided query parameters.

---

### Step-by-step logic

1. **Log source resolution**

   Logs are retrieved using dependency injection:

   - the `resource` query parameter defines the log source
   - currently supported source: `nginx`
   - raw log lines are fetched over HTTP from the nginx service
   - logs are parsed and validated into `NginxLog` models

2. **Field selection**

   - optional `selected_fields` flags allow the user to choose which fields should be returned
   - field selection affects:
     - the response payload
     - exported files
   - if no fields are selected, full log models are used

3. **Export validation**

   - if `save=true` is provided:
     - the `convert_to` parameter becomes mandatory
     - missing `convert_to` results in a `400 Bad Request`
   - this prevents ambiguous or incomplete export requests

4. **Log export**

   - when export is enabled:
     - logs are converted to the requested format (`csv` or `json`)
     - only selected fields are included if specified
     - a single export file is created
     - the file is saved to the local exports directory
   - the export function returns the path to the generated file

5. **External delivery**

   - if `add_to` is specified, exported data is forwarded accordingly:
     - `github`:
       - the exported file is uploaded to a GitHub repository
       - the GitHub Contents API is used
       - missing directories are created implicitly
       - existing files are overwritten using SHA
     - `db`:
       - not implemented
       - returns an explicit error indicating missing database configuration

6. **Response generation**

   - if `selected_fields` are specified:
     - the response contains only the requested fields
   - otherwise:
     - full validated log models are returned
   - exporting or uploading does not affect the response payload

---

### Design principles

- separation of concerns:
  - log parsing, exporting, and uploading are isolated
- explicit validation:
  - invalid parameter combinations fail early
- predictable behavior:
  - exporting and external delivery do not mutate response data
- extensibility:
  - new export formats or destinations can be added without changing the endpoint logic

## Query parameters

The `POST /logs` endpoint supports the following query parameters, which control how logs are processed, exported, and delivered.

| Parameter | Type | Required | Description |
|----------|------|----------|-------------|
| `resource` | enum | yes | Defines the log source. Currently supported value is `nginx`. |
| `save` | bool | no | Enables exporting logs to a file. Defaults to `false`. |
| `convert_to` | enum | conditionally | Export format. Required when `save=true`. Supported values: `csv`, `json`. |
| `add_to` | enum | no | External destination for logs or exported files. Supported values: `github`, `db`. |
| `selected_fields` | flags | no | A set of boolean flags defining which log fields should be included in the response and export. |

---

### Parameter interaction rules

- `save=true` **requires** `convert_to`  
  If `save` is enabled without specifying `convert_to`, the request fails with `400 Bad Request`.

- `convert_to` has no effect if `save=false`

- `add_to=github`:
  - requires a successfully generated export file
  - uploads the exported file to GitHub

- `add_to=db`:
  - expects structured log models
  - currently not implemented and returns an error

- `selected_fields`:
  - limits fields in the response payload
  - also limits fields included in exported files
  - does not affect internal validation or processing

---

### Examples

Return full logs without exporting: POST /logs?resource=nginx

Return only selected fields: POST /logs?resource=nginx&selected_fields=client_ip&selected_fields=status

Export logs as CSV: POST /logs?resource=nginx&save=true&convert_to=csv

Export logs and upload to GitHub: POST /logs?resource=nginx&save=true&convert_to=csv&add_to=github

## Swagger UI example

The logs service exposes an interactive API documentation using Swagger UI.

After starting the project, Swagger UI is available at: http://localhost:8001/docs

3. Click **“Try it out”**

---

### Example 1: Get full nginx logs

Fill query parameters:

- `resource`: `nginx`

Leave all other parameters empty.

Click **Execute**.

**Result**
- Returns full parsed nginx logs
- No files are created
- No external integrations are triggered

---

### Example 2: Select specific fields

Query parameters:

- `resource`: `nginx`
- `selected_fields`: `client_ip`
- `selected_fields`: `status`
- `selected_fields`: `method`

**Result**
- Response contains only selected fields
- Useful for lightweight responses
- Same selection is applied to exports if enabled

---

### Example 3: Export logs to CSV

Query parameters:

- `resource`: `nginx`
- `save`: `true`
- `convert_to`: `csv`

**Result**
- Logs are exported to a CSV file
- File is saved to: logs/src/exports/
