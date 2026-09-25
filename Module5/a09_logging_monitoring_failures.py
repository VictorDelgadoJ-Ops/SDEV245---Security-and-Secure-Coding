"""A10: Server-Side Request Forgery (SSRF).

Original problem: letting a user choose any URL can make the server request
internal or untrusted sites.
Change made: I allow only the listed hostname, set a timeout, and turn off
redirects so the request cannot automatically switch to another address.
"""

from urllib.parse import urlparse
import requests

ALLOWED_DOMAINS = ["example.com"]

url = input("Enter URL: ")

parsed = urlparse(url)

if parsed.hostname not in ALLOWED_DOMAINS:
    raise ValueError("Domain not allowed")

response = requests.get(url, timeout=5, allow_redirects=False)

print(response.text)