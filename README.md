# SemanticKBLI
Semantic Search Classification with Transformers and FastAPI

# Benchmarking

| Source Data | Module         | Algorithm | Acc. Jenis Produk (%) | Acc. KBLI (%)|
|-------------|----------------|-----------|-----------------------|--------------|
| Mei         | Self Declare   | AutoML C# | 56.461                | 48.787       |
| Juni        | Self Declare   | AutoML C# | 56.461                | 83.041       |
| Juni        | Self Declare with Enrichment  | SetFit    | 99.477                | 98.929       |
| Juli        | Reguler        | SetFit    | 98.473                | 98.473       |

# Tutorial Run Service
1. Create docker container on local.
```
docker build -t fastapi-service .
```
2. Running container
```
docker run -d -p 8000:8000 --name fastapi-container --restart unless-stopped fastapi-service
```
3. Access Swagger Documentation via
```
localhost:8000/docs
```

# TODO
- [x] Create Boilerplate System
- [x] Research Semantic Algorithm
- [x] Implement Logging System
- [x] Test on Bulk Request