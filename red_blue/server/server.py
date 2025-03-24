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

    # Store the data by client IP
    status_map[client_ip] = {
        "mysql_up": data.get("mysql_up"),
        "remote_connections": data.get("remote_connections"),
        "timestamp": time.strftime('%H:%M:%S')
    }

    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

