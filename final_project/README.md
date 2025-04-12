
## 🔐 **CTF Lab: CVE Exploration & Live Demo**

### **Objective**
You will investigate a real-world CVE and build a full lab environment around it — from exploitation to remediation — and demo it live!

---

## 🧪 Lab Overview

Each student (or team) will:

1. **Choose a CVE**  
   Select a CVE from the provided table or search a new one using:  
   - [CVE Search Tool](https://www.cve.org/CVERecord/SearchResults?query=python)
   - [GitHub JSON Repo](https://github.com/CVEProject/cvelistV5)

2. **Understand the CVE**  
   Research the CVE and identify:
   - What the vulnerability is
   - Why it occurs
   - How it can be exploited
   - How it can be remediated

Make life easy on yourself!  Find one is related to a programming language, like Python.  The URL for CVE Search above is hardcoded to search on Python. 

3. **Generate a Lab with AI Assistance**  
   Using ChatGPT, Claude, or another AI assistant, prompt the AI with:
   > "Create a complete lab for CVE-XXXX-YYYY including:  
   > a) a demo script to exploit it  
   > b) a remediation script  
   > c) a Dockerfile to set up the environment  
   > d) a README with setup and run instructions"

4. **Build & Test the Lab**  
   Implement the lab on your local machine or a cloud instance (Docker recommended). Test all components:
   - Exploit works as intended
   - Remediation prevents the issue
   - Docker container builds and runs cleanly
   - Instructions are clear and reproducible

5. **Present to the Class**  
   Final day of the unit, each student/team will:
   - Present the CVE and its context
   - Show the exploit running
   - Apply the remediation and show it's fixed
   - Walk through their Docker setup and writeup

---

## 🧩 Lab Requirements

Each student/team must submit:

| Element                  | Description                                                                 |
|--------------------------|-----------------------------------------------------------------------------|
| ✅ Exploit Script         | A working proof-of-concept showing the vulnerability in action             |
| ✅ Remediation Script     | Code or config that fixes the issue                                         |
| ✅ Dockerfile             | Full build of a vulnerable environment ready for testing                    |
| ✅ README.md              | Clear setup steps + how to run the exploit and remediation scripts          |

---

## 📚 Tools You Can Use

- ChatGPT / Claude / Perplexity / Bing AI for lab generation
- Docker / Docker Compose
- VSCode / GitHub
- OWASP Cheatsheets
- CVE Details / NVD Database
- Stack Overflow (use responsibly!)

---

## 🧠 Suggested Prompts for AI

Here’s a template students can use to prompt AI assistants:

> **Prompt:**  
> "I'm building a security lab for CVE-2023-47114. Can you create a Docker-based lab that includes:  
> 1. A script to demonstrate the vulnerability  
> 2. A script or patch to fix it  
> 3. A Dockerfile or Docker Compose setup  
> 4. A README with steps to run everything."

---

## 🔄 Submission 

- A D2L dropbox has been established for this assignment!  Due date is the final Monday of class - April 28, 2025. 