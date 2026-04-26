import os
import sys
import socket
from flask import Flask, Response, render_template_string
import requests
from zeroconf import ServiceInfo, Zeroconf

# --- PORTABLE PATH ---
current_dir = os.path.dirname(os.path.abspath(__file__))
lib_folder = os.path.join(current_dir, "lib")
if lib_folder not in sys.path:
    sys.path.insert(0, lib_folder)

app = Flask(__name__)
PORT = 80 # The "Invisible" Port
NAME = "pc" # Your "Cleaner" Name

@app.route('/')
def home():
    return "<h1>OS PROJECT: NODE ONLINE</h1><p>Mirroring: skmedix.pl</p>"

@app.route('/<path:path>')
def proxy(path):
    url = f"https://skmedix.pl/{path}"
    resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    return Response(resp.content, resp.status_code)

def start_broadcast():
    """This makes your computer show up as 'pc.local' to everyone else"""
    local_ip = socket.gethostbyname(socket.gethostname())
    info = ServiceInfo(
        "_http._tcp.local.",
        f"{NAME}._http._tcp.local.",
        addresses=[socket.inet_aton(local_ip)],
        port=PORT,
        properties={},
        server=f"{NAME}.local.",
    )
    zeroconf = Zeroconf()
    zeroconf.register_service(info)
    return zeroconf

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Start the "PC.local" naming broadcast
    try:
        zc = start_broadcast()
        print(f"[SUCCESS] Broadcast active: http://{NAME}.local")
    except:
        print("[WARNING] Broadcast failed. Use IP instead.")

    print(f"[SYSTEM] Listening on Port {PORT} (Invisible Mode)")
    
    # NOTE: Running on Port 80 usually requires "Run as Administrator"
    # If it fails, change PORT back to 8080.
    try:
        app.run(host='0.0.0.0', port=PORT, debug=False)
    except PermissionError:
        print("[!] PORT 80 BLOCKED. Reverting to 8080...")
        app.run(host='0.0.0.0', port=8080, debug=False)
