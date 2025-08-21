```bash
docker compose build  --no-cache
docker compose up -d
docker logs -f vllm-server
```

```bash
...
(APIServer pid=1) INFO:     Started server process [1]
(APIServer pid=1) INFO:     Waiting for application startup.
(APIServer pid=1) INFO:     Application startup complete.
```