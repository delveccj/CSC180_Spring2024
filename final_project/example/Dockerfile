FROM python:3.13-rc-slim

# 🔧 Install required build tools
RUN apt-get update && apt-get install -y build-essential && \
    pip install --upgrade pip setuptools wheel

# Step 1: Copy and build the malicious package
COPY malicious_pkg /malicious_pkg
WORKDIR /malicious_pkg

RUN python3 setup.py sdist && \
    mkdir -p /local_pypi && \
    cp dist/*.tar.gz /local_pypi/

# Step 2: Copy app files and install
WORKDIR /app
COPY requirements.txt install.sh /app/
RUN chmod +x install.sh

# (Optional) Debug output
RUN ls -l /local_pypi

CMD ["./install.sh"]

