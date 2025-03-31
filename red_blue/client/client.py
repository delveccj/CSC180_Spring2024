import time
import requests
import mysql.connector
import socket
import subprocess
import json

# Load config
CONFIG_FILE = "config.json"

def load_config():
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading config file: {e}")
        return {}

config = load_config()

INSTRUCTOR_IP = config.get("instructor_ip", "127.0.0.1")
INSTRUCTOR_PORT = config.get("instructor_port", 5000)
TEAM_NAME = config.get("team_name", socket.gethostname())

SERVER_URL = f"http://{INSTRUCTOR_IP}:{INSTRUCTOR_PORT}/update"

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

    print("\n📡 Sending payload to instructor...")
    print(f"Destination: {SERVER_URL}")
    print(f"Payload: {payload}")

    try:
        response = requests.post(SERVER_URL, json=payload, timeout=2)
        print(f"✅ Sent! Server responded with status {response.status_code}")
    except Exception as e:
        print(f"❌ Failed to send payload: {e}")

    time.sleep(30)
