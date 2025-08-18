FROM vllm/vllm-openai:gptoss

ENV USERNAME="$USERNAME"
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ Europe/Berlin

ENV VLLM_ATTENTION_BACKEND=TRITON_ATTN_VLLM_V1

RUN echo $USERNAME

COPY . .

RUN  pip3 --no-cache-dir install -r requirements.txt 

RUN apt-get update && apt-get install -y curl

EXPOSE 8008





