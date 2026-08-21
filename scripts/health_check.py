#!/usr/bin/env python3
import urllib.request
import json
import sys

URL = 'http://localhost:5000/api/v1/health'

try:
    with urllib.request.urlopen(URL, timeout=5) as response:
        if response.status == 200:
            data = json.loads(response.read().decode())
            print(f"Health Check OK: {data}")
            sys.exit(0)
        else:
            print(f"Health Check Failed: status {response.status}")
            sys.exit(1)
except Exception as e:
    print(f"Health Check Connection Error: {e}")
    sys.exit(1)
