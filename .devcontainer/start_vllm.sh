#!/usr/bin/env bash
vllm serve openai/gpt-oss-120b --gpu-memory-utilization 0.95 --tensor-parallel-size 2 --download-dir /app/vllm --port 8008

