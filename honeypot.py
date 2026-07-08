import socket
import json
import datetime
import os
import threading
import time

ALERTS_FILE = os.path.join(os.path.dirname(__file__), 'backend', 'alerts.json')

def log_attack(src_ip, alert_desc, level, rule_id):
    now = datetime.datetime.utcnow().isoformat() + "Z"
    alert = {
        "id": str(abs(hash(now + src_ip)))[-6:],
        "timestamp": now,
        "rule": {"level": level, "description": alert_desc, "id": rule_id},
        "data": {"srcip": src_ip},
        "agent": {"name": "windows-sensor", "ip": "127.0.0.1"},
        "location": "smart-honeypot"
    }
    with open(ALERTS_FILE, "a") as f:
        f.write(json.dumps(alert) + "\n")

def get_login_html():
    try:
        with open(os.path.join(os.path.dirname(__file__), "login.html"), "r") as f:
            return f.read()
    except Exception as e:
        return "<html><body><h1>Enterprise Secure Portal</h1></body></html>"

def get_error_html(msg):
    return f"""<!DOCTYPE html><html>
    <head><meta charset="utf-8"><style>body{{background:#0f2027;color:#ff4b4b;font-family:'Inter',sans-serif;text-align:center;padding-top:100px;}}</style></head>
    <body><h2>🚨 SECURITY ALERT 🚨</h2><h1>{msg}</h1><p>This incident has been logged and reported to the SOC.</p><br><a href="/" style="color:white;text-decoration:none;border-bottom:1px solid white;">Return to Safety</a></body>
    </html>"""

def get_success_html():
    return f"""<!DOCTYPE html><html>
    <head><meta charset="utf-8"><style>body{{background:#0f2027;color:#00ff9d;font-family:'Inter',sans-serif;text-align:center;padding-top:100px;}}</style></head>
    <body><h2>✅ AUTHENTICATION SUCCESSFUL ✅</h2><h1>Welcome Administrator</h1><p>Demonstration Login Successful. No threats detected.</p><br><a href="/" style="color:white;text-decoration:none;border-bottom:1px solid white;">Log Out</a></body>
    </html>"""

def start_smart_honeypot(port, name):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind(("0.0.0.0", port))
        server.listen(5)
        print(f"[*] {name} Sensor listening on port {port}...")
    except Exception as e:
        print(f"[-] Could not bind to port {port}: {e}")
        return
        
    while True:
        try:
            client, addr = server.accept()
            src_ip = addr[0]
            client.settimeout(1.0) # Wait 1 second for data
            
            # Default fallback alert
            alert_desc = f"Real-Time Port Scan Detected!"
            level = 10
            rule_id = "40501"
            
            try:
                data = client.recv(4096).decode('utf-8', errors='ignore')
                data_upper = data.upper()
                
                # Payload Inspection (Smart Detection)
                if port == 8081:
                    if data_upper.startswith("GET"):
                        if "WGET" in data_upper or "CURL" in data_upper:
                            alert_desc = "Web application firewall rule triggered"
                            level = 9; rule_id = "31301"
                            log_attack(src_ip, alert_desc, level, rule_id)
                            print(f"\n[🚨] TRIGGERED: {alert_desc} from {src_ip}!", flush=True)
                            err_bytes = get_error_html("Access Denied by WAF").encode('utf-8')
                            client.sendall(f"HTTP/1.1 403 Forbidden\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: {len(err_bytes)}\r\n\r\n".encode('utf-8') + err_bytes)
                        else:
                            # Serve login page normally
                            html_bytes = get_login_html().encode('utf-8')
                            client.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: {len(html_bytes)}\r\n\r\n".encode('utf-8') + html_bytes)
                        client.close()
                        continue
                    elif data_upper.startswith("POST"):
                        if "OR 1=1" in data_upper or "UNION SELECT" in data_upper or "%27" in data_upper or "ADMIN'" in data_upper:
                            alert_desc = "SQL Injection attempt detected"
                            level = 14; rule_id = "31106"
                            log_attack(src_ip, alert_desc, level, rule_id)
                            print(f"\n[🚨] TRIGGERED: {alert_desc} from {src_ip}!", flush=True)
                            err_bytes = get_error_html("SQL Injection Blocked by SentinelOPS").encode('utf-8')
                            client.sendall(f"HTTP/1.1 403 Forbidden\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: {len(err_bytes)}\r\n\r\n".encode('utf-8') + err_bytes)
                        elif "USERNAME=ADMIN&PASSWORD=PASSWORD123" in data_upper:
                            print(f"\n[+] Demonstration login success from {src_ip} (No alert triggered)", flush=True)
                            succ_bytes = get_success_html().encode('utf-8')
                            client.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: {len(succ_bytes)}\r\n\r\n".encode('utf-8') + succ_bytes)
                        else:
                            alert_desc = "Suspicious login attempt detected on Honeypot"
                            level = 10; rule_id = "5503"
                            log_attack(src_ip, alert_desc, level, rule_id)
                            print(f"\n[🚨] TRIGGERED: {alert_desc} from {src_ip}!", flush=True)
                            err_bytes = get_error_html("Invalid Credentials").encode('utf-8')
                            client.sendall(f"HTTP/1.1 403 Forbidden\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: {len(err_bytes)}\r\n\r\n".encode('utf-8') + err_bytes)
                        client.close()
                        continue
                        
                elif port == 2222:
                    alert_desc = "Brute force attack on SSH"
                    level = 12; rule_id = "5712"
                    
                elif port == 3306:
                    alert_desc = "Data exfiltration pattern detected"
                    level = 14; rule_id = "99001"
                    
                elif port == 21:
                    alert_desc = "Malware signature matched in file upload"
                    level = 13; rule_id = "62002"
            
            except Exception:
                pass # If timeout or no data, stick to default Port Scan alert
                
            log_attack(src_ip, alert_desc, level, rule_id)
            print(f"\n[🚨] TRIGGERED: {alert_desc} from {src_ip}!", flush=True)
            
            try:
                client.send(b"Access Denied\n")
            except:
                pass
            client.close()
        except Exception as e:
            pass

if __name__ == "__main__":
    print("==================================================")
    print("   SentinelOPS SMART Honeypot Sensors")
    print("==================================================")
    
    threading.Thread(target=start_smart_honeypot, args=(2222, "SSH"), daemon=True).start()
    threading.Thread(target=start_smart_honeypot, args=(8081, "HTTP"), daemon=True).start()
    threading.Thread(target=start_smart_honeypot, args=(3306, "MySQL"), daemon=True).start()
    threading.Thread(target=start_smart_honeypot, args=(21, "FTP"), daemon=True).start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[*] Shutting down sensors...")
