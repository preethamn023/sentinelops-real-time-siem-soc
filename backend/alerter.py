import time
import requests
import sys

# Your Telegram Bot Token
TELEGRAM_TOKEN = "8834001291:AAHCIM4Je2_OKohtFJMxeDHzYDRR6RfYuQc"
CHAT_ID = "1158931153"  # Hardcoded from previous detection

# The URL to the local SentinelOPS API
API_URL = "http://127.0.0.1:5000/api/events"

# Keep track of alerts we've already sent to avoid spam
SEEN_ALERTS = set()

def get_chat_id():
    print("[*] Attempting to auto-detect your Telegram Chat ID...")
    print("[*] PLEASE OPEN TELEGRAM AND SEND ANY MESSAGE (like 'hello') TO @benakabot RIGHT NOW.")
    
    for i in range(30):
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
            resp = requests.get(url, timeout=5).json()
            if resp.get("ok") and len(resp.get("result", [])) > 0:
                # Get the chat ID of the most recent message received
                chat_id = resp["result"][-1]["message"]["chat"]["id"]
                print(f"\n[+] Success! Found your Chat ID: {chat_id}")
                return str(chat_id)
        except Exception as e:
            pass
        
        print(".", end="", flush=True)
        time.sleep(2)
    
    print("\n[-] Could not detect a message. Please send a message to the bot and try running this again.")
    sys.exit(1)

def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"Failed to send telegram message: {e}", flush=True)

def monitor_alerts(chat_id):
    print(f"[*] Monitoring for Critical & High severity alerts...", flush=True)
    while True:
        try:
            resp = requests.get(API_URL, timeout=5)
            if resp.status_code == 200:
                events = resp.json()
                
                # Reverse to process oldest first
                for event in reversed(events):
                    alert_id = event.get("id")
                    
                    if alert_id and alert_id not in SEEN_ALERTS:
                        SEEN_ALERTS.add(alert_id)
                        severity = event.get("severity", "LOW")
                        
                        # Only alert on CRIT or HIGH threats
                        if severity in ["CRIT", "HIGH"]:
                            msg = f"🚨 **SENTINELOPS SECURITY ALERT** 🚨\n\n"
                            msg += f"**Severity:** {severity}\n"
                            msg += f"**Attack Type:** {event.get('rule_name', 'Unknown')}\n"
                            msg += f"**Source IP:** `{event.get('source_ip', 'Unknown')}`\n"
                            msg += f"**Timestamp:** {event.get('timestamp', 'Unknown')}\n"
                            
                            print(f"[!] Sending alert for rule {event.get('rule_id')} ({severity})", flush=True)
                            send_telegram_message(chat_id, msg)
        except requests.exceptions.ConnectionError:
            print("[-] Cannot connect to API. Is backend/api.py running?")
        except Exception as e:
            print(f"[-] Error fetching alerts: {e}")
            
        # Wait 5 seconds before checking again
        time.sleep(5)

if __name__ == "__main__":
    import os
    os.environ['PYTHONUNBUFFERED'] = '1'
    
    chat_id = CHAT_ID
    if not chat_id:
        chat_id = get_chat_id()
    
    # Pre-load existing alerts so we don't spam historical alerts on startup
    print("[*] Connecting to SentinelOPS API...", flush=True)
    try:
        resp = requests.get(API_URL, timeout=5)
        if resp.status_code == 200:
            for ev in resp.json():
                if "id" in ev:
                    SEEN_ALERTS.add(ev["id"])
            print(f"[+] Loaded {len(SEEN_ALERTS)} historical alerts. Ready for NEW attacks!", flush=True)
    except:
        print("[-] Could not preload alerts. API might be down.", flush=True)

    # Send a startup notification
    send_telegram_message(chat_id, "✅ **SentinelOPS Alerter** is now ONLINE and monitoring the network.")
    monitor_alerts(chat_id)
