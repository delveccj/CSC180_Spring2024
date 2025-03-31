from flask import Flask, request, render_template
import time

app = Flask(__name__)
status_map = {}

@app.route('/')
def dashboard():
    return render_template('dashboard.html', status=status_map, time=time.time())

@app.route('/update', methods=['POST'])
def update():
    client_ip = request.remote_addr
    data = request.json

    # 💬 Print raw incoming data
    print("\n--- Incoming POST ---")
    print(f"From IP: {client_ip}")
    print(f"Payload: {data}")

    # Extract team name
    team = data.get('team') or client_ip

    # 💬 Confirm what's being stored
    status_map[team] = {
        "mysql_up": data.get("mysql_up"),
        "remote_connections": data.get("remote_connections"),
        "timestamp": time.strftime('%H:%M:%S')
    }

    print(f"Stored under team: {team}")
    print(f"Current status_map: {status_map}")
    print("--- End POST ---\n")

    return 'OK', 200

if __name__ == '__main__':
    print("🚀 Dashboard server starting up on port 5001...")
    app.run(host='0.0.0.0', port=5001)
