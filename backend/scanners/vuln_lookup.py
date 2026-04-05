import nvdlib
import logging
import time
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class VulnLookup:
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        # Cache to prevent fetching same CPE multiple times during a single sweep
        self.cache = {}
        
    def check_cve(self, cpe_string: str) -> List[Dict[str, Any]]:
        """
        Query NVD API for CVEs related to a Common Platform Enumeration (CPE).
        """
        if not cpe_string:
            return []
            
        if cpe_string in self.cache:
            return self.cache[cpe_string]
            
        logger.info(f"Querying NVD for {cpe_string}")
        
        try:
            # We want vulnerabilities for this specific CPE
            # In a production environment, you might narrow down parameters heavily
            # The nvdlib.searchCVE supports cpeName
            results = nvdlib.searchCVE(cpeName=cpe_string, key=self.api_key, delay=1 if not self.api_key else 0.2)
            
            cves = []
            for r in results:
                # Extract essential data
                cve_id = r.id
                cvss = 0.0
                severity = "UNKNOWN"
                
                # Check for V3 or V2 metrics
                if hasattr(r, 'metrics'):
                    if hasattr(r.metrics, 'cvssMetricV31'):
                        cvss = r.metrics.cvssMetricV31[0].cvssData.baseScore
                        severity = r.metrics.cvssMetricV31[0].cvssData.baseSeverity
                    elif hasattr(r.metrics, 'cvssMetricV30'):
                        cvss = r.metrics.cvssMetricV30[0].cvssData.baseScore
                        severity = r.metrics.cvssMetricV30[0].cvssData.baseSeverity
                    elif hasattr(r.metrics, 'cvssMetricV2'):
                        cvss = r.metrics.cvssMetricV2[0].cvssData.baseScore
                        severity = r.metrics.cvssMetricV2[0].baseSeverity
                
                desc = getattr(r.descriptions[0], 'value', '') if hasattr(r, 'descriptions') and len(r.descriptions) > 0 else 'No description'
                
                cves.append({
                    "cve_id": cve_id,
                    "cvss": float(cvss),
                    "severity": severity,
                    "description": desc
                })
                
            # Store in cache
            self.cache[cpe_string] = cves
            
            # Artificial sleep to avoid rate limits if API Key is not present
            if not self.api_key:
                time.sleep(2)
                
            return cves
            
        except Exception as e:
            logger.error(f"Failed to query NVD for {cpe_string}: {e}")
            return []
