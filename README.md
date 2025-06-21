# Gemini MQTT Dashboard

A web‑based monitoring and control console built on Flask, Flask‑SocketIO, and MQTT. Gemini provides a responsive GUI for subscribing to device topics, viewing real‑time telemetry, and sending control commands over MQTT (including TLS‑secured connections).

---

## Key Features

* **Real‑time Data Streaming** – Updates incoming messages instantly using WebSockets.
* **TLS/SSL Toggle** – Easily switch between secure (TLS) and anonymous connections via a checkbox.
* **Credential Management** – Save and overwrite MQTT host, port, user, password, and topic settings through the UI.
* **Topic Subscription** – Dynamically subscribe to multiple topics without restarting the server.
* **Command Panel** – Publish custom payloads or preconfigured control commands to any topic.
* **Logging & History** – View and export session logs, including timestamps and topic details.
* **Clean, Responsive UI** – Built with Bootstrap; adapts to desktop and mobile screens.

---

## Prerequisites

* **Python 3.8+**
* **pip** (Python package manager)
* **Git** (to clone the repo)

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

3. **Set up credentials**

   * On first launch, you’ll be prompted to enter:

     * MQTT Host & Port
     * Username & Password (if using TLS)
     * Default Subscription Topic
   * These will be saved to `mqtt_credentials.txt` (or `APIKEY.txt` for API key storage).

---

## Usage

```bash
python app.py
```

* Open your browser at `http://127.0.0.1:8050` (or the port you configured).
* Use the sidebar to:

  * Toggle TLS on/off
  * Update credentials
  * Subscribe or unsubscribe topics
  * Publish commands
* View incoming messages in the live log panel.

---

## Configuration Files

* **app.py** – Main Flask + SocketIO application.
* **templates/index.html** – HTML template for the dashboard.
* **static/** – Static assets (CSS, JS, icons, images).
* **mqtt\_credentials.txt** – Stored MQTT connection details.
* **APIKEY.txt** – Optional file for storing an API key if needed.
* **requirements.txt** – Pinpointed Python dependencies.

---

## Project Structure

```
gemini-mqtt-dashboard/
├── app.py
├── requirements.txt
├── README.md
├── mqtt_credentials.txt  
├── APIKEY.txt (optional)
├── templates/
│   └── index.html
└── static/
    ├── brain.png
    ├── logo.png
    └── ...
```

---
![image](https://github.com/user-attachments/assets/85cddcf5-4249-4367-b282-087bf2fa1ad6)
![image](https://github.com/user-attachments/assets/fa03308c-6cfe-46be-a5b6-e2bd27a02803)

## License



gemini-mqtt-dashboard/
├── app.py
├── requirements.txt
├── README.md
├── mqtt_credentials.txt  
├── APIKEY.txt (optional)
├── templates/
│   └── index.html
└── static/
    ├── brain.png
    ├── logo.png
    └── ...

License

MIT License

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
