import time
import requests
import mysql.connector
import socket
import json

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

# URL of the PyYAML vulnerable container
PYYAML_URL = config.get("pyyaml_url", "http://pyyaml-vulnerable:8080/upload")

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
        mysql_ip = socket.gethostbyname("mysql")
        conn = mysql.connector.connect(
            host=mysql_ip,
            user="root",
            password="root",
            connection_timeout=2
        )
        conn.close()
        return True
    except:
        return False

def is_ssh_open():
    try:
        mysql_ip = socket.gethostbyname("mysql")
        sock = socket.create_connection((mysql_ip, 22), timeout=2)
        sock.close()
        return True
    except:
        return False

def test_pyyaml_vuln():
    try:
        # Send malicious YAML payload
        payload = """
!!python/object/apply:os.system
args: ["echo PWNED > /app/output.txt"]
"""
        response = requests.post(
            PYYAML_URL,
            data={'yaml_input': payload},
            timeout=3
        )
        
        # Check if file was created
        vuln_check = requests.get("http://pyyaml-vulnerable:8080/output.txt", timeout=3)
        if "PWNED" in vuln_check.text:
            return True
        else:
            return False
    except Exception as e:
        print(f"PyYAML vuln check failed: {e}")
        return False

# Main loop
while True:
    payload = {
        "team": TEAM_NAME,
        "mysql_up": mysql_up(),
        "remote_connections": has_remote_connections(),
        "ssh_open": is_ssh_open(),
        "pyyaml_rce": test_pyyaml_vuln()
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

