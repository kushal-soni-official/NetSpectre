import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import json

def generate_pdf_report(scan_data: dict, filepath: str):
    """
    Generate a formatted PDF report from scan results.
    """
    doc = SimpleDocTemplate(filepath, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph(f"NetSpectre Security Report", styles['Title']))
    story.append(Spacer(1, 12))
    
    # Executive Summary
    total_hosts = len(scan_data.get('hosts', []))
    total_ports = sum(len(h.get('ports', [])) for h in scan_data.get('hosts', []))
    total_cves = sum(len(p.get('cves', [])) for h in scan_data.get('hosts', []) for p in h.get('ports', []))

    summary = f"Scan completed successfully. Discovered {total_hosts} live hosts, {total_ports} open ports, and identified {total_cves} associated CVEs."
    story.append(Paragraph("Executive Summary", styles['Heading2']))
    story.append(Paragraph(summary, styles['BodyText']))
    story.append(Spacer(1, 12))

    # Host Details
    for host in scan_data.get('hosts', []):
        story.append(Paragraph(f"Host: {host.get('ip')} [{host.get('os', 'Unknown OS')}]", styles['Heading3']))
        
        for port in host.get('ports', []):
            story.append(Paragraph(f"Port {port.get('port')} - {port.get('name')} ({port.get('product')} {port.get('version')})", styles['Heading4']))
            
            cves = port.get('cves', [])
            if not cves:
                story.append(Paragraph("No associated CVEs found.", styles['BodyText']))
            else:
                for cve in cves:
                    sev = cve.get('severity', 'UNKNOWN')
                    color = "red" if sev in ["CRITICAL", "HIGH"] else "orange" if sev == "MEDIUM" else "green"
                    
                    cve_text = f"<b><font color='{color}'>{cve.get('cve_id')} (CVSS: {cve.get('cvss')} - {sev})</font></b><br/>{cve.get('description', '')}"
                    story.append(Paragraph(cve_text, styles['BodyText']))
                    story.append(Spacer(1, 6))

        story.append(Spacer(1, 12))

    doc.build(story)
    return filepath
