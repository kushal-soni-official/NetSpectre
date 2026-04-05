import pytest
from unittest.mock import patch, MagicMock

# Mock out Nmap and Scapy since they require root privileges and external networks
@patch('netspectre.scanners.port_scanner.nmap.PortScanner')
def test_port_scanner_initialization(mock_nmap):
    from netspectre.scanners.port_scanner import PortScanner
    scanner = PortScanner()
    assert scanner.nm is not None

@patch('netspectre.scanners.host_discovery.srp')
def test_host_discovery_mock(mock_srp):
    from netspectre.scanners.host_discovery import discover_hosts
    # Mock scapy response structure
    mock_received = MagicMock()
    mock_received.psrc = "192.168.1.10"
    mock_received.hwsrc = "AA:BB:CC:DD:EE:FF"
    mock_srp.return_value = ([(None, mock_received)], None)
    
    hosts = discover_hosts("192.168.1.0/24")
    assert len(hosts) == 1
    assert hosts[0]['ip'] == "192.168.1.10"
    assert hosts[0]['mac'] == "AA:BB:CC:DD:EE:FF"

@patch('netspectre.scanners.vuln_lookup.nvdlib.searchCVE')
def test_cve_lookup_mock(mock_search):
    from netspectre.scanners.vuln_lookup import VulnLookup
    # Mock NVDlib response
    mock_result = MagicMock()
    mock_result.id = "CVE-2024-9999"
    mock_result.metrics.cvssMetricV31 = [MagicMock()]
    mock_result.metrics.cvssMetricV31[0].cvssData.baseScore = 9.8
    mock_result.metrics.cvssMetricV31[0].cvssData.baseSeverity = "CRITICAL"
    mock_result.descriptions = [MagicMock(value="Remote Code Execution vulnerability.")]
    
    mock_search.return_value = [mock_result]
    
    lookup = VulnLookup()
    res = lookup.check_cve("cpe:2.3:a:mock:software:1.0:*:*:*:*:*:*:*")
    
    assert len(res) == 1
    assert res[0]['cve_id'] == "CVE-2024-9999"
    assert res[0]['severity'] == "CRITICAL"
