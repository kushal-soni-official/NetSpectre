from setuptools import setup, find_packages

setup(
    name="netspectre",
    version="1.0.0",
    description="Automated Network Vulnerability Scanner",
    author="Antigravity",
    packages=find_packages(),
    install_requires=[
        "Flask",
        "python-nmap",
        "nvdlib"
    ]
)
