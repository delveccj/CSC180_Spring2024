# Lockdown Overview #

Welcome to a lecture that will explain how a lockdown work.  It is like a CTF but in reverse.  You are in control of a network and it has bunch of exploits and vulnerabilities.  Worse, people have infected your system and are crusing through the network to create chaos. 

You instructor worked with ChatGPT to create these instructions.  He guided on what he wanted, it provided the content.  But note, the instructor had to guide the agent and refine what it focused on.  This is exactly how ChatGPT can be useful - it would have taken me forever to type up this description even though I know what it does!

### **Creating the Network**
---
It is a pretty involved network.  We can't possibly replicate all of it.  However, we can replicate *some* of it.  Take a look a this file `docker-compose.yml`  It will literally establish elements of the network and connect them together!

---

## **📜 Docker Compose File (`docker-compose.yml`)**
Here’s the file again:

```yaml
version: '3.8'

services:
  web:
    build: .
    container_name: web_server
    ports:
      - "8080:80"
    depends_on:
      - db
    networks:
      - lockdown_net

  db:
    image: mysql:5.7
    container_name: mysql_server
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: tickitnow
      MYSQL_USER: tickit
      MYSQL_PASSWORD: tickitpass
    ports:
      - "3306:3306"
    networks:
      - lockdown_net

  ftp:
    build: .
    container_name: ftp_server
    ports:
      - "21:21"
    networks:
      - lockdown_net

networks:
  lockdown_net:
    name: lockdown_net
    driver: bridge
```

---

### **🧐 What Does This File Do?**
Think of **`docker-compose.yml`** as a script that tells Docker:  
*"Hey, I want to run multiple containers together as one system!"*

### **🔍 Breaking It Down**
#### **1️⃣ Defining the Compose Version**
```yaml
version: '3.8'
```
- This tells Docker **which version of Docker Compose syntax** we are using.  
- Version **3.8** is a good modern choice for compatibility.

#### **2️⃣ Services Section (This Defines Our Apps)**
Each "service" is like an **app running inside a container**.

##### **🔹 Web Server (`web`)**
```yaml
web:
  build: .
  container_name: web_server
  ports:
    - "8080:80"
  depends_on:
    - db
  networks:
    - lockdown_net
```
- **`build: .`** → Build the container **using the `Dockerfile`** in this directory.  
- **`container_name: web_server`** → The container’s name is `web_server`.  
- **`ports: - "8080:80"`** →  
  - Maps **port 8080 on your computer** 🏠 → **port 80 inside the container** 🌍.  
  - So if you go to **http://localhost:8080**, you’ll see the web server!  
- **`depends_on: - db`** → The web server **waits for the database** (`db`) to start before running.  
- **`networks: - lockdown_net`** → Connects this container to the **lockdown_net** network.

---

##### **🔹 Database (`db`)**
```yaml
db:
  image: mysql:5.7
  container_name: mysql_server
  restart: always
  environment:
    MYSQL_ROOT_PASSWORD: root
    MYSQL_DATABASE: tickitnow
    MYSQL_USER: tickit
    MYSQL_PASSWORD: tickitpass
  ports:
    - "3306:3306"
  networks:
    - lockdown_net
```
- **`image: mysql:5.7`** → Instead of building a new container, it **downloads MySQL 5.7** from Docker Hub.  
- **`container_name: mysql_server`** → The container is named `mysql_server`.  
- **`restart: always`** → If the container crashes, it **automatically restarts**.  
- **`environment:`** → Sets MySQL **login credentials**:
  - `MYSQL_ROOT_PASSWORD: root` → Password for **root user**.  
  - `MYSQL_DATABASE: tickitnow` → Creates a **database named `tickitnow`**.  
  - `MYSQL_USER: tickit`, `MYSQL_PASSWORD: tickitpass` → Creates a **new database user**.  
- **`ports: - "3306:3306"`** →  
  - Maps **port 3306 on your computer** 🏠 → **port 3306 inside MySQL** 📦.  
  - This lets **web apps connect to the database**.  
- **`networks: - lockdown_net`** → Connects to the **lockdown_net** network.

---

##### **🔹 FTP Server (`ftp`)**
```yaml
ftp:
  build: .
  container_name: ftp_server
  ports:
    - "21:21"
  networks:
    - lockdown_net
```
- **`build: .`** → Uses the **same `Dockerfile`** as the web server (for simplicity).  
- **`container_name: ftp_server`** → The container name is `ftp_server`.  
- **`ports: - "21:21"`** →  
  - Maps **port 21 on your computer** 🏠 → **port 21 inside the container** (for FTP).  
- **`networks: - lockdown_net`** → Connects to the **lockdown_net** network.

---

#### **3️⃣ Network Section**
```yaml
networks:
  lockdown_net:
    name: lockdown_net
    driver: bridge
```
- **`name: lockdown_net`** → Forces Docker to use a **fixed network name** instead of a random one.  
- **`driver: bridge`** → Uses **Docker’s built-in virtual network** for containers.  

💡 **This allows all containers to talk to each other privately, just like a LAN (Local Area Network).**

---

## **📜 Dockerfile**
Here’s the file:

```dockerfile
# Base image
FROM ubuntu:20.04

# Set environment variables to prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Update and install necessary services
RUN apt-get update && apt-get install -y \
    apache2 \
    mysql-server \
    vsftpd \
    openssh-server \
    iputils-ping \
    net-tools \
    && apt-get clean

# Enable Apache and MySQL to start at boot
RUN systemctl enable apache2 && systemctl enable mysql

# Set up SSH (default password for root is 'root' for testing purposes)
RUN mkdir /var/run/sshd && echo 'root:root' | chpasswd
EXPOSE 22 80 3306 21

# Start necessary services when the container starts
CMD service apache2 start && service mysql start && service vsftpd start && /usr/sbin/sshd -D
```

---

### **🧐 What Does This Dockerfile Do?**
This **creates a custom Linux server image** for our web and FTP services.

### **🔍 Breaking It Down**
- **`FROM ubuntu:20.04`** → Uses **Ubuntu 20.04** as the base system.  
- **`ENV DEBIAN_FRONTEND=noninteractive`** → Prevents **interactive prompts** during installation.  
- **`RUN apt-get update && apt-get install -y ...`**  
  - Installs **Apache (Web Server)** 🌍  
  - Installs **MySQL (Database)** 🗄  
  - Installs **vsftpd (FTP Server)** 📂  
  - Installs **SSH (Remote Access)** 🔐  
  - Installs **ping/net-tools** for networking  
- **`RUN systemctl enable apache2 && systemctl enable mysql`**  
  - Ensures **Apache & MySQL start automatically**.  
- **`RUN mkdir /var/run/sshd && echo 'root:root' | chpasswd`**  
  - Creates an SSH **root user with password `root` (for testing)**.  
- **`EXPOSE 22 80 3306 21`**  
  - **Tells Docker to allow traffic on these ports:**  
    - **22** → SSH  
    - **80** → Web Server  
    - **3306** → MySQL  
    - **21** → FTP  
- **`CMD ...`**  
  - Starts **Apache, MySQL, FTP, and SSH** when the container runs.  

---

## **🔍 The Magic of Docker Networking**
Docker uses **virtual networking** to give containers their **own unique IP addresses**, even though they run on the same physical machine (your computer).

Here’s **how** this happens:

### **1️⃣ Containers Run in a Virtual Network**
When you run:
```sh
docker-compose up -d
```
Docker **automatically creates a virtual network** (in our case, `lockdown_net`). This network behaves **like a LAN (Local Area Network)** inside Docker.

Each container **joins this network** and gets a **private IP address**, like:
- `web_server` → `172.19.0.4`
- `ftp_server` → `172.19.0.2`
- `mysql_server` → `172.19.0.3`

These IPs come from **Docker’s internal DHCP system**, which assigns an IP **just like a home router** assigns IPs to devices on Wi-Fi.

💡 **Think of each container as a separate computer plugged into the same network switch.**  

---

### **2️⃣ Bridge Networking Makes It Work**
In our `docker-compose.yml`, we specified:
```yaml
networks:
  lockdown_net:
    driver: bridge
```
- `bridge` mode means **Docker creates an internal "virtual switch".**  
- All containers attached to `lockdown_net` can **talk to each other** as if they were on the same local network.

You can test this:
```sh
docker exec -it web_server ping mysql_server
```
If it works, the **web server can "see" the database server** via the network.

💡 **Even though all containers run on the same physical machine, Docker makes them act like separate computers on a network.**

---

### **3️⃣ Why Doesn’t Everything Use `localhost`?**
You might think: *“Why don’t we just use `localhost` to connect services?”*  
Here’s why:

| Scenario | What Happens |
|----------|-------------|
| **`localhost` inside a container** | Refers to *only that container*, not others. |
| **Container-to-Container communication** | Uses Docker’s internal IPs (`172.19.x.x`). |
| **Accessing from your computer** | You use `localhost:8080` (because of port mapping). |

💡 **Docker containers act like separate virtual computers, so they need real network addresses.**  

---

## **🛠 Recap: How Containers Get Separate IPs**
1. **Docker creates a virtual network (`lockdown_net`).**  
2. **Each container joins this network** and gets its own **IP address**.  
3. **They talk to each other using internal IPs** (`172.19.x.x`).  
4. **Your computer accesses them using `localhost:PORT`** because of **port mapping**.  



I can't directly draw images here, but I can **create an ASCII diagram** that visually represents how Docker assigns IPs to containers and connects them through the virtual network.  

---

### **🌍 Docker Networking - Visual Representation**
```
                 🏠 Your Computer (Host Machine)
                         │
     ┌───────────────────┴───────────────────┐
     │        Docker Virtual Network         │
     │          (lockdown_net)               │
     │       IP Range: 172.19.0.0/16         │
     ├──────────────┬──────────────┬────────┤
     │              │              │        │
     ▼              ▼              ▼        ▼
┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐
│ web_server│  │ db_server │  │ ftp_server│  │ other_srv │
│  Apache   │  │  MySQL    │  │   vsftpd  │  │   (etc.)  │
│ IP: .4    │  │ IP: .3    │  │ IP: .2    │  │ IP: .5    │
└───────────┘  └───────────┘  └───────────┘  └───────────┘
      ▲               ▲               ▲
      │               │               │
      └────────── Communicate with each other ───────────┘
      
```
---

### **🛠 Explanation of This Diagram**
1. Your **computer** (host machine) runs Docker, which creates a **virtual network** (`lockdown_net`).
2. This network has an **IP range** of `172.19.0.0/16` (like a home router assigns IPs).
3. Each **container** is assigned an IP:
   - `web_server (Apache)` → `172.19.0.4`
   - `db_server (MySQL)` → `172.19.0.3`
   - `ftp_server (vsftpd)` → `172.19.0.2`
4. Containers **talk to each other** through **internal Docker networking**, not `localhost`.  
5. You (the user) **can access the web server** via:
   ```sh
   http://localhost:8080  # Because we mapped port 8080 → 80
   ```
6. The **web server can talk to MySQL** using:
   ```sh
   mysql -h 172.19.0.3 -u tickit -p
   ```
   (Instead of `localhost`, it uses the **internal network IP**).  

---

### **🧐 Why Is This Useful?**
- **Encapsulation**: Each service runs in its own isolated environment.  
- **No conflicts**: You can run multiple web servers/databases without interfering.  
- **Better security**: Internal communication stays within Docker.  

Would this make sense for your students? Let me know if you'd like an even simpler version! 🚀
### **🔍 What This Command Does?**
The command:  

```
docker network inspect lockdown_lockdown_net
```
**Asks Docker to show details about the network** named `lockdown_lockdown_net`. This is a **virtual network** that Docker created to allow the different containers (services like the web server, database, and FTP server) to communicate with each other.

---

### **📝 Explanation of Each Section**  

#### ✅ **1. Network Name & ID**  
```json
"Name": "lockdown_lockdown_net",
"Id": "57e9049b9b44cebd852cd7e5da83ea1f29f9e5924ad6deaea0bd291d2ff7561a",
```
- `Name`: This is the **name of the network** Docker created.  
- `Id`: A **unique identifier** for this network (just like how every device has a unique serial number).  

💡 **Think of this as the name and ID of a Wi-Fi network inside Docker.**

---

#### ✅ **2. Network Type & Scope**  
```json
"Scope": "local",
"Driver": "bridge",
```
- `Scope`: `local` means the network **only exists on this computer** (not shared across multiple machines).  
- `Driver`: `bridge` means it's a **virtual network** that lets containers communicate **like they're connected to a real network switch**.  

💡 **Think of this as a home Wi-Fi network that only exists inside your computer.**

---

#### ✅ **3. IP Addressing (How Devices Get Their Addresses)**  
```json
"IPAM": {
    "Driver": "default",
    "Config": [
        {
            "Subnet": "172.19.0.0/16",
            "Gateway": "172.19.0.1"
        }
    ]
}
```
- `Subnet`: The **range of IP addresses** used in this network (`172.19.0.0` to `172.19.255.255`).  
- `Gateway`: `172.19.0.1` is the **"router"** for this network (the address containers use to send data outside this network).  

💡 **Think of this as the router in your house that assigns IP addresses to your devices.**  

---

#### ✅ **4. Containers (Devices on the Network)**
This section lists the **containers connected to this network**, including their **names, IP addresses, and MAC addresses**.

##### 🔹 **Container 1: Web Server**
```json
"2752699fd56256815d93ec343d2728a99b67d59b95dee828aabf070368301f8c": {
    "Name": "web_server",
    "MacAddress": "02:42:ac:13:00:04",
    "IPv4Address": "172.19.0.4/16"
}
```
- **Container Name**: `web_server`  
- **IP Address**: `172.19.0.4` (This is how other services find it)  
- **MAC Address**: `02:42:ac:13:00:04` (Like a unique fingerprint for networking)  

##### 🔹 **Container 2: FTP Server**
```json
"4a0343cca4e0eb479f46e5214a59c78d1ecee62bb869602590d9689b7f296ff5": {
    "Name": "ftp_server",
    "MacAddress": "02:42:ac:13:00:02",
    "IPv4Address": "172.19.0.2/16"
}
```
- **Container Name**: `ftp_server`  
- **IP Address**: `172.19.0.2`  

##### 🔹 **Container 3: MySQL Database Server**
```json
"6f4b2a027f68f752073e16bb75862d81eccd04d10aeda67a71cc90368fd6ecd1": {
    "Name": "mysql_server",
    "MacAddress": "02:42:ac:13:00:03",
    "IPv4Address": "172.19.0.3/16"
}
```
- **Container Name**: `mysql_server`  
- **IP Address**: `172.19.0.3`  

💡 **Think of this as listing all the devices connected to your Wi-Fi network, like your laptop, phone, and smart TV. Each device gets a unique IP address.**

---

#### ✅ **5. Additional Docker-Specific Info**
```json
"Labels": {
    "com.docker.compose.network": "lockdown_net",
    "com.docker.compose.project": "lockdown"
}
```
- **Docker Compose Project Name**: `lockdown`  
- **Network Name Inside Compose**: `lockdown_net`  

💡 **This tells us that this network was created by Docker Compose, not manually.**


---

## **📌 Exercise Goal: "Hack Your Friend’s Database!"**
1. **Step 1: Connect to another student's MySQL database** using the default weak credentials.
2. **Step 2: Change the root password** to secure it.
3. **Step 3: Reconnect using the new password** and confirm the change.

---

## **🛠 Step-by-Step Instructions**
### **1️⃣ Step 1: Find Another Student’s Host IP**
Each student’s machine (running Docker) has its **own host IP** on the lab network.  
- Run this on your machine to find **your IP**:
  ```sh
  ip a   # On Linux/macOS
  ipconfig   # On Windows
  ```
  Look for something like **`192.168.1.105`** (this is your **host machine’s IP** in the lab).  

- Now, **exchange IPs** with another student.

---

### **2️⃣ Step 2: Connect to Their MySQL Database**
Now, try logging into their MySQL **remotely** using their host machine’s IP.  

```sh
mysql -h 192.168.1.105 -P 3306 -u root -p
```
- **Replace `192.168.1.105`** with the **other student’s IP**.  
- When prompted, enter the **default password** (`root`).  
- If successful, you now have **full control over their database!** 😈

💡 **This simulates a real-world security risk:**  
*"If a database has a weak password, anyone on the network can log in!"*

---

### **3️⃣ Step 3: Change the Root Password**
Now, **secure their database** by changing the root password:  
```sql
ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'NewSecureP@ss!';
FLUSH PRIVILEGES;
```
💡 **Make sure you write down the new password!** 😆

---

### **4️⃣ Step 4: Try Reconnecting with the New Password**
Now, test the security fix:  
- Try logging in again using the **old password (`root`)**—it should **fail**!  
- Try logging in with the **new password**—it should **work**!  

```sh
mysql -h 192.168.1.105 -P 3306 -u root -p
```
(Use the new password when prompted.)

---

### **Step 5: Houston We Have a Problem** 
Even if you, as the protector, **change the root password**, any **already connected user** will **still have access** **until** they disconnect! This is a **huge security risk** because an attacker **can stay inside** the database session **even after their credentials are changed**.  

### **🔍 How to Monitor Active Connections to the MySQL Database**
You need to:
1. **List active connections** (to see who is connected).  
2. **Kick out attackers** (forcefully close their session).  

---

## **📌 Step 1: Check Active Connections**
To login to your local MySQL server (the one running in your container) - you need to issue this command:

```sh
mysql -h 127.0.0.1 -P 3306 -u root -p

```

Once you are inside MySQL, run this:  
```sql
SHOW PROCESSLIST;
```
This will display **who is connected** and what they’re doing.  

### **🔍 Example Output**
| Id  | User  | Host          | DB         | Command | Time | State      | Info  |
|-----|-------|--------------|------------|---------|------|------------|-------|
| 101 | root  | 192.168.1.110 | tickitnow  | Query   | 12   | Sleeping   | NULL  |
| 102 | root  | 192.168.1.105 | tickitnow  | Query   | 5    | Executing  | SELECT * FROM users;  |
| 103 | tickit | 172.19.0.4   | tickitnow  | Query   | 3    | Running    | INSERT INTO tickets VALUES... |

💡 **What this tells us:**  
- Someone from **192.168.1.110** (another student) is **connected as root**.  
- Someone from **192.168.1.105** is running a **query to dump user data** (possible hacker).  
- A **container (172.19.0.4)** is using the `tickit` user for normal operations.

---

## **📌 Step 2: Kill a Suspicious Connection**
If you see an **unwanted user still inside the database**, **kick them out**! 🚪💥  

1. Find their **process ID (`Id` column)** from `SHOW PROCESSLIST;`.  
2. Kill their session:
   ```sql
   KILL 102;
   ```
   (Replace `102` with the actual **Id** of the suspicious connection.)  

💡 **Now they are forcefully disconnected!** If they try to reconnect, they’ll need the **new password**—but **they don’t know it anymore!**  

---

## **📌 Step 3: Apply Security Fixes**
After kicking them out, **prevent future intrusions** by:
1. **Immediately changing the root password (again)**
   ```sql
   ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'UltraSecureP@ss!';
   FLUSH PRIVILEGES;
   ```
2. **Restrict remote access to MySQL** so only `localhost` can connect:
   ```sql
   ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'SuperSecure123!';
   CREATE USER 'root'@'localhost' IDENTIFIED BY 'LocalOnlyPass!';
   FLUSH PRIVILEGES;
   ```
   Now, **only connections from the local machine** (Docker container) will work.  

---

## **📌 Bonus: Monitor Active Users in Real-Time**
Instead of manually running `SHOW PROCESSLIST;`, you can **watch connections live** using this command:
```sh
watch -n 2 "docker exec -it mysql_server mysql -uroot -p'yourpassword' -e 'SHOW PROCESSLIST;'"
```
---

