import urllib.request
import subprocess
import os
import sys
import datetime

TARGET_URL = "https://volunteer-portal-live-2026.surge.sh"
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
    log(f"Checking {TARGET_URL}...")
    needs_redeploy = False
    try:
        req = urllib.request.Request(
            TARGET_URL,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) KeepAliveBot/1.0"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status == 200:
                log(f"Status 200 OK (Content-Length: {len(resp.read())} bytes)")
            else:
                log(f"Unexpected status: {resp.status}")
                needs_redeploy = True
    except Exception as e:
        log(f"Health check failed: {e}")
        needs_redeploy = True

    if needs_redeploy:
        log("Triggering auto-redeploy to Surge.sh...")
        try:
            cmd = f'cmd /c npx surge "{DEPLOY_DIR}" volunteer-portal-live-2026.surge.sh'
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=DEPLOY_DIR)
            log(f"Redeploy finished. Return code: {res.returncode}")
            if res.stdout:
                log(f"Stdout snippet: {res.stdout[-300:]}")
            if res.stderr:
                log(f"Stderr: {res.stderr}")
        except Exception as e:
            log(f"Error during redeploy: {e}")

if __name__ == "__main__":
    check_and_revive()
