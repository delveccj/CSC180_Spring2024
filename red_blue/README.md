# 🛡️ MySQL Security Visibility Lab

A Docker-based security visibility lab where students run intentionally misconfigured MySQL containers that report their status to an instructor-run dashboard.

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
