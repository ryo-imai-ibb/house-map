# Architecture

## 全体構成

```text
[Browser]
   |
   | HTTP
   v
[Frontend: React]
   |
   | REST API
   v
[Backend: FastAPI]
   |
   | SQL
   v
[SQLite]

[Backend: FastAPI]
   |
   | Geocoding API
   v
[Google Maps Platform]