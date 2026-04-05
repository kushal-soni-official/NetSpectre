# 📘 NetSpectre Usage Guide

This guide provides a detailed walkthrough of how to use NetSpectre effectively for network reconnaissance and vulnerability assessment.

---

## 🛠️ Setup & Installation <a name="setup"></a>

### Prerequisites
1.  **Python 3.8+**: Ensure Python is installed and added to your PATH.
2.  **Nmap**: NetSpectre relies on the Nmap scanning engine.
    *   **Windows**: Download and run the [Nmap Installer](https://nmap.org/download.html#windows).
    *   **Linux**: `sudo apt install nmap` or `sudo yum install nmap`.
    *   **macOS**: `brew install nmap`.

### Installation
1.  Clone the repository or download the source code.
2.  Open a terminal in the project root.
3.  (Optional but Recommended) Create a virtual environment:
    ```bash
    python -m venv venv
    venv\Scripts\activate  # On Windows
    source venv/bin/activate  # On Linux/macOS
    ```
4.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

---

## 🚀 Running the Application

1.  Start the Flask server:
    ```bash
    python -m netspectre.app
    ```
2.  Open your browser and navigate to `http://localhost:5000`.

---

## 🔍 Scanning Modes

NetSpectre offers two primary scanning modes tailored for different needs:

### 1. Light Scan (`-sS -T5 --top-ports 100`)
*   **Speed**: Ultra-fast (usually < 30 seconds).
*   **Scope**: Scans the top 100 most common ports.
*   **Best For**: Quick surface discovery and checking if hosts are alive.

### 2. Deep Scan (`-sS -sV -sC -T4 --top-ports 1000`)
*   **Speed**: Moderate (depends on network size).
*   **Scope**: Scans the top 1000 ports + Service Version Detection + Default Scripts.
*   **Best For**: Comprehensive security audits and vulnerability correlation.

---

## 🎯 Target Input Formats

You can enter targets in several ways:
*   **Single IP**: `192.168.1.1`
*   **IP Range**: `192.168.1.1-50`
*   **Subnet (CIDR)**: `192.168.1.0/24`
*   **Hostname**: `example.com`

---

## 📊 Understanding Results

### Dashboard Indicators
*   **Progress Bar**: Shows the real-time status of the scan.
*   **Terminal Output**: Provides live logs from the scanning engine.

### Intel Reports
Once a scan completes, a professional HTML report is generated in the `reports/` directory. These reports include:
*   **Host Status**: Up/Down status and MAC addresses.
*   **Open Ports**: Service names, versions, and identified protocols.
*   **CVE Correlation**: If a service version is identified, NetSpectre automatically checks the National Vulnerability Database (NVD) for known exploits.

---

## ❓ Troubleshooting

### "Nmap not found" Error
Ensure Nmap is installed and the `nmap` command is accessible from your terminal. You may need to restart your terminal after installing Nmap.

### "Permission Denied" (Linux/macOS)
Some Nmap features (like SYN scans `-sS`) require root privileges. You can either:
*   Run the app with `sudo` (not recommended for web apps).
*   Grant Nmap cap_net_raw capabilities: `sudo setcap cap_net_raw,cap_net_admin,cap_net_bind_service+eip $(which nmap)`.

---

## 🛡️ Legal Disclaimer
NetSpectre is intended for educational and authorized security testing only. Unauthorized scanning of networks is illegal and unethical. Use this tool only on networks you own or have explicit permission to test.
