from flask import current_app as app, render_template
from .fing_query_api import get_fing_devices

@app.route('/')
def index():
    devices = get_fing_devices()
    up_devices = [d for d in devices if d.get('state') == 'UP']
    down_devices = [d for d in devices if d.get('state') == 'DOWN']
    return render_template('index.html', devices=devices, up_count=len(up_devices), down_count=len(down_devices))
