import nmap
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class PortScanner:
    def __init__(self):
        try:
            self.nm = nmap.PortScanner()
        except nmap.PortScannerError as e:
            logger.error(f"Nmap not found: {e}")
            raise
            
    def scan_light(self, target_ip: str) -> Dict[str, Any]:
        """
        Fast scan: SYN scan on top 100 ports, no OS detection.
        Args: target_ip
        """
        logger.info(f"Starting Light Scan on {target_ip}")
        # -sS: Stealth SYN, -F: Fast scan (top 100 ports), -T4: Aggressive timing
        # Requires root for -sS
        try:
            self.nm.scan(target_ip, arguments='-sS -F -T4')
            return self._parse_results(target_ip)
        except Exception as e:
            logger.error(f"Light scan failed on {target_ip}: {e}")
            return {"error": str(e)}

    def scan_deep(self, target_ip: str) -> Dict[str, Any]:
        """
        Deep scan: Full port scan (1-65535), Version detection, OS Fingerprinting.
        """
        logger.info(f"Starting Deep Scan on {target_ip}")
        # -sS: Stealth SYN, -sV: Probe open ports for service info
        # -O: OS detection, -p-: All ports, -T4: Aggressive timing
        try:
            self.nm.scan(target_ip, arguments='-sS -sV -O -p- -T4')
            return self._parse_results(target_ip)
        except Exception as e:
            logger.error(f"Deep scan failed on {target_ip}: {e}")
            return {"error": str(e)}

    def _parse_results(self, target_ip: str) -> Dict[str, Any]:
        if target_ip not in self.nm.all_hosts():
            return {"status": "down", "ip": target_ip, "ports": []}
            
        host_info = self.nm[target_ip]
        
        parsed = {
            "ip": target_ip,
            "status": host_info.state(),
            "mac": host_info['addresses'].get('mac', ''),
            "os": self._extract_os(host_info),
            "ports": []
        }
        
        if 'tcp' in host_info:
            for port, data in host_info['tcp'].items():
                parsed["ports"].append({
                    "port": port,
                    "state": data['state'],
                    "name": data['name'],
                    "product": data.get('product', ''),
                    "version": data.get('version', ''),
                    "extrainfo": data.get('extrainfo', ''),
                    "cpe": data.get('cpe', '')
                })
                
        return parsed

    def _extract_os(self, host_info: Dict) -> str:
        if 'osmatch' in host_info and host_info['osmatch']:
            # Return name of best match
            return host_info['osmatch'][0]['name']
        return "Unknown"
