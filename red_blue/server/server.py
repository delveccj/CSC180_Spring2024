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
    team = data.get('team') or request.remote_addr

    status_map[team] = {
        "mysql_up": data.get("mysql_up"),
        "remote_connections": data.get("remote_connections"),
        "ssh_open": data.get("ssh_open"),
        "timestamp": time.strftime('%H:%M:%S')
    }

    print(f"✅ Received update from {team}: {status_map[team]}")
    return 'OK', 200

if __name__ == '__main__':
    print("🚀 Instructor dashboard running on port 5001...")
    app.run(host='0.0.0.0', port=5001)
