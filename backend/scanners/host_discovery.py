import logging
from typing import List, Dict, Optional
from scapy.all import ARP, Ether, srp, conf

logger = logging.getLogger(__name__)

def discover_hosts(target_subnet: str, timeout: int = 2) -> List[Dict[str, str]]:
    """
    Perform an ARP ping sweep on the target subnet to discover live hosts.
    Requires root/sudo privileges.
    
    Args:
        target_subnet: CIDR notation of target (e.g. '192.168.1.0/24')
        timeout: Wait time for responses
        
    Returns:
        List of dictionaries containing 'ip' and 'mac' of discovered hosts.
    """
    logger.info(f"Starting host discovery on {target_subnet}")
    live_hosts = []
    
    try:
        # Create ARP Request packet
        arp_request = ARP(pdst=target_subnet)
        # Create Ethernet frame for broadcast
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        # Combine them
        packet = ether/arp_request
        
        # Send packets and receive answers
        # srp sends and receives packets at layer 2
        result = srp(packet, timeout=timeout, verbose=0)[0]
        
        for sent, received in result:
            live_hosts.append({
                'ip': received.psrc,
                'mac': received.hwsrc
            })
            
        logger.info(f"Discovered {len(live_hosts)} hosts.")
        return live_hosts
        
    except PermissionError:
        logger.error("Permission denied. Scapy requires root privileges for active mapping.")
        # Fallback or re-raise
        raise
    except Exception as e:
        logger.error(f"Host discovery failed: {str(e)}")
        raise
