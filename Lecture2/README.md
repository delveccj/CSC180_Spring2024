# Lecture 2: January 27, 2025 #

## Learning Objectives ##
1. LO1: Familiarity with CTF vulnerability approaches; either an insider or an outsider
2. LO2: Creating a vulnerable environment with containers
3. LO3: Using CTF tools - its all about the command line
4. LO4:  Exploiting a vulnerable container

## Familiarity with Approaches
There are two approaches to CTF.  

*The Insider*

The first approach is the insider.  In this example your network is infected.  You have malware that is either stealthily or blatantly providing access to your network via a vulnerability.
Here is an example of one such tool we can use 'safely':

[https://caldera.mitre.org/](https://caldera.mitre.org/)

We will use this in a few weeks.

*The Outsider*

The second approach is to poke a hole through a network's defenses.  Everyone has public access points to their networks.  Industry, academia, the U.S. government.  It is simply impossible not to have public access points.  Note, a public access point is typically a port that is used for legitamate users and applications to connect to resources hosted by or inside your environment.

We will tackle the outsider example with today's lecture.

## How Are Public Access Points Identified?  ##

There are many ways.  Here is a basic one.  Let's explore the utility ```nmap```.

### **What is Nmap?**  
**Nmap** (short for **Network Mapper**) is a powerful, open-source tool used for **network discovery** and **security auditing.** It’s primarily a command-line tool, but it also has a graphical interface called Zenmap.  

Nmap allows users to scan networks to identify active devices, open ports, services, and their versions, as well as the operating systems they’re running. It is widely used in cybersecurity, systems administration, and even academic research.

---

### **History of Nmap**  
- **Released in 1997**: Nmap was first introduced by **Gordon Lyon**, also known by his online alias "Fyodor," in a seminal article for *Phrack Magazine*. The tool was created to help network administrators and security professionals better understand their networks.
  
- **First Public Release**: Version 1.0 was released as an open-source project in September 1997.

- **Evolution**: Over the years, Nmap has grown from a simple port scanner to an all-encompassing **network mapping and reconnaissance tool.**
  - **2000s**: Nmap gained features like OS detection and the ability to detect service versions.
  - **2009**: Zenmap, the GUI frontend for Nmap, was released for easier adoption by non-technical users.
  - **Today**: Nmap is one of the most trusted tools in cybersecurity and a staple in tools like Kali Linux.

---

### **Why Was Nmap Legitimately Created?**
Nmap was **legitimately created for network administrators and security professionals** to better understand their networks. Its purpose is **proactive security**—to help identify weaknesses before attackers can exploit them. Legitimate use cases include:

1. **Network Discovery**:
   - Identify live hosts, open ports, and running services on a network.

2. **Vulnerability Assessment**:
   - By discovering open ports and services, admins can assess whether those services are secure or up-to-date.

3. **Compliance and Auditing**:
   - Nmap is commonly used during compliance scans to verify that only authorized services are accessible.

4. **Troubleshooting**:
   - Admins can use Nmap to diagnose connectivity issues or misconfigurations.

---

### **What Does Nmap Stand For?**
Nmap stands for **Network Mapper.**  
The name emphasizes its primary function—**mapping a network** by identifying devices, services, and other resources in a given range of IP addresses.

---

### **Why Has Nmap Stood the Test of Time?**
1. **Open Source**: Nmap’s open-source nature has allowed for continuous improvement by the community.
2. **Flexibility**: It works across a wide range of operating systems (Linux, Windows, macOS, etc.).
3. **Powerful Features**:
   - Advanced scanning techniques (e.g., SYN scans, service detection).
   - OS and version fingerprinting.
   - A rich **scripting engine** (NSE) for custom scans and automation.
4. **Educational and Practical**: While often used for penetration testing, it remains a vital tool for legitimate IT and security operations.

---

### **How is Nmap Used Legitimately?**
While Nmap can be used maliciously (as with many powerful tools), its **legitimate use cases** include:
- **IT Departments**: Map networks to ensure no unauthorized devices are connected.
- **Penetration Testing**: Identify potential vulnerabilities in a controlled, ethical environment.
- **Incident Response**: After a breach, use Nmap to investigate unauthorized devices or services.

---

### **Try it out!**
Let's scan our network to find active devices.  This takes a bit of time:

```bash
nmap -sn 192.168.1.0/24
```

Let's scan all the ports on our machine to see what is open.

```bash
nmap -p- 127.0.0.1
```

## How Can I Create a Safe But Vulnerable Environment?  ##

Welcome to containers!  If you are familiar with Virtual Machines, containers are similar to these but have a much smaller footprint and require far less time to setup and use up fewere computaitonal resources.

Let's dive in and create a vulnerable container.  That's the beauty of 2025, you can do all of this stuff!

```bash
# Use a lightweight base image
FROM ubuntu:20.04

# Install SSH server
RUN apt-get update && apt-get install -y openssh-server

# Set up SSH with weak credentials
RUN mkdir /var/run/sshd && \
    echo 'root:1234' | chpasswd  # Weak root password!

# Allow root login via SSH (big no-no in production!)
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# Expose the SSH port
EXPOSE 22

# Start SSH service
CMD ["/usr/sbin/sshd", "-D"]
```

We first need to build the container.  We can issue this command:

```bash
docker build -t vulnerable-ssh .
```

Now, to run the container do:

```bash
docker run -d -p 2222:22 --name vulnerable-ssh vulnerable-ssh
```

To verify it is running, try this:

```bash
docker ps
```

Now let's scan the open ports once again with this:

```bash
nmap -p- 127.0.0.1
```

Do you see port 2222 open?  Great!  Time to leverage its terrible password.

## How Can I Quickly Take Advantage of Weak Passwords?  ##
### **What is Hydra?**
Hydra (short for **THC-Hydra**) is a fast and flexible **password-cracking tool** designed for brute-forcing authentication on various network services. It was created by the **The Hacker's Choice (THC)** group as a tool for penetration testing and security professionals to evaluate the strength of authentication mechanisms. First released in the early 2000s, Hydra has become a popular tool in the cybersecurity community due to its ability to target over 50 different protocols, including SSH, HTTP, FTP, SMTP, and more.

Hydra works by automating login attempts against a target service. It does this by trying combinations of usernames and passwords from specified lists until it finds valid credentials. This process, known as a **dictionary attack**, makes Hydra effective for testing weak or default passwords. However, it's important to note that Hydra should only be used for ethical and legitimate purposes, such as auditing your own systems or during authorized penetration testing.

---

### **Installing Hydra**
Hydra is available on most Linux distributions and is often pre-installed on penetration-testing distros like **Kali Linux**. Here's how to install it:

#### 🐧 **On Linux (Debian/Ubuntu):**
```bash
sudo apt update
sudo apt install -y hydra
```

To confirm the installation, run:
```bash
hydra -h
```

You should see Hydra's help menu with a list of supported options and protocols.

---

### **Using Hydra Against Localhost Port 2222**
Let’s say you have a Docker container or service running an SSH server on `localhost:2222` (mapped to port 22 inside the container). You can use Hydra to brute-force the SSH credentials as follows:

#### Step 1: Prepare Username and Password Lists
Hydra requires a list of usernames and passwords to attempt. You can use the default **rockyou.txt** password list or create your own.  I've included one in the repository for this week!

---

#### Step 2: Run Hydra
Use the following Hydra command to brute-force the SSH service on `localhost:2222`:

```bash
hydra -l root -P rockyou.txt ssh://127.0.0.1:2222
```

- **`-l root`**: Specifies the username (`root` in this case).  
- **`-P passwords.txt`**: Specifies the file containing the list of passwords to try.  
- **`ssh://127.0.0.1`**: Tells Hydra to target the SSH service at `127.0.0.1`.  
- **`-s 2222`**: Specifies the custom port (`2222`).

#### Example Output:
If Hydra finds valid credentials, the output will look something like this:
```plaintext
[22][ssh] host: 127.0.0.1   login: root   password: 1234
```

Now we can simply do this:
```bash
ssh root@127.0.0.1 -p 2222
```

---

### **Best Practices**
1. **Keep It Ethical**: Only use Hydra on systems you own or have explicit permission to test.
2. **Avoid Detection**: Hydra’s brute-force behavior is noisy and can trigger intrusion detection/prevention systems (IDS/IPS).
3. **Experiment Safely**: Set up a controlled environment (e.g., a Docker container) to experiment with Hydra's capabilities.



