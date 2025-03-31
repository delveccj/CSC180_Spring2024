FROM python:3.9

# Install dependencies
RUN apt-get update && apt-get install -y \
    net-tools \
    iputils-ping \
    && apt-get clean

COPY config.json .
COPY client.py .
RUN pip install requests mysql-connector-python

CMD ["python", "client.py"]

