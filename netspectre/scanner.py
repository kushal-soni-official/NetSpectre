import nmap
import nvdlib
import logging
import time
import threading
import uuid
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Any, List, Optional
import subprocess
import signal
from netspectre.config import Config
from netspectre.reports import generate_html_report

logger = logging.getLogger(__name__)

class TargetScanner:
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.nm = nmap.PortScanner()
        self.vuln_cache = {}

    def fetch_cves(self, cpe_string: str) -> List[Dict[str, Any]]:
        """Query NVD API for CVEs matching the CPE."""
        if not cpe_string:
            return []
            
        if cpe_string in self.vuln_cache:
            return self.vuln_cache[cpe_string]
            
        logger.info(f"Querying NVD for {cpe_string}")
        cves = []
        try:
            results = nvdlib.searchCVE(cpeName=cpe_string, key=self.api_key, delay=0.5 if self.api_key else 1.0)
            for r in results:
                cvss, severity = 0.0, "UNKNOWN"
                if hasattr(r, 'metrics'):
                    if hasattr(r.metrics, 'cvssMetricV31'):
                        cvss = r.metrics.cvssMetricV31[0].cvssData.baseScore
                        severity = r.metrics.cvssMetricV31[0].cvssData.baseSeverity
                    elif hasattr(r.metrics, 'cvssMetricV2'):
                        cvss = r.metrics.cvssMetricV2[0].cvssData.baseScore
                        severity = r.metrics.cvssMetricV2[0].baseSeverity
                
                desc = getattr(r.descriptions[0], 'value', '') if hasattr(r, 'descriptions') and len(r.descriptions) > 0 else 'No description'
                cves.append({
                    "cve_id": r.id,
                    "cvss": float(cvss),
                    "severity": severity,
                    "description": desc
                })
            self.vuln_cache[cpe_string] = cves
        except Exception as e:
            logger.error(f"Failed NVD query for {cpe_string}: {e}")
        return cves

    def scan_ip(self, ip: str, mode: str, update_cb=None, stop_event=None) -> Dict[str, Any]:
        """Runs the scan for a single IP."""
        if stop_event and stop_event.is_set():
            return {"ip": ip, "status": "cancelled", "ports": []}
            
        if update_cb: update_cb(f"Scanning {ip} in {mode} mode...")
        try:
            if mode == 'deep':
                # Optimized Deep Scan: Top 1000 ports, TCP SYN, Service detection, Default scripts, Aggressive timing
                self.nm.scan(ip, arguments='-sS -sV -sC -T4 --top-ports 1000')
            else:
                # Optimized Light Scan: Top 100 ports, TCP SYN, Insane timing
                self.nm.scan(ip, arguments='-sS -T5 --top-ports 100')
        except Exception as e:
            return {"ip": ip, "status": "error", "error": str(e), "ports": []}

        if ip not in self.nm.all_hosts():
            return {"ip": ip, "status": "down", "ports": []}

        host_info = self.nm[ip]
        os_match = host_info.get('osmatch', [])
        os_name = os_match[0]['name'] if os_match else "Unknown"

        result = {
            "ip": ip,
            "status": host_info.state(),
            "mac": host_info['addresses'].get('mac', ''),
            "os": os_name,
            "ports": []
        }

        if 'tcp' in host_info:
            for port, data in host_info['tcp'].items():
                port_result = {
                    "port": port,
                    "state": data['state'],
                    "name": data['name'],
                    "product": data.get('product', ''),
                    "version": data.get('version', ''),
                    "cpe": data.get('cpe', '')
                }
                if port_result['cpe']:
                    if update_cb: update_cb(f"Fetching CVEs for {port_result['cpe']}...")
                    port_result['cves'] = self.fetch_cves(port_result['cpe'])
                else:
                    port_result['cves'] = []
                result['ports'].append(port_result)

        return result

    def scan_network(self, target_subnet: str, mode: str, update_cb=None) -> Dict[str, Any]:
        """Discovers hosts and scans them."""
        # Host Discovery using nmap Ping Sweep
        if update_cb: update_cb("Discovering live hosts via Nmap (-sn)...")
        self.nm.scan(target_subnet, arguments='-sn -T4')
        live_hosts = self.nm.all_hosts()
        
        if not live_hosts:
            if update_cb: update_cb("No live hosts found.")
            return {"target": target_subnet, "mode": mode, "hosts": []}

        if update_cb: update_cb(f"Found {len(live_hosts)} hosts. Commencing port scans...")
        
        results = {"target": target_subnet, "mode": mode, "hosts": []}
        
        # Concurrently scan all discovered hosts
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_ip = {executor.submit(self.scan_ip, ip, mode, update_cb, stop_event=getattr(self, 'stop_event', None)): ip for ip in live_hosts}
            for future in as_completed(future_to_ip):
                if getattr(self, 'stop_event', None) and self.stop_event.is_set():
                    break
                ip = future_to_ip[future]
                try:
                    data = future.result()
                    results['hosts'].append(data)
                except Exception as e:
                    logger.error(f"Error scanning {ip}: {e}")

        if update_cb: update_cb("Generating Report...")
        scan_id = str(uuid.uuid4())[:8]
        html_path = os.path.join(Config.REPORTS_DIR, f"netspectre_report_{scan_id}.html")
        generate_html_report(results, html_path)
        results['html_report'] = f"netspectre_report_{scan_id}.html"

        if update_cb: update_cb("Scan Complete")
        return results

class TaskManager:
    def __init__(self):
        self.tasks = {}

    def submit_scan(self, target_subnet: str, mode: str):
        task_id = str(uuid.uuid4())
        self.tasks[task_id] = {
            'state': 'PENDING',
            'status': 'Initializing scan...',
            'result': None,
            'stop_event': threading.Event()
        }

        def worker():
            def cb(msg):
                self.tasks[task_id]['status'] = msg
            
            scanner = TargetScanner(api_key=Config.NVD_API_KEY)
            scanner.stop_event = self.tasks[task_id]['stop_event']
            
            start_time = time.time()
            self.tasks[task_id]['start_time'] = start_time
            
            try:
                self.tasks[task_id]['state'] = 'PROGRESS'
                res = scanner.scan_network(target_subnet, mode, update_cb=cb)
                
                if scanner.stop_event.is_set():
                    self.tasks[task_id]['state'] = 'CANCELLED'
                    self.tasks[task_id]['status'] = 'Scan stopped by user.'
                else:
                    self.tasks[task_id]['state'] = 'SUCCESS'
                    self.tasks[task_id]['result'] = res
                    self.tasks[task_id]['end_time'] = time.time()
                    self.tasks[task_id]['duration'] = self.tasks[task_id]['end_time'] - start_time
            except nmap.PortScannerError:
                self.tasks[task_id]['state'] = 'FAILURE'
                self.tasks[task_id]['status'] = "Nmap installation not found. Please install Nmap from nmap.org and add it to your PATH."
            except Exception as e:
                self.tasks[task_id]['state'] = 'FAILURE'
                self.tasks[task_id]['status'] = f"Fatal Error: {str(e)}"

        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()
        
        return task_id

    def stop_scan(self, task_id: str) -> bool:
        if task_id in self.tasks:
            self.tasks[task_id]['stop_event'].set()
            return True
        return False

    def get_status(self, task_id: str) -> Optional[Dict]:
        task = self.tasks.get(task_id)
        if not task:
            return None
        
        # Add live duration if in progress
        if task['state'] == 'PROGRESS' and 'start_time' in task:
            task['elapsed'] = time.time() - task['start_time']
            
        return task

task_manager = TaskManager()
