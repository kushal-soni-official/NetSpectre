import json
from datetime import datetime

def generate_html_report(scan_data: dict, output_path: str):
    """
    Generates a modern, high-quality, standalone HTML report.
    """
    total_hosts = len(scan_data.get('hosts', []))
    total_ports = sum(len(h.get('ports', [])) for h in scan_data.get('hosts', []))
    total_cves = sum(len(p.get('cves', [])) for h in scan_data.get('hosts', []) for p in h.get('ports', []))
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    target = scan_data.get('target', 'Unknown')
    mode = scan_data.get('mode', 'Unknown')

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NetSpectre Security Report</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #0f172a;
            --text-color: #f8fafc;
            --card-bg: rgba(30, 41, 59, 0.7);
            --card-border: rgba(255, 255, 255, 0.1);
            --accent: #38bdf8;
            --critical: #ef4444;
            --high: #f97316;
            --medium: #facc15;
            --low: #4ade80;
        }}
        body {{
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 2rem;
            line-height: 1.6;
        }}
        h1, h2, h3 {{ margin-top: 0; }}
        .header {{
            text-align: center;
            margin-bottom: 3rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid var(--card-border);
        }}
        .header h1 {{
            font-size: 2.5rem;
            background: linear-gradient(90deg, #38bdf8, #818cf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin-bottom: 3rem;
        }}
        .stat-card {{
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }}
        .stat-value {{
            font-size: 2rem;
            font-weight: 700;
            color: var(--accent);
        }}
        .host-card {{
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 12px;
            margin-bottom: 2rem;
            overflow: hidden;
        }}
        .host-header {{
            background: rgba(255, 255, 255, 0.05);
            padding: 1rem 1.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--card-border);
        }}
        .host-ip {{ font-size: 1.25rem; font-weight: 600; color: #818cf8; }}
        .host-os {{ font-size: 0.9rem; color: #cbd5e1; }}
        .port-list {{ padding: 1.5rem; }}
        .port-item {{
            margin-bottom: 1.5rem;
            padding-bottom: 1.5rem;
            border-bottom: 1px dashed rgba(255,255,255,0.1);
        }}
        .port-item:last-child {{ border-bottom: none; margin-bottom: 0; padding-bottom: 0; }}
        .port-title {{
            font-weight: 600;
            color: #cbd5e1;
            margin-bottom: 0.5rem;
        }}
        .cve-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.85rem;
            margin-top: 0.5rem;
        }}
        .cve-table th, .cve-table td {{
            text-align: left;
            padding: 0.75rem;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }}
        .cve-table th {{ background: rgba(0,0,0,0.2); color: #94a3b8; font-weight: 600; }}
        .badge {{
            padding: 0.25rem 0.5rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 700;
            color: #fff;
        }}
        .badge.critical {{ background-color: var(--critical); }}
        .badge.high {{ background-color: var(--high); }}
        .badge.medium {{ background-color: var(--medium); color: #000; }}
        .badge.low {{ background-color: var(--low); color: #000; }}
        .badge.unknown {{ background-color: #64748b; }}
        
        .no-cve {{ color: #4ade80; font-weight: bold; font-size: 0.9rem; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>NetSpectre Security Report</h1>
        <p>Target: <strong>{target}</strong> | Mode: <strong>{mode.capitalize()}</strong> | Generated on: <strong>{timestamp}</strong></p>
    </div>

    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-value">{total_hosts}</div>
            <div>Live Hosts</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{total_ports}</div>
            <div>Open Ports Discovered</div>
        </div>
        <div class="stat-card">
            <div class="stat-value" style="color: {var(--critical) if total_cves > 0 else var(--accent)}">{total_cves}</div>
            <div>Vulnerabilities (CVEs)</div>
        </div>
    </div>
"""
    
    if not scan_data.get('hosts'):
        html_content += "<p style='text-align:center;'>No hosts discovered on this target.</p>"
    
    for host in scan_data.get('hosts', []):
        os_info = host.get('os', 'Unknown')
        mac_info = f" | MAC: {host.get('mac')}" if host.get('mac') else ""
        
        html_content += f"""
    <div class="host-card">
        <div class="host-header">
            <div class="host-ip">Host: {host.get('ip')}</div>
            <div class="host-os">OS: {os_info}{mac_info}</div>
        </div>
        <div class="port-list">
        """
        
        ports = host.get('ports', [])
        if not ports:
            html_content += "<p>No open ports discovered.</p>"
            
        for port in ports:
            version_str = f"{port.get('product', '')} {port.get('version', '')}".strip()
            title = f"Port {port.get('port')} ({port.get('name', 'unknown')})"
            if version_str:
                title += f" - {version_str}"
                
            html_content += f"""
            <div class="port-item">
                <div class="port-title">{title}</div>
            """
            
            cves = port.get('cves', [])
            if not cves:
                html_content += "<span class='no-cve'>✓ No known CVEs found.</span>"
            else:
                html_content += """
                <table class="cve-table">
                    <thead>
                        <tr>
                            <th style="width: 15%">CVE ID</th>
                            <th style="width: 10%">CVSS / Severity</th>
                            <th>Description</th>
                        </tr>
                    </thead>
                    <tbody>
                """
                for cve in cves:
                    sev = cve.get('severity', 'UNKNOWN').lower()
                    sev_class = sev if sev in ['critical', 'high', 'medium', 'low'] else 'unknown'
                    
                    html_content += f"""
                        <tr>
                            <td><strong><a href="https://nvd.nist.gov/vuln/detail/{cve.get('cve_id')}" target="_blank" style="color:#38bdf8; text-decoration:none;">{cve.get('cve_id')}</a></strong></td>
                            <td><span class="badge {sev_class}">{cve.get('cvss')} {sev.upper()}</span></td>
                            <td>{cve.get('description', '')}</td>
                        </tr>
                    """
                html_content += """
                    </tbody>
                </table>
                """
            
            html_content += "</div>" # end port-item
            
        html_content += """
        </div>
    </div>
        """
        
    html_content += """
</body>
</html>
"""
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
