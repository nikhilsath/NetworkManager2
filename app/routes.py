from flask import current_app as app, render_template, request, jsonify
import subprocess

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_devices', methods=['POST'])
def check_devices():
    mac_addresses = request.json.get('mac_addresses', [])
    results = []

    for mac in mac_addresses:
        result = check_device(mac)
        results.append({'mac': mac, 'reachable': result})

    return jsonify(results)

def check_device(mac):
    try:
        # Replace 'arp-scan' with the appropriate command to check MAC address on your system
        result = subprocess.run(['arp-scan', '-l'], capture_output=True, text=True)
        return mac in result.stdout
    except Exception as e:
        print(f"Error checking device {mac}: {e}")
        return False
