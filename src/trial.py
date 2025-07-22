import streamlit as st
import requests
import socket
import ipaddress
from urllib.parse import urlparse
import os

# Environment variable listing allowed domains (comma-separated)
ALLOWED_DOMAINS = os.getenv('ALLOWED_DOMAINS', '').split(',') if os.getenv('ALLOWED_DOMAINS') else []


def is_private_address(hostname):
    try:
        # Resolve hostname to IP and check if it falls into private ranges
        addr = socket.gethostbyname(hostname)
        ip = ipaddress.ip_address(addr)
        return ip.is_private or ip.is_loopback
    except Exception:
        return True  # Fail closed: treat resolution errors as private


def validate_url(url_str):
    parsed = urlparse(url_str)
    if parsed.scheme not in ('http', 'https'):
        raise ValueError('Invalid URL scheme')
    host = parsed.hostname
    if not host:
        raise ValueError('URL must include a hostname')
    # Check against environment allowlist if provided
    if ALLOWED_DOMAINS:
        if not any(host.endswith(domain.strip()) for domain in ALLOWED_DOMAINS):
            raise ValueError('Domain not in allowed list')
    # Prevent SSRF by blocking private IPs
    if is_private_address(host):
        raise ValueError('Hostname resolves to a private or loopback address')
    return parsed.geturl()


def main():
    st.title("Safe External Image Fetcher")

    user_url = st.text_input("Enter image URL (HTTP/HTTPS)")
    if user_url:
        try:
            safe_url = validate_url(user_url)
            resp = requests.get(safe_url, timeout=5)
            resp.raise_for_status()
            st.image(resp.content, use_column_width=True)
        except Exception as e:
            st.error(f"Failed to fetch image: {e}")

if __name__ == "__main__":
    main()
