# 🌌 NetSpectre (v2.0)
### *Advanced Quantum-Ready Network Reconnaissance Engine*

NetSpectre is a high-performance network security tool designed for rapid discovery, port identification, and vulnerability correlation. It provides a sleek, modern, and interactive web dashboard featuring a stunning Glassmorphism UI.

![NetSpectre Banner](https://img.shields.io/badge/NetSpectre-2.0.0-blueviolet?style=for-the-badge&logo=target)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Framework](https://img.shields.io/badge/Flask-Web-lightgrey?style=for-the-badge&logo=flask)

---

## 🚀 Quick Start (Zero to Scan)

Get NetSpectre up and running in less than 2 minutes.

1.  **Install Requirements** (Ensure you have [Nmap](https://nmap.org/download.html) installed on your system):
    ```bash
    pip install -r requirements.txt
    ```

2.  **Ignite the Engine**:
    ```bash
    python -m netspectre.app
    ```

3.  **Access the Dashboard**:
    Open [http://localhost:5000](http://localhost:5000) in your browser.

---

## 🔑 NVD API Integration (Optional but Recommended)

NetSpectre uses the [National Vulnerability Database (NVD)](https://nvd.nist.gov/) to correlate service versions with known CVEs. 

While it works out of the box, setting an API key is highly recommended for faster lookups and higher rate limits.

| Mode | Speed / Rate Limit |
|---|---|
| **Without Key** | 1.0s delay per request (~5 req / 30s) |
| **With Key** | 0.5s delay per request (Significantly faster) |

### 1. Get Your Free Key
Request a free key instantly at [NVD Key Request](https://nvd.nist.gov/developers/request-an-api-key).

### 2. Set the Environment Variable
**Windows (Command Prompt):**
```cmd
set NVD_API_KEY=your_key_here
```

**Linux/macOS:**
```bash
export NVD_API_KEY='your_key_here'
```

### 3. Verify the Setup
Run this command to check if the variable is active:
- **Windows:** `echo %NVD_API_KEY%`
- **Linux/macOS:** `echo $NVD_API_KEY`

> [!TIP]
> NetSpectre will also display a **[CONFIRMED]** status in the console during startup if the key is detected.

---

## ⚡ Key Features

*   🚀 **High-Velocity Scanning**: Sub-30s surface scans for rapid reconnaissance.
*   🛡️ **Vulnerability Correlation**: Automatic CVE lookup via NVD integration.
*   🎨 **Modern Design**: Crystal-clear Glassmorphism 2.0 interface.
*   📊 **Instant Reporting**: Professional HTML reports generated after every scan.
*   🛑 **Full Control**: Start, stop, and monitor scans in real-time.

---

## 📖 Guided Documentation

Looking for more detail? Check out our visual guides:

*   [**Usage Guide**](USAGE.md) - Learn how to master the scanning modes.
*   [**Installation Guide**](USAGE.md#setup) - Detailed setup instructions for all platforms.

---

## 📂 Project Architecture

```text
netspectre/
├── netspectre/                 # Core Engine
│   ├── app.py                  # Entry Point
│   ├── scanner.py              # Scanning Logic
│   └── web/                    # Dashboard Interface
├── reports/                    # Generated Intelligence
├── tests/                      # Reliability Tests
└── USAGE.md                    # Detailed Manual
```

---

## 🔮 Future Roadmap

*   **AI-Powered Triaging**: LLM-based analysis of vulnerabilities.
*   **Mesh Graphing**: Visualize your network topology in 3D.
*   **Distributed Scanners**: Deployable agents for multi-point reconnaissance.

---

## 📜 license & Legal

Distributed under the MIT License. Use responsibly.

*“Seeing through the network shroud.”*
