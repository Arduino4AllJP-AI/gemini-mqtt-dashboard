# Gemini MQTT Dashboard

A web‑based monitoring and control console built on Flask and Flask‑SocketIO. Gemini provides a responsive GUI for subscribing to device topics, viewing real‑time telemetry, and sending control commands over MQTT (including TLS‑secured connections).

---

## Key Features

* **Real‑time Data Streaming** – Instantly updates incoming MQTT messages via WebSockets.
* **TLS/SSL Toggle** – Enable or disable secure MQTT connections with a single checkbox.
* **Credential Management** – Save and overwrite MQTT host, port, username, password, and topic settings directly from the UI.
* **Dynamic Subscriptions** – Subscribe or unsubscribe to multiple topics on the fly without restarting the server.
* **Command Panel** – Publish custom payloads or choose from predefined control commands to any topic.
* **Session Logging** – View live logs with timestamps and export session history as a text file.
* **Responsive Design** – Built with Bootstrap for seamless desktop and mobile use.

---

## Prerequisites

* **Python 3.8+**
* **pip** (Python package manager)
* **Git** (to clone or update the repository)

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Arduino4AllJP-AI/gemini-mqtt-dashboard.git
   cd gemini-mqtt-dashboard
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **First-time setup**

   * Run: `python app.py`
   * In the web UI, enter your MQTT connection details:

     * Host, Port
     * Username & Password (if using TLS)
     * Default Topic to subscribe
   * Click **Save**. Your settings will be stored in `mqtt_credentials.txt`.

---

## Usage

Run the application:

```bash
python app.py
```

* Open your browser to `http://127.0.0.1:8050`.
* Use the sidebar to:

  * Toggle TLS on/off
  * Update MQTT credentials
  * Subscribe/unsubscribe topics
  * Publish commands
* Watch the **Live Log** panel for incoming and outgoing messages.

---

## Configuration Files

* **`mqtt_credentials.txt`** – Stores your MQTT host, port, user, password, and topic.
* **`app.py`** – Main Flask + SocketIO application logic.
* **`templates/index.html`** – Jinja2 template for the dashboard UI.
* **`static/`** – Static assets (CSS, JS, images).
* **`requirements.txt`** – Python package dependencies.

---

## Project Structure

```text
gemini-mqtt-dashboard/
├── app.py
├── requirements.txt
├── README.md
├── mqtt_credentials.txt
├── templates/
│   └── index.html
└── static/
    ├── css/
    ├── js/
    └── images/
```

---

## License

Copyright (c) 2025 Jose Perez

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

👩‍💻 **Happy Monitoring!**
