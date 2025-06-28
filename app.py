import eventlet
eventlet.monkey_patch()

import os
import threading
import time
import webbrowser
import ssl
from datetime import datetime

from flask import Flask, render_template, request, jsonify, Response
from flask_socketio import SocketIO, emit
import google.generativeai as genai
import paho.mqtt.client as mqtt

# ——— Config ———
API_KEY_FILE       = 'APIKEY.txt'
MQTT_CRED_FILE     = 'mqtt_credentials.txt'
MEMORY_FILE        = 'memory.txt'
MAX_LOG            = 100

# ——— In-memory logs ———
incoming_log = []
ai_log       = []
command_log  = []

def read_api_key():
    try:
        return open(API_KEY_FILE).read().strip()
    except FileNotFoundError:
        return None

def read_memory():
    try:
        return open(MEMORY_FILE).read().strip()
    except FileNotFoundError:
        return ""

def load_mqtt_credentials():
    creds = {}
    try:
        with open(MQTT_CRED_FILE) as f:
            for line in f:
                if '=' in line:
                    k, v = line.strip().split('=', 1)
                    creds[k] = v.strip()
    except FileNotFoundError:
        pass

    return (
        creds.get('host') or None,
        int(creds.get('port','0')),
        creds.get('user') or None,
        creds.get('pass') or None,
        creds.get('topic') or None,
        creds.get('tls','false').lower() == 'true'
    )

# Load API key
api_key = read_api_key()
if api_key:
    genai.configure(api_key=api_key)
    print("✅ Google AI API key loaded.")
else:
    print("❌ Google AI API key NOT found.")

# Load MQTT creds (host, port, user, pass, topic, use_tls)
MQTT_HOST, MQTT_PORT, MQTT_USER, MQTT_PASS, MQTT_DEFAULT_TOPIC, MQTT_USE_TLS = load_mqtt_credentials()

mqtt_client    = None
mqtt_connected = False

# ——— MQTT callbacks ———
def on_connect(client, userdata, flags, rc):
    global mqtt_connected
    mqtt_connected = (rc == 0)
    status = 'Connected' if mqtt_connected else f'Connection failed (rc={rc})'
    color  = 'green' if mqtt_connected else 'red'
    socketio.emit('status_update', {
        'api_key': api_key is not None,
        'mqtt':    {'status': status, 'color': color}
    })
    if mqtt_connected and MQTT_DEFAULT_TOPIC:
        client.subscribe(MQTT_DEFAULT_TOPIC)

def on_disconnect(client, userdata, rc):
    global mqtt_connected
    mqtt_connected = False
    socketio.emit('status_update', {
        'api_key': api_key is not None,
        'mqtt':    {'status': 'Disconnected', 'color': 'red'}
    })

def on_message(client, userdata, msg):
    payload = msg.payload.decode(errors='ignore')
    socketio.emit('mqtt_message', {
        'topic': msg.topic,
        'payload': payload
    })
    ts = datetime.utcnow().isoformat()
    incoming_log.append(f"{ts} {msg.topic}: {payload}")
    if len(incoming_log) > MAX_LOG:
        incoming_log.pop(0)

# ——— Start or restart MQTT client ———
def start_mqtt():
    global mqtt_client
    if not MQTT_HOST:
        return
    mqtt_client = mqtt.Client()
    if MQTT_USER and MQTT_PASS:
        mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)

    if MQTT_USE_TLS:
        mqtt_client.tls_set(
            ca_certs=None,
            cert_reqs=ssl.CERT_NONE,
            tls_version=ssl.PROTOCOL_TLS_CLIENT
        )
        mqtt_client.tls_insecure_set(True)

    mqtt_client.on_connect    = on_connect
    mqtt_client.on_disconnect = on_disconnect
    mqtt_client.on_message    = on_message

    # retry loop
    while True:
        try:
            mqtt_client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
            mqtt_client.loop_start()
            break
        except Exception as e:
            print("MQTT connect failed:", e)
            time.sleep(5)

# ——— Flask + SocketIO setup ———
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET', 'change_me')
socketio = SocketIO(app, async_mode='eventlet')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_api_key', methods=['POST'])
def save_api_key():
    data    = request.json or {}
    new_key = data.get('api_key','').strip()
    if not new_key:
        return jsonify({'success': False, 'error': 'No API key provided'}), 400
    try:
        with open(API_KEY_FILE, 'w') as f:
            f.write(new_key)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    global api_key
    api_key = new_key
    genai.configure(api_key=api_key)
    socketio.emit('status_update', {
        'api_key': True,
        'mqtt':    {'status': 'Connected' if mqtt_connected else 'Disconnected',
                    'color':  'green'   if mqtt_connected else 'red'}
    })
    return jsonify({'success': True})

@app.route('/save_mqtt', methods=['POST'])
def save_mqtt():
    data = request.json or {}
    try:
        lines = [
            f"host={data.get('host','')}",
            f"port={data.get('port','')}",
            f"user={data.get('user','')}",
            f"pass={data.get('pass','')}",
            f"topic={data.get('topic','')}",
            f"tls={'true' if data.get('tls') else 'false'}"
        ]
        with open(MQTT_CRED_FILE, 'w') as f:
            f.write("\n".join(lines))
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

    # reload creds and restart MQTT
    global MQTT_HOST, MQTT_PORT, MQTT_USER, MQTT_PASS, MQTT_DEFAULT_TOPIC, MQTT_USE_TLS
    MQTT_HOST, MQTT_PORT, MQTT_USER, MQTT_PASS, MQTT_DEFAULT_TOPIC, MQTT_USE_TLS = load_mqtt_credentials()
    threading.Thread(target=start_mqtt, daemon=True).start()
    socketio.emit('status_update', {
        'api_key': api_key is not None,
        'mqtt':    {'status': 'Connected', 'color': 'green'}
    })
    return jsonify({'success': True})

@app.route('/generate', methods=['POST'])
def generate():
    data        = request.json or {}
    user_prompt = data.get('prompt','').strip()
    history     = data.get('history','').strip()

    parts = []
    mem = read_memory()
    if mem: parts.append(mem)
    if history: parts.append(history)
    parts.append(user_prompt)
    full_prompt = "\n\n".join(parts).strip()
    if not full_prompt:
        return jsonify({'error':'Nothing to send'}), 400

    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        resp  = model.generate_content(full_prompt)
        text  = getattr(resp, 'text', '')
        ts    = datetime.utcnow().isoformat()
        ai_log.append(f"{ts} {text}")
        if len(ai_log)>MAX_LOG: ai_log.pop(0)
        return jsonify({'response': text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/export_log')
def export_log():
    lines = ['=== AI Responses ==='] + ai_log
    lines += ['', '=== Published Commands ==='] + command_log
    lines += ['', '=== Incoming MQTT ==='] + incoming_log
    out   = "\n".join(lines)
    return Response(out,
                    mimetype='text/plain',
                    headers={'Content-Disposition':'attachment;filename=events.txt'})

@socketio.on('connect')
def ws_connect():
    socketio.emit('status_update', {
        'api_key': api_key is not None,
        'mqtt':    {'status': 'Connected' if mqtt_connected else 'Disconnected',
                    'color':  'green'   if mqtt_connected else 'red'}
    })

@socketio.on('subscribe')
def handle_subscribe(data):
    t = data.get('topic','').strip()
    if t and mqtt_client:
        mqtt_client.subscribe(t)
        emit('subscribed', {'topic': t})

@socketio.on('publish')
def handle_publish(data):
    t = data.get('topic','').strip()
    m = data.get('message','')
    if t and mqtt_client:
        mqtt_client.publish(t, m)
        ts = datetime.utcnow().isoformat()
        command_log.append(f"{ts} {t}: {m}")
        if len(command_log)>MAX_LOG: command_log.pop(0)
        emit('published', {'topic': t})

def open_browser():
    time.sleep(1)
    webbrowser.open_new_tab('http://127.0.0.1:5100/')

if __name__ == '__main__':
    threading.Thread(target=start_mqtt,   daemon=True).start()
    threading.Thread(target=open_browser, daemon=True).start()
    socketio.run(app,
                 host='0.0.0.0',
                 port=5100,
                 debug=True,
                 use_reloader=False,
                 allow_unsafe_werkzeug=True)
