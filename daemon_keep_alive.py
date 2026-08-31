import urllib.request
import subprocess
import os
import time
import datetime

TARGET_URLS = [
    "https://volunteer-hub-recruitment-2025.surge.sh",
    "https://volunteer-hub-portal-2026.surge.sh"
]
DEPLOY_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "배포")
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "keep_alive.log")

def log(msg):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line, flush=True)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass

def ping_and_revive():
    for target_url in TARGET_URLS:
        domain = target_url.replace("https://", "").replace("http://", "")
        needs_redeploy = False
        try:
            req = urllib.request.Request(
                target_url,
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) KeepAliveDaemon/1.0"}
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                if resp.status == 200:
                    log(f"[KEEP-ALIVE] {target_url} is healthy (200 OK)")
                else:
                    log(f"[WARNING] {target_url} status: {resp.status}")
                    needs_redeploy = True
        except Exception as e:
            log(f"[ERROR] Connection check failed for {target_url}: {e}")
            needs_redeploy = True

        if needs_redeploy:
            log(f"[AUTO-REVIVE] Triggering automatic redeploy to {domain}...")
            try:
                cmd = f'cmd /c npx surge "{DEPLOY_DIR}" {domain}'
                res = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=DEPLOY_DIR)
                log(f"[AUTO-REVIVE] Redeploy finished with code {res.returncode}")
            except Exception as e:
                log(f"[AUTO-REVIVE] Redeploy failed: {e}")

if __name__ == "__main__":
    log("=== Keep-Alive Daemon Started ===")
    while True:
        ping_and_revive()
        time.sleep(180)  # 3분마다 반복 체크 및 활성 유지
