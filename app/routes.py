import os
from flask import current_app as app, render_template, request, jsonify
import subprocess
import requests

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_devices', methods=['POST'])
def check_devices():
    ip_range = request.json.get('ip_range', '192.168.68.0/24')
    devices = run_arp_scan(ip_range)
    return jsonify(devices)

@app.route('/ping_device', methods=['POST'])
def ping_device():
    ip = request.json.get('ip')
    success = run_ping(ip)
    return jsonify({'success': success})

@app.route('/scan_volumes', methods=['POST'])
def scan_volumes():
    mac = request.json.get('mac')
    ip = request.json.get('ip')
    message = send_command_to_agent(ip, 'ls /Volumes')
    return jsonify({'message': message})

@app.route('/get_volumes_info/<mac>', methods=['GET'])
def get_volumes_info(mac):
    volumes_path = f"data/{mac}_volumes.json"
    if os.path.exists(volumes_path):
        with open(volumes_path, 'r') as file:
            volumes_data = file.read()
        return jsonify({'volumes': volumes_data.split('\n')})
    return jsonify({'volumes': ['No volumes found']})

def run_arp_scan(ip_range):
    try:
        result = subprocess.run(['sudo', 'arp-scan', ip_range], capture_output=True, text=True)
        result.check_returncode()
        return parse_arp_scan_output(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running arp-scan: {e}")
        return []

def parse_arp_scan_output(output):
    devices = []
    lines = output.split('\n')
    for line in lines:
        if line and not line.startswith(('Interface', 'Starting', 'Ending', 'Packets')):
            parts = line.split()
            if len(parts) >= 2:
                devices.append({
                    'ip': parts[0],
                    'mac': parts[1],
                    'vendor': ' '.join(parts[2:]) if len(parts) > 2 else 'Unknown'
                })
    return devices

def run_ping(ip):
    try:
        result = subprocess.run(['ping', '-c', '1', ip], capture_output=True, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"Error pinging IP {ip}: {e}")
        return False

def send_command_to_agent(ip, command):
    try:
        url = f"http://{ip}:8080"
        response = requests.post(url, data=command)
        if response.status_code == 200:
            return response.text
        else:
            return f"Error: {response.status_code}"
    except Exception as e:
        print(f"Error sending command to agent: {e}")
        return f"Error sending command: {e}"

# Ensure the data directory exists
os.makedirs('data', exist_ok=True)
