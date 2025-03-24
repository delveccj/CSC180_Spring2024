## 🚧 The Mission
- 🧑‍🏫 **You (Teacher)**: Run the **Web Server Dashboard**
- 🧑‍🎓 **Students**: Run Dockerized **client agents** that:
  - Check if MySQL is running ✅
  - Check if it has **remote connections** 🔍
  - Report their status back to your server every 30 seconds

---

## 🛠️ Architecture Overview

```plaintext
          🧑‍🏫 Instructor Machine (Server with UI)
              ┌────────────────────────────┐
              │ Web UI: Shows all clients  │
              │ Status: MySQL ✔ | Remote ✔ │
              └────────────────────────────┘
                      ▲            ▲
               JSON POSTs     every 30 sec
                      ▲            ▲
    ┌─────────────────┴────────────┴────────────┐
    │                                           │
 🧑‍🎓 Student A (Client)              🧑‍🎓 Student B (Client)
 [Docker Compose Stack]              [Docker Compose Stack]
 ┌────────────┐                      ┌────────────┐
 │ mysql      │                      │ mysql      │
 │ client.py  │ → sends status       │ client.py  │ → sends status
 └────────────┘                      └────────────┘
```

---

## ✅ The Components

### 🖥️ **Instructor Dashboard (Server)**
- Python + Flask for the backend
- HTML + JavaScript for the live UI
- Receives POSTs from each student’s client:
  ```json
  {
    "team": "Team A",
    "mysql_up": true,
    "remote_connections": true
  }
  ```

### 🐳 **Student Docker Compose Stack**
Contains:
- MySQL with intentionally bad security
- A `client.py` script that:
  - Pings `localhost:3306` to see if MySQL is up
  - Parses `SHOW PROCESSLIST` or `netstat` to see if remote IPs are connected
  - Sends that data to your Flask server every 30 seconds

---

## 🧱 Step-by-Step Build Plan

### 1️⃣ Instructor: Flask Server with Live Dashboard

**server.py**
```python
from flask import Flask, request, render_template
import time

app = Flask(__name__)
status_map = {}

@app.route('/')
def dashboard():
    return render_template('dashboard.html', status=status_map, time=time.time())

@app.route('/update', methods=['POST'])
def update():
    data = request.json
    team = data.get('team')
    status_map[team] = {
        "mysql_up": data.get("mysql_up"),
        "remote_connections": data.get("remote_connections"),
        "timestamp": time.strftime('%H:%M:%S')
    }
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

**templates/dashboard.html**
```html
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="refresh" content="5">
    <style>
        .green { background-color: #c8f7c5; }
        .red { background-color: #f7c5c5; }
        table, th, td { border: 1px solid black; padding: 8px; }
    </style>
</head>
<body>
    <h1>MySQL Service Status Dashboard</h1>
    <table>
        <tr><th>Team</th><th>MySQL</th><th>Remote Conn</th><th>Last Update</th></tr>
        {% for team, stat in status.items() %}
        <tr>
            <td>{{ team }}</td>
            <td class="{{ 'green' if stat.mysql_up else 'red' }}">{{ 'UP' if stat.mysql_up else 'DOWN' }}</td>
            <td class="{{ 'green' if not stat.remote_connections else 'red' }}">{{ 'CLEAN' if not stat.remote_connections else 'REMOTE' }}</td>
            <td>{{ stat.timestamp }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
```

---

### 2️⃣ Students: Docker Compose + Client

**docker-compose.yml**
```yaml
version: '3'
services:
  mysql:
    image: mysql:5.7
    environment:
      MYSQL_ROOT_PASSWORD: root
    ports:
      - "3306:3306"

  client:
    build: ./client
    depends_on:
      - mysql
```

**client/Dockerfile**
```dockerfile
FROM python:3.9
COPY client.py .
RUN pip install requests mysql-connector-python
CMD ["python", "client.py"]
```

**client/client.py**
```python
import time
import requests
import mysql.connector
import socket
import subprocess

SERVER_URL = "http://<teacher-ip>:5000/update"
TEAM_NAME = socket.gethostname()

def mysql_up():
    try:
        conn = mysql.connector.connect(
            host="mysql",
            user="root",
            password="root",
            connection_timeout=2
        )
        conn.close()
        return True
    except:
        return False

def has_remote_connections():
    try:
        output = subprocess.check_output(
            "netstat -an | grep :3306 | grep ESTABLISHED", shell=True
        ).decode()
        for line in output.splitlines():
            if not "127.0.0.1" in line:
                return True
        return False
    except:
        return False

while True:
    payload = {
        "team": TEAM_NAME,
        "mysql_up": mysql_up(),
        "remote_connections": has_remote_connections()
    }
    try:
        requests.post(SERVER_URL, json=payload, timeout=2)
    except:
        pass
    time.sleep(30)
```

---

## 🧪 What the Students Do
1. Build and run:
   ```bash
   docker-compose up --build -d
   ```
2. Their container stack:
   - Runs a **vulnerable MySQL server**
   - Periodically checks status and **reports back to your instructor dashboard**

---

## 🧠 What This Teaches Students
- Using Docker Compose to orchestrate services
- Inter-container communication (client talks to MySQL)
- Basic service health monitoring
- Network awareness: remote vs. local connections
- **Security visibility**: “Oops! Why is someone connected to my DB!?”

---

## 🏁 At a Glance in Class
From your dashboard:
- 🔴 Red = MySQL is down or exposed
- 🟢 Green = Healthy, locked-down service
- You can **watch in real time** as students:
  - Misconfigure things
  - Get breached
  - Fix and defend

---
