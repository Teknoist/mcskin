# -*- coding: utf-8 -*-
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

res = subprocess.run([sys.executable, "build_perfect_studio.py"], capture_output=True, text=True, encoding='utf-8')
print(res.stdout)
if res.stderr:
    print(res.stderr, file=sys.stderr)
