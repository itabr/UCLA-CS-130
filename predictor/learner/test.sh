apt-get update && apt-get install -y --allow-downgrades --no-install-recommends \ 
    libcudnn7=7.0.5.15-1+cuda9.1 \
    libcudnn7-dev=7.0.5.15-1+cuda9.1 && \
    rm -rf /var/lib/apt/lists/*
