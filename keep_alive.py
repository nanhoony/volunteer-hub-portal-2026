import urllib.request
import subprocess
import os
import sys
import datetime
import ssl

TARGET_URLS = [
    "https://volunteer-hub-recruitment-2025.surge.sh",
    "https://nanhoony-volunteer-2026.surge.sh"
]
DEPLOY_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "배포")
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "keep_alive.log")

def log(msg):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass

def check_and_revive():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    for target_url in TARGET_URLS:
        domain = target_url.replace("https://", "").replace("http://", "")
        log(f"Checking {target_url}...")
        needs_redeploy = False
        try:
            req = urllib.request.Request(
                target_url,
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) KeepAliveBot/1.0 (Surge Health Monitoring)"}
            )
            with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
                if resp.status == 200:
                    content = resp.read()
                    log(f"[{domain}] Status 200 OK (Content-Length: {len(content)} bytes)")
                else:
                    log(f"[{domain}] Unexpected status: {resp.status}")
                    needs_redeploy = True
        except Exception as e:
            log(f"[{domain}] Health check failed: {e}")
            needs_redeploy = True

        if needs_redeploy:
            log(f"[{domain}] Triggering auto-redeploy to Surge.sh...")
            try:
                cmd = f'cmd /c npx surge "{DEPLOY_DIR}" {domain}'
                res = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding="utf-8", errors="ignore", cwd=DEPLOY_DIR)
                log(f"[{domain}] Redeploy finished with return code {res.returncode}")
            except Exception as e:
                log(f"[{domain}] Error during redeploy: {e}")

if __name__ == "__main__":
    check_and_revive()
