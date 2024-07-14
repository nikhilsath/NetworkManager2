from flask import current_app as app, render_template, request, jsonify
import subprocess
import re

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_devices', methods=['POST'])
def check_devices():
    mac_addresses = request.json.get('mac_addresses', [])
    results = []

    for mac in mac_addresses:
        ip = find_ip_by_mac(mac)
        reachable = check_device(ip) if ip else False
        results.append({'mac': mac, 'ip': ip, 'reachable': reachable})

    return jsonify(results)

def find_ip_by_mac(mac):
    try:
        result = subprocess.run(['arp-scan', '-l'], capture_output=True, text=True)
        pattern = re.compile(rf'(\d+\.\d+\.\d+\.\d+)\s+{mac}\s+')
        match = pattern.search(result.stdout)
        if match:
            return match.group(1)
        else:
            return None
    except Exception as e:
        print(f"Error finding IP for MAC {mac}: {e}")
        return None

def check_device(ip):
    try:
        result = subprocess.run(['ping', '-c', '1', ip], capture_output=True, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"Error checking device {ip}: {e}")
        return False
