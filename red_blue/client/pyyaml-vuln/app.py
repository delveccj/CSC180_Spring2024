from flask import Flask, request, render_template, send_file
import yaml

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    yaml_input = request.form.get('yaml_input', '')
    try:
        # 🚨 VULNERABLE LINE
        yaml.load(yaml_input, Loader=yaml.UnsafeLoader)
        return "✅ YAML processed!"
    except Exception as e:
        return f"❌ Error: {e}"

@app.route('/output.txt')
def get_output():
    return send_file("/app/output.txt", mimetype='text/plain')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
