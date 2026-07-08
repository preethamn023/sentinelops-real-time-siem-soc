import json
import time
import sys
import os
import datetime
import random

# Import mock data from api to seed the file if it doesn't exist
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
try:
    from api import MOCK_ALERTS
except ImportError:
    MOCK_ALERTS = []

ALERTS_FILE = os.path.join(os.path.dirname(__file__), 'backend', 'alerts.json')

def seed_file_if_needed():
    if not os.path.exists(ALERTS_FILE):
        print("[*] Initializing local SIEM alerts database with mock data...")
        with open(ALERTS_FILE, "w") as f:
            for alert in MOCK_ALERTS:
                f.write(json.dumps(alert) + "\n")

def generate_alert(attack_type):
    now = datetime.datetime.utcnow().isoformat() + "Z"
    alert_id = str(random.randint(10000, 99999))
    
    if attack_type == "ssh":
        alert = {
            "id": alert_id,
            "timestamp": now,
            "rule": {"level": 12, "description": "Brute force attack on SSH", "id": "5712"},
            "data": {"srcip": f"192.168.1.{random.randint(10,250)}"},
            "agent": {"name": "ubuntu-server", "ip": "10.0.0.10"},
            "location": "/var/log/auth.log"
        }
    elif attack_type == "nmap":
        alert = {
            "id": alert_id,
            "timestamp": now,
            "rule": {"level": 10, "description": "Port scan detected from external IP", "id": "40501"},
            "data": {"srcip": f"45.33.32.{random.randint(10,250)}"},
            "agent": {"name": "firewall-edge", "ip": "10.0.0.1"},
            "location": "/var/log/firewall.log"
        }
    elif attack_type == "malware":
        alert = {
            "id": alert_id,
            "timestamp": now,
            "rule": {"level": 13, "description": "Malware signature matched in file upload", "id": "62002"},
            "data": {"srcip": f"198.51.100.{random.randint(10,250)}"},
            "agent": {"name": "web-server-01", "ip": "10.0.0.5"},
            "location": "/var/log/clamav/clamd.log"
        }
    else:
        print("[-] Unknown attack type! Use: ssh, nmap, or malware")
        sys.exit(1)
        
    return alert

def main():
    if len(sys.argv) < 2:
        print("Usage: python simulate_attack.py [ssh|nmap|malware]")
        sys.exit(1)
        
    seed_file_if_needed()
    
    attack = sys.argv[1].lower()
    alert = generate_alert(attack)
    
    print(f"[*] Executing simulated {attack.upper()} attack against network...")
    time.sleep(1) # Dramatic pause
    
    # Write to alerts.json
    with open(ALERTS_FILE, "a") as f:
        f.write(json.dumps(alert) + "\n")
        
    print(f"[+] Attack triggered SIEM Rule: {alert['rule']['description']} (Severity: {alert['rule']['level']})")
    print("[+] Attack successfully logged to SIEM pipeline. Check the dashboard and your mobile device!")

if __name__ == "__main__":
    main()
