<div align="center">
  <h1>🌐 NetSpectre</h1>
  <p><strong>An Automated, Asynchronous Network Vulnerability Scanner</strong></p>
  
  <p>
    <img alt="Python" src="https://img.shields.io/badge/Python-3.11+-blue.svg" />
    <img alt="Framework" src="https://img.shields.io/badge/Flask%20%26%20Celery-Background%20Workers-green.svg" />
    <img alt="Scanner" src="https://img.shields.io/badge/Engine-Nmap%20%26%20Scapy-orange.svg" />
    <img alt="Reports" src="https://img.shields.io/badge/Exports-PDF%20%2B%20HTML-yellow.svg" />
  </p>
</div>

---

## 🌟 What is NetSpectre?

**NetSpectre** is a professional-grade cybersecurity tool designed to automatically sweep through networks, identify every connected device, map out open ports, and cross-reference them with global vulnerability databases to find security risks (CVEs). 

It is separated into two parts: a heavy-lifting background worker ensuring scans never crash or lag, and a beautiful Real-Time Web Dashboard where you can watch the hacks unfold live!

### ✨ Key Features:
* 📡 **Smart Scanning Modes:** Choose between a **Light Scan** (fast, stealthy) or a **Deep Scan** (intense verification, OS fingerprinting).
* 🔍 **Automated Vulnerability Lookups:** Connects directly to NIST's National Vulnerability Database (NVD) to instantly alert you of known software flaws.
* ⚡ **Asynchronous Engine:** Uses Celery and Redis so you can run network scans lasting anywhere from 2 minutes to 2 hours without freezing your dashboard.
* 🎨 **Dual Reporting:** Generate clean, structured **PDF reports** for executives, or visually stunning, **Interactive HTML (Glassmorphism)** reports for modern analysts.

---

## 🚀 Step 1: Easy Installation (Beginner Friendly!)

To run NetSpectre, you'll need Python, the Nmap network scanner, and Redis (which handles background messaging).

### Install System Requirements (Linux/Ubuntu):
```bash
sudo apt update
sudo apt install nmap redis-server
sudo systemctl enable redis-server
sudo systemctl start redis-server
```

### Install the NetSpectre Python Application:
Open your terminal, navigate into the project folder, and run:
```bash
# 1. Create a safe bubble for your Python app (Virtual Environment)
python3 -m venv venv

# 2. Activate the virtual environment
source venv/bin/activate  # On Windows, use: venv\Scripts\activate

# 3. Install the required Python packages
pip install -r requirements.txt
```

*(Important Tip for Experts: You can export `NVD_API_KEY="your_api_key"` in your terminal to speed up vulnerability lookups natively!)*

---

## 💥 Step 2: Running the System

NetSpectre requires two terminals to run simultaneously because the heavy network scanning happens independently of the web dashboard.

### Terminal A: The Scanning Engine (Background Worker)
Because advanced network scanning requires deep operating system access (like spoofing identities or writing raw packets), the worker **must run as root/sudo**.
```bash
# In your netspectre folder
source venv/bin/activate

# Start the Celery Worker as Root
sudo ./venv/bin/celery -A backend.celery_worker.celery_app worker --loglevel=info
```

### Terminal B: The Web Dashboard
In a completely new terminal window, start your dashboard:
```bash
# In your netspectre folder
source venv/bin/activate

# Start the Web Server
PYTHONPATH=. python backend/app.py
```

---

## 🌐 Step 3: Using the Dashboard

1. Open your web browser (Chrome, Firefox, Safari) and visit: 👉 **[http://localhost:5000](http://localhost:5000)** 👈
2. In the **Target Range**, type the IP address or Subnet you want to scan (e.g., `192.168.1.0/24`).
3. Select your **Scan Profile** (Light or Deep).
4. Click **Initialize Scan**!
5. Watch the glowing terminal window as NetSpectre finds active devices, probes their services, and logs vulnerabilities in real-time. 
6. When complete, click the buttons on-screen to instantly download your **PDF** or **Interactive HTML** Report!

---
<div align="center">
  <i>Created for cybersecurity mapping and vulnerability exposure. Built cleanly and defensively.</i>
</div>
