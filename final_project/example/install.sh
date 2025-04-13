#!/bin/bash
echo "[*] Installing dev dependencies..."

# ✅ Correct file URI with three slashes for absolute path
pip install --no-cache-dir --find-links=file:///local_pypi -r requirements.txt

echo "[*] Installation done."
ls /tmp/pwned.txt && cat /tmp/pwned.txt || echo "[!] Exploit file not found."

