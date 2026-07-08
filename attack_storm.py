import json
import datetime
import os
import time
import random

ALERTS_FILE = os.path.join(os.path.dirname(__file__), 'backend', 'alerts.json')

# The full list of attacks seen in your Threat Intel dropdown
ATTACK_TYPES = [
    {"level": 12, "desc": "Brute force attack on SSH", "id": "5712", "loc": "/var/log/auth.log"},
    {"level": 2, "desc": "Config file modified on monitored path", "id": "550", "loc": "syscheck"},
    {"level": 14, "desc": "Data exfiltration pattern detected", "id": "99001", "loc": "netflow"},
    {"level": 13, "desc": "Malware signature matched in file upload", "id": "62002", "loc": "/var/log/clamav.log"},
    {"level": 7, "desc": "Multiple failed login attempts", "id": "5503", "loc": "/var/log/secure"},
    {"level": 10, "desc": "Port scan detected from external IP", "id": "40501", "loc": "/var/log/firewall.log"},
    {"level": 14, "desc": "Privilege escalation attempt", "id": "5401", "loc": "/var/log/auth.log"},
    {"level": 15, "desc": "Ransomware behavior detected", "id": "87002", "loc": "syscheck"},
    {"level": 14, "desc": "SQL Injection attempt detected", "id": "31106", "loc": "/var/log/apache2/access.log"},
    {"level": 11, "desc": "Suspicious DNS query to known C2 domain", "id": "82101", "loc": "/var/log/named.log"},
    {"level": 8, "desc": "Suspicious PowerShell execution", "id": "91234", "loc": "WinEvtLog"},
    {"level": 3, "desc": "System audit log cleared", "id": "1002", "loc": "WinEvtLog"},
    {"level": 6, "desc": "Unusual outbound traffic volume", "id": "31530", "loc": "netflow"},
    {"level": 4, "desc": "User account created outside business hours", "id": "5902", "loc": "WinEvtLog"},
    {"level": 9, "desc": "Web application firewall rule triggered", "id": "31301", "loc": "/var/log/modsec.log"}
]

def generate_random_ip():
    return f"{random.randint(11,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"

print("=====================================================")
print("  ⚠️ INITIATING GLOBAL CYBER ATTACK SIMULATION ⚠️")
print("=====================================================")
print("Injecting all known MITRE ATT&CK framework vectors...")

for i in range(20): # Generate 20 random attacks
    attack = random.choice(ATTACK_TYPES)
    src_ip = generate_random_ip()
    now = datetime.datetime.utcnow().isoformat() + "Z"
    
    alert = {
        "id": str(random.randint(100000, 999999)),
        "timestamp": now,
        "rule": {
            "level": attack["level"],
            "description": attack["desc"],
            "id": attack["id"]
        },
        "data": {"srcip": src_ip},
        "agent": {"name": f"sensor-{random.randint(1,5)}", "ip": "10.0.0.1"},
        "location": attack["loc"]
    }
    
    with open(ALERTS_FILE, "a") as f:
        f.write(json.dumps(alert) + "\n")
        
    print(f"[🔥] Fired: {attack['desc']} (IP: {src_ip})")
    time.sleep(1.5) # Wait 1.5 seconds between attacks so the dashboard charts look cool

print("=====================================================")
print("[+] SIMULATION COMPLETE. Check your SOC Dashboard!")
