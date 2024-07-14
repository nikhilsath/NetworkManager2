import os
import json
from flask import current_app as app, render_template, request, jsonify
import subprocess
import requests

@app.route('/')
def index():
    """
    Render the index page.
    """
    return render_template('index.html')

@app.route('/check_devices', methods=['POST'])
def check_devices():
    """
    Endpoint to check devices on the network by scanning the specified IP range.
    """
    ip_range = request.json.get('ip_range', '192.168.68.0/24')
    devices = run_arp_scan(ip_range)
    return jsonify(devices)

@app.route('/ping_device', methods=['POST'])
def ping_device():
    """
    Endpoint to ping a specified device IP to check its reachability.
    """
    ip = request.json.get('ip')
    success = run_ping(ip)
    return jsonify({'success': success})

@app.route('/scan_volumes', methods=['POST'])
def scan_volumes():
    """
    Endpoint to scan volumes on a specified device IP.
    """
    mac = request.json.get('mac')
    ip = request.json.get('ip')
    headers = {'Mac-Address': mac}
    message = send_command_to_agent(ip, 'ls /Volumes', headers)
    
    # Save the volumes information to a JSON file
    volumes_path = f"data/{mac}_volumes.json"
    try:
        with open(volumes_path, 'w') as file:
            json.dump(message.split('\n'), file)
        print(f"Volumes information saved to {volumes_path}")
    except Exception as e:
        print(f"Error writing volumes file: {e}")
    
    return jsonify({'message': message})

@app.route('/get_volumes_info/<mac>', methods=['GET'])
def get_volumes_info(mac):
    """
    Endpoint to get volumes information for a specified MAC address.
    """
    print(f"Getting volumes info for MAC: {mac}")
    volumes_path = f"data/{mac}_volumes.json"
    if os.path.exists(volumes_path):
        try:
            with open(volumes_path, 'r') as file:
                volumes_data = json.load(file)
            print(f"Volumes data loaded: {volumes_data}")
            return jsonify({'volumes': volumes_data})
        except json.JSONDecodeError as e:
            print(f"Error reading volumes file: {e}")
            return jsonify({'volumes': ['Error reading volumes file - invalid JSON']})
        except Exception as e:
            print(f"Error reading volumes file: {e}")
            return jsonify({'volumes': ['Error reading volumes file']})
    print("Volumes file not found")
    return jsonify({'volumes': ['No volumes found']})

@app.route('/generate_scripts', methods=['POST'])
def generate_scripts():
    """
    Endpoint to generate scripts for the volumes found.
    """
    mac = request.json.get('mac')
    volumes = request.json.get('volumes')
    
    # Create scripts for each volume
    scripts_path = f"data/{mac}_scripts"
    os.makedirs(scripts_path, exist_ok=True)
    
    for volume in volumes:
        script_content = f"#!/bin/bash\n# Script for volume {volume}\n\n"
        script_filename = os.path.join(scripts_path, f"{volume.replace('/', '_')}.sh")
        with open(script_filename, 'w') as script_file:
            script_file.write(script_content)
        os.chmod(script_filename, 0o755)  # Make the script executable
    
    return jsonify({'message': 'Scripts generated successfully'})

def run_arp_scan(ip_range):
    """
    Run arp-scan on the specified IP range to discover devices.
    """
    try:
        result = subprocess.run(['sudo', 'arp-scan', ip_range], capture_output=True, text=True)
        result.check_returncode()
        return parse_arp_scan_output(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running arp-scan: {e}")
        return []

def parse_arp_scan_output(output):
    """
    Parse the output of arp-scan and extract device information.
    """
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
    """
    Run a ping command to check if the specified IP is reachable.
    """
    try:
        result = subprocess.run(['ping', '-c', '1', ip], capture_output=True, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"Error pinging IP {ip}: {e}")
        return False

def send_command_to_agent(ip, command, headers):
    """
    Send a command to the agent running on the specified IP.
    """
    try:
        url = f"http://{ip}:8080"
        response = requests.post(url, data=command, headers=headers, timeout=5)  # Adding a 5-second timeout
        if response.status_code == 200:
            return response.text
        else:
            return f"Error: {response.status_code}"
    except requests.Timeout:
        print(f"Error: Request to {ip} timed out")
        return f"Error: Request to {ip} timed out"
    except requests.ConnectionError as e:
        print(f"Error sending command to agent: {e}")
        return f"Error sending command to agent: {e}"
    except Exception as e:
        print(f"Error sending command to agent: {e}")
        return f"Error sending command: {e}"

# Ensure the data directory exists
os.makedirs('data', exist_ok=True)
