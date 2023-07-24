# SemanticKBLI
Semantic Search Classification using Text Embedding &amp; ElasticSearch

# Tutorial Run Service
1. Create docker container on local.
```
docker build -t fastapi-service .
```
2. Running container
```
docker run -d -p 8000:8000 --name fastapi-container --restart unless-stopped fastapi-service
```

# TODO
- [x] Create Boilerplate System
- [ ] Research Semantic Algorithm
- [ ] Implement Logging System
- [ ] Test on Bulk Request