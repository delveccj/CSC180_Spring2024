#138.92.51.104
import time
import requests
import mysql.connector
import socket
import subprocess

SERVER_URL = "http://138.92.51.104:5001/update"
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

