import urllib.request
import subprocess
import os
import time
import datetime
import ssl

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
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    needs_redeploy = False
    try:
        req = urllib.request.Request(
            TARGET_URL,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) KeepAliveDaemon/1.0 (nanhoony@gmail.com)"}
        )
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            if resp.status == 200:
                log(f"[KEEP-ALIVE] {TARGET_URL} is healthy (200 OK)")
            else:
                log(f"[WARNING] {TARGET_URL} status: {resp.status}")
                needs_redeploy = True
    except Exception as e:
        log(f"[ERROR] Connection check failed for {TARGET_URL}: {e}")
        needs_redeploy = True

    if needs_redeploy:
        log("[AUTO-REVIVE] Triggering automatic redeploy to Surge.sh under nanhoony@gmail.com...")
        try:
            env = os.environ.copy()
            env["SURGE_LOGIN"] = "nanhoony@gmail.com"
            env["SURGE_TOKEN"] = "1d003a62c2fa3a7481755eb621809050"
            cmd = "cmd /c npx surge . volunteer-hub-recruitment-2025.surge.sh"
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True, errors="ignore", cwd=DEPLOY_DIR, env=env)
            log(f"[AUTO-REVIVE] Redeploy finished with code {res.returncode}")
        except Exception as e:
            log(f"[AUTO-REVIVE] Redeploy failed: {e}")

if __name__ == "__main__":
    log("=== Keep-Alive Daemon Started (volunteer-hub-recruitment-2025.surge.sh - nanhoony@gmail.com) ===")
    while True:
        ping_and_revive()
        time.sleep(120)  # 2분마다 정기 점검 및 CDN 웜업 유지
