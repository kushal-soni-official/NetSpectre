import os
import json

def generate_html_report(scan_data: dict, filepath: str):
    """
    Generate a dynamic, glassmorphism-styled HTML report.
    """
    total_hosts = len(scan_data.get('hosts', []))
    total_ports = sum(len(h.get('ports', [])) for h in scan_data.get('hosts', []))
    
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>NetSpectre Security Report</title>
        <style>
            body {{
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
                color: #fff;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                min-height: 100vh;
            }}
            .glass-container {{
                background: rgba(255, 255, 255, 0.05);
                backdrop-filter: blur(15px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 15px;
                padding: 30px;
                max-width: 1000px;
                margin: 0 auto 30px auto;
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
                animation: fadeIn 1s ease-in-out;
            }}
            .severity-critical {{ color: #ff4d4d; font-weight: bold; text-shadow: 0 0 5px rgba(255,77,77,0.5); }}
            .severity-high {{ color: #ff9f43; font-weight: bold; text-shadow: 0 0 5px rgba(255,159,67,0.5); }}
            .severity-medium {{ color: #feca57; font-weight: bold; }}
            .severity-low {{ color: #1dd1a1; font-weight: bold; }}
            
            h1 {{ text-align: center; font-weight: 300; letter-spacing: 2px; text-transform: uppercase; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 15px; }}
            .host-card {{
                background: rgba(0, 0, 0, 0.2);
                border-radius: 10px;
                padding: 20px;
                margin-top: 20px;
                border-left: 5px solid #00d2d3;
                transition: transform 0.3s;
            }}
            .host-card:hover {{ transform: scale(1.01); }}
            
            @keyframes fadeIn {{
                0% {{ opacity: 0; transform: translateY(20px); }}
                100% {{ opacity: 1; transform: translateY(0); }}
            }}
        </style>
    </head>
    <body>
        <div class="glass-container">
            <h1>🛡️ NetSpectre Scan Report</h1>
            <p style="text-align: center;">Generated automatically. Discovered <b>{total_hosts}</b> Hosts and <b>{total_ports}</b> Open Ports.</p>
        </div>
    """
    
    for host in scan_data.get('hosts', []):
        html_template += f"""
        <div class="glass-container host-card">
            <h2>🖥️ IP: {host.get('ip')} <span style="font-size: 0.6em; color: #aaa;">({host.get('os', 'Unknown OS')})</span></h2>
            <p>MAC: {host.get('mac', 'Unknown')}</p>
            <hr style="border-color: rgba(255,255,255,0.05);">
        """
        
        for port in host.get('ports', []):
            product = port.get('product', '')
            version = port.get('version', '')
            software = f"{product} {version}".strip() or "Unknown Service"
            
            html_template += f"<h3>🔌 Port {port.get('port')} - {port.get('name')} | {software}</h3>"
            
            cves = port.get('cves', [])
            if not cves:
                html_template += "<p style='color: #1dd1a1;'>✅ No known CVEs detected.</p>"
            else:
                html_template += "<ul>"
                for cve in cves:
                    sev = cve.get('severity', 'UNKNOWN').lower()
                    sev_class = f"severity-{sev}"
                    desc = cve.get('description', '')
                    html_template += f"<li style='margin-bottom: 10px;'><span class='{sev_class}'>{cve.get('cve_id')}</span> (CVSS {cve.get('cvss')}) - {desc}</li>"
                html_template += "</ul>"
                
        html_template += "</div>"
        
    html_template += """
    </body>
    </html>
    """
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_template)
        
    return filepath
