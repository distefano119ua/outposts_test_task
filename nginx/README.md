---

## Services

### nginx service

**Purpose**  
Provides raw nginx access logs over HTTP.

**Endpoint**
GET /logs
---
**Response example**
```json
[
  "162.55.33.98 - - [26/Apr/2021:21:20:17 +0000] \"GET /api HTTP/2.0\" 200 ...",
  "192.168.226.64 - - [26/Apr/2021:21:20:32 +0000] \"GET /metrics HTTP/2.0\" 200 ..."
]
```
---
