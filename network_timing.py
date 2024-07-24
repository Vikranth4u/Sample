import requests
import socket
import ssl
import time
from urllib.parse import urlparse

def get_timings(url):
    timings = {}
    
    # Parse the URL
    parsed_url = urlparse(url)
    host = parsed_url.hostname
    port = parsed_url.port or (443 if parsed_url.scheme == 'https' else 80)
    
    # DNS resolution
    start_time = time.time()
    ip = socket.gethostbyname(host)
    dns_time = time.time() - start_time
    timings['dns_lookup'] = dns_time
    
    # TCP connection
    start_time = time.time()
    sock = socket.create_connection((ip, port))
    tcp_time = time.time() - start_time
    timings['tcp_connection'] = tcp_time
    
    # SSL handshake (if HTTPS)
    if parsed_url.scheme == 'https':
        context = ssl.create_default_context()
        start_time = time.time()
        sock = context.wrap_socket(sock, server_hostname=host)
        ssl_time = time.time() - start_time
        timings['ssl_handshake'] = ssl_time
    
    # HTTP request
    start_time = time.time()
    response = requests.get(url)
    http_time = time.time() - start_time
    timings['http_request'] = http_time
    
    # Total time
    total_time = dns_time + tcp_time + ssl_time + http_time
    timings['total_time'] = total_time
    
    return timings

if __name__ == "__main__":
    url = "https://www.example.com"
    timings = get_timings(url)
    
    print("Timings:")
    print(f"DNS Lookup: {timings['dns_lookup']:.2f} seconds")
    print(f"TCP Connection: {timings['tcp_connection']:.2f} seconds")
    if 'ssl_handshake' in timings:
        print(f"SSL Handshake: {timings['ssl_handshake']:.2f} seconds")
    print(f"HTTP Request: {timings['http_request']:.2f} seconds")
    print(f"Total Time: {timings['total_time']:.2f} seconds")
