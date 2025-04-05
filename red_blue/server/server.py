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
    client_ip = request.remote_addr
    team = data.get('team') or client_ip

    status_map[team] = {
        "mysql_up": data.get("mysql_up"),
        "remote_connections": data.get("remote_connections"),
        "ssh_open": data.get("ssh_open"),
        "pyyaml_rce": data.get("pyyaml_rce"),  # ✅ New: PyYAML vuln status
        "timestamp": time.strftime('%H:%M:%S'),
        "ip_address": client_ip
    }

    print(f"✅ Received update from {team} ({client_ip}): {status_map[team]}")
    print(f"📥 Raw incoming data from {request.remote_addr}: {request.data}")

    return 'OK', 200

if __name__ == '__main__':
    print("🚀 Instructor dashboard running on port 5989...")
    app.run(host='0.0.0.0', port=5989)

