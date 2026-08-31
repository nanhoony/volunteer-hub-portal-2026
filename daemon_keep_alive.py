import urllib.request
import subprocess
import os
import time
import datetime

TARGET_URL = "https://volunteer-hub-recruitment-2025.surge.sh"
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
    needs_redeploy = False
    try:
        req = urllib.request.Request(
            TARGET_URL,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) KeepAliveDaemon/1.0"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status == 200:
                log(f"[KEEP-ALIVE] {TARGET_URL} is healthy (200 OK)")
            else:
                log(f"[WARNING] Status code: {resp.status}")
                needs_redeploy = True
    except Exception as e:
        log(f"[ERROR] Connection check failed: {e}")
        needs_redeploy = True

    if needs_redeploy:
        log("[AUTO-REVIVE] Triggering automatic teardown & redeploy to Surge.sh...")
        try:
            cmd_teardown = 'cmd /c npx surge teardown volunteer-hub-recruitment-2025.surge.sh'
            subprocess.run(cmd_teardown, shell=True, capture_output=True, text=True, cwd=DEPLOY_DIR)

            cmd = f'cmd /c npx surge "{DEPLOY_DIR}" volunteer-hub-recruitment-2025.surge.sh'
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=DEPLOY_DIR)
            log(f"[AUTO-REVIVE] Redeploy finished with code {res.returncode}")
        except Exception as e:
            log(f"[AUTO-REVIVE] Redeploy failed: {e}")

if __name__ == "__main__":
    log("=== Keep-Alive Daemon Started ===")
    while True:
        ping_and_revive()
        time.sleep(600)  # 10분마다 반복 체크
