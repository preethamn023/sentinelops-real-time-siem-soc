# 🛡️ SentinelOPS A-Z Demonstration Guide

This guide contains everything you need to know to launch the project from a cold start, execute real-world network attacks from WSL, trigger automated incident response, and impress your audience with a flawless demonstration.

---

## 🛠️ Step 1: Launch the Infrastructure

Before you start presenting, you need to spin up the 3 core components of the SIEM pipeline. Open three separate Windows terminals (Command Prompt or PowerShell) inside your project folder (`C:\Users\preet\Desktop\sentinelops-real-time-siem-soc-main`).

**Terminal 1: Start the Backend API**
This processes security logs and serves data to the dashboard.
```bash
python backend/api.py
```

**Terminal 2: Start the Telegram Alerter**
This monitors the API and sends push notifications to your phone.
```bash
python backend/alerter.py
```
*(Wait until you see the "SentinelOPS Alerter is now ONLINE" message).*

**Terminal 3: Start the Smart Honeypot Sensors**
This creates fake, vulnerable ports on your Windows machine to trap hackers and actively inspect their payloads.
```bash
python honeypot.py
```

---

## 📊 Step 2: Open the SOC Dashboard

Now that the backend is running, open your web browser (Chrome, Edge, etc.) and navigate to:
👉 **http://127.0.0.1:5000**

You should see the SentinelOPS dashboard. Keep this open on your screen—this is the main visual element of your presentation!

---

## 🎬 Step 3: The Live Demonstration

### 1. Introduce the Dashboard
Start by explaining what the audience is looking at. 
> *"This is SentinelOPS, a Real-Time Security Operations Center. It continuously monitors network traffic and system logs. The dashboard tracks the total events, identifies critical threats, and maps attacker IP addresses using the MITRE ATT&CK framework."*

### 2. Set the Scene
> *"To demonstrate how this works, we are going to perform a live reconnaissance attack. I am going to switch over to my Kali Linux (WSL) terminal and act as a malicious hacker trying to find a vulnerability in our network."*

### 3. Launch the Attack (From WSL)
Open your **WSL Terminal** (Kali Linux). We are going to run an industry-standard Nmap Port Scan to look for vulnerabilities across multiple protocols at once (SSH, Web, Database, and FTP).

Run this command in WSL against your Windows host IP:
```bash
nmap -p 2222,8080,3306,21 172.20.96.1
```

### 4. Show the Results (The "Wow" Factor)
As soon as you hit Enter in WSL, point back to the Web Dashboard and pull out your phone.
> *"Our hacker just touched our SSH port. Because we set up Smart Honeypot sensors on our host machine, the SIEM pipeline immediately trapped them. If you look at the Dashboard, you'll see a live 'Brute force attack on SSH' alert with my WSL's real IP address."*
> 
> *"But security engineers can't stare at a dashboard all day. Notice my phone..."*

*(Show your phone to the audience as the Telegram notification buzzes).* 
> *"Because this was a severe event, the system instantly fired an automated incident response alert to my mobile device via the Telegram Bot API."*

---

## 🌩️ Step 4: The Grand Finale (The Attack Storm)

To end your presentation on a high note, you can simulate a massive, global cyber attack to show off the Analytics and Threat Intel features.

> *"Finally, let's see what happens during a full-scale Advanced Persistent Threat (APT) attack."*

Open a standard Windows Terminal and run:
```bash
python attack_storm.py
```

*(While it runs, click through the tabs on the dashboard)*
> *"I've just initiated a global cyber attack simulation. Watch the Live Event feed explode with Ransomware, SQL Injections, and Malware events. If we click over to the Analytics tab, you can see our 'Events Per Hour' chart spiking drastically. And in the Threat Intel tab, our database is rapidly populating with the real-time IP addresses of our attackers."*

---

## ❓ Frequently Asked Questions (To memorize for the demo)

**Q: Why didn't you use Wazuh directly for the demo?**
**A:** Wazuh requires a heavy, dedicated Linux Enterprise server. To make this demo portable and run natively on Windows, I engineered a custom Python Smart Honeypot script that exactly mimics the behavior of a Wazuh agent by capturing network traffic, inspecting payloads, and pushing it into the SIEM pipeline.

**Q: How does the Telegram Alerter work?**
**A:** It constantly polls the local Flask API. When it detects a new event with a "HIGH" or "CRIT" severity tag, it formats the data into Markdown and issues a POST request to the official Telegram Bot API using a secure bot token.

**Q: Can you detect specific payloads?**
**A:** Yes. The Smart Honeypot actively reads the incoming packets. If it detects a SQL string like `' OR 1=1`, it flags it as an SQL Injection. If it detects SSH connection attempts, it flags it as an SSH Brute Force.
