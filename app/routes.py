from flask import current_app as app, render_template, request, jsonify
import subprocess
import re

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_devices', methods=['POST'])
def check_devices():
    ip_range = request.json.get('ip_range', '192.168.68.0/24')  # Get IP range from the request or use default
    devices = run_arp_scan(ip_range)  # Run the arp-scan command
    return jsonify(devices)  # Return the results as JSON

def run_arp_scan(ip_range):
    try:
        result = subprocess.run(['sudo', 'arp-scan', ip_range], capture_output=True, text=True)  # Run sudo arp-scan
        return parse_arp_scan_output(result.stdout)  # Parse the output
    except Exception as e:
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
