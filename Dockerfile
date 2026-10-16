FROM ubuntu:26.04

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        ca-certificates curl git nodejs npm python3 ripgrep && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN npm install -g opencode-ai@1.19.3 && npm cache clean --force

CMD ["/bin/bash"]
