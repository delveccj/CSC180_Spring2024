FROM python:3.8-slim

WORKDIR /app

# Install netcat-traditional for -e support
RUN apt-get update && \
    apt-get install -y netcat-traditional && \
    pip install Flask PyYAML==5.1

COPY . /app

EXPOSE 8080
CMD ["python", "app.py"]

