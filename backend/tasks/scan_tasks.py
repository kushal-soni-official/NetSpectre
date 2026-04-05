from celery import shared_task
from backend.scanners.host_discovery import discover_hosts
from backend.scanners.port_scanner import PortScanner
from backend.scanners.vuln_lookup import VulnLookup
from utils.report_generator import generate_pdf_report
from utils.html_report_builder import generate_html_report
from backend.config import Config
import os
import uuid

@shared_task(bind=True)
def run_network_scan(self, target_subnet: str, scan_mode: str = "light"):
    """
    Main background task to execute network scans.
    """
    self.update_state(state='PROGRESS', meta={'status': 'Initialzing Target Discovery...'})
    
    # 1. Host Discovery
    live_hosts = discover_hosts(target_subnet)
    total_hosts = len(live_hosts)
    
    self.update_state(state='PROGRESS', meta={'status': f'Found {total_hosts} live hosts. Starting Port Scan...'})
    
    port_scanner = PortScanner()
    vuln_lookup = VulnLookup(api_key=Config.NVD_API_KEY)
    
    results = {"target": target_subnet, "mode": scan_mode, "hosts": []}
    
    # 2. Port & Vulnerability Scanning
    for index, host in enumerate(live_hosts):
        ip = host['ip']
        self.update_state(state='PROGRESS', meta={'status': f'Scanning {ip} ({index+1}/{total_hosts})...'})
        
        if scan_mode == "deep":
            host_result = port_scanner.scan_deep(ip)
        else:
            host_result = port_scanner.scan_light(ip)
            
        # Merge MAC from scapy specifically if nmap didn't find it
        if not host_result.get('mac'):
            host_result['mac'] = host['mac']
            
        # 3. CVE Lookups
        for port_info in host_result.get('ports', []):
            cpe = port_info.get('cpe', '')
            if cpe:
                self.update_state(state='PROGRESS', meta={'status': f'Querying NVD API for {cpe}...'})
                cves = vuln_lookup.check_cve(cpe)
                port_info['cves'] = cves
            else:
                port_info['cves'] = []
                
        results['hosts'].append(host_result)
        
    # 4. Generate Reports
    self.update_state(state='PROGRESS', meta={'status': 'Generating Reports...'})
    
    scan_id = str(uuid.uuid4())[:8]
    pdf_path = os.path.join(Config.REPORTS_DIR, f"netspectre_report_{scan_id}.pdf")
    html_path = os.path.join(Config.REPORTS_DIR, f"netspectre_report_{scan_id}.html")
    
    try:
        generate_pdf_report(results, pdf_path)
    except Exception as e:
        results['pdf_error'] = str(e)
        
    try:
        generate_html_report(results, html_path)
    except Exception as e:
        results['html_error'] = str(e)
        
    results['pdf_report'] = f"netspectre_report_{scan_id}.pdf"
    results['html_report'] = f"netspectre_report_{scan_id}.html"
    
    self.update_state(state='SUCCESS', meta={'status': 'Scan Complete'})
    return results
