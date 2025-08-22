# vLLM Server Setup

This repository provides a ready-to-use **Docker Compose** setup to run a [vLLM](https://github.com/vllm-project/vllm) server with the **OpenAI-compatible API**.  
It is configured for large-scale models (here: `openai/gpt-oss-120b`) and GPU acceleration with NVIDIA.

---

## 🚀 Quick Start

1. **Clone this repository** (or copy the `docker-compose.yml` into your project):

   ```bash
   git clone https://github.com/Perpetue237/agentsculptor
   cd agentsculptor/vllm-server-config
   ```

2. **Start the vLLM server:**

    ```bash
    docker compose up -d
    ```

3. **Verify that the container is running:**

    ```bash
    docker ps
    ```

4. **The vLLM server will be available at:**

    http://localhost:8008/v1/

### ⚙️ Configuration Details
docker-compose.yml

```bash
services:
  vllm:
    image: vllm/vllm-openai:gptoss
    container_name: vllm-server
    command: >
      --model openai/gpt-oss-120b
      --gpu-memory-utilization 0.95
      --tensor-parallel-size 2
      --download-dir /raid/vllm
      --port 8008
      --no-enable-prefix-caching
    shm_size: "64gb"
    ulimits:
      memlock: -1
      stack: 67108864
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              device_ids: ["5,6"]
              capabilities: [gpu]
    volumes:
      - /raid/vllm:/raid/vllm
    ports:
      - "8008:8008"
    environment:
      VLLM_ATTENTION_BACKEND: TRITON_ATTN_VLLM_V1
```

### Breakdown of Key Options

* Image:
  
    `vllm/vllm-openai:gptoss` — vLLM container with OpenAI-compatible REST API.

* Command Arguments:

    * `--model openai/gpt-oss-120b` → Which model to serve.

    * `--gpu-memory-utilization 0.95` → Allow GPU memory usage up to 95%.

    * `--tensor-parallel-size 2` → Use 2 GPUs in tensor parallel mode.

    * `--download-dir /raid/vllm` → Directory for caching/downloaded weights.

    * `--port 8008` → Server will listen on port 8008.

    * `--no-enable-prefix-caching` → Disables prefix caching (useful for memory-heavy workloads).

* GPU Resources:

    * Uses NVIDIA GPU devices 5 and 6.

    * Requires NVIDIA Container Toolkit.

* Volumes:

    Maps `/raid/vllm` (on host) → `/raid/vllm` (in container).
    This persists model weights & avoids re-downloading.

* Ports:

    `Exposes 8008:8008` (host:container).

* Shared Memory & ulimits:

    * `shm_size: "64gb"` → Required for large tensor operations.

    * `ulimits` → Removes memory locking restrictions.

* Environment:

    * `VLLM_ATTENTION_BACKEND=TRITON_ATTN_VLLM_V1` → Use optimized attention kernel.

## 📡 Using the API

You can interact with the server using any OpenAI-compatible client. For example, with curl:

```bash
curl http://localhost:8008/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openai/gpt-oss-120b",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Hello! Can you explain tensor parallelism?"}
    ]
  }'
  ```
with Python using requests:

```python
import requests

url = "http://localhost:8008/v1/chat/completions"

payload = {
    "model": "openai/gpt-oss-120b",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain tensor parallelism in simple terms."}
    ],
    "max_tokens": 200
}

response = requests.post(url, json=payload)

if response.ok:
    data = response.json()
    print("Response:")
    print(data["choices"][0]["message"]["content"])
else:
    print("Error:", response.status_code, response.text)
```

Or with the official OpenAI Python client:

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8008/v1", api_key="dummy")

resp = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[{"role": "user", "content": "Hello from vLLM!"}]
)

print(resp.choices[0].message.content)
```

## 🛠️ Requirements

* Docker and Docker Compose

* NVIDIA drivers and NVIDIA Container Toolkit
(for GPU passthrough)

* Sufficient GPU memory (2× high-memory GPUs for gpt-oss-120b)

## 🧰 Useful Commands

Check logs:

```bash
docker compose logs -f vllm
```

Restart the server:

```bash
docker compose restart vllm
```

Stop everything:

```bash
docker compose down
```

## 📖 Notes

* If you want prefix caching, remove --no-enable-prefix-caching.

* To use a smaller model, replace openai/gpt-oss-120b with another model supported by vLLM.

* Adjust device_ids depending on which GPUs you want to allocate.

## 📜 License

This setup is released under the Apache-2.0  [LICENSE](LICENSE) (same as vLLM).