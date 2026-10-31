#!/usr/bin/env python3
"""
Run All Experiments — One-Command Runner
Launches all 6 AI Laboratory Experiments simultaneously on dedicated ports.
"""
import os
import sys
import time
import signal
import shutil
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Detect Virtualenv or System Python
VENV_PYTHON = os.path.join(BASE_DIR, ".venv_shared", "bin", "python")
VENV_STREAMLIT = os.path.join(BASE_DIR, ".venv_shared", "bin", "streamlit")

if os.path.exists(VENV_PYTHON):
    PYTHON = VENV_PYTHON
else:
    PYTHON = sys.executable

if os.path.exists(VENV_STREAMLIT):
    STREAMLIT_CMD = [VENV_STREAMLIT]
else:
    STREAMLIT_CMD = [PYTHON, "-m", "streamlit"]

PORTS = [5001, 5002, 5003, 5004, 8501, 5006]

APPS = [
    {
        "id": "exp1",
        "name": "Exp 1: ECommerceGPT (RAG Retail Chatbot)",
        "cwd": os.path.join(BASE_DIR, "exp_1", "GPT-main"),
        "cmd": [PYTHON, "app.py"],
        "env": {"PORT": "5001"},
        "url": "http://127.0.0.1:5001",
        "port": 5001
    },
    {
        "id": "exp2",
        "name": "Exp 2: BlogStudio Pro (AI Content Workspace)",
        "cwd": os.path.join(BASE_DIR, "exp_2", "GPT_4_Exp_2-main"),
        "cmd": [PYTHON, "app.py"],
        "env": {"PORT": "5002"},
        "url": "http://127.0.0.1:5002",
        "port": 5002
    },
    {
        "id": "exp3",
        "name": "Exp 3: MailSense AI (Customer Support Co-Pilot)",
        "cwd": os.path.join(BASE_DIR, "exp_3", "GPT_4_Exp_3-main"),
        "cmd": [PYTHON, "app.py"],
        "env": {"PORT": "5003"},
        "url": "http://127.0.0.1:5003",
        "port": 5003
    },
    {
        "id": "exp4",
        "name": "Exp 4: PathFinder AI (Learning Recommender)",
        "cwd": os.path.join(BASE_DIR, "exp_4", "GPT_4_Exp_4-main"),
        "cmd": [PYTHON, "app.py"],
        "env": {"PORT": "5004"},
        "url": "http://127.0.0.1:5004",
        "port": 5004
    },
    {
        "id": "exp5",
        "name": "Exp 5: LexiGuard AI (Contract & Risk Analyzer)",
        "cwd": os.path.join(BASE_DIR, "exp_5", "GPT_4_Exp_5-main"),
        "cmd": STREAMLIT_CMD + [
            "run", "app.py",
            "--server.port", "8501",
            "--server.headless", "true",
            "--browser.gatherUsageStats", "false"
        ],
        "env": {"HOME": "/tmp"},
        "url": "http://localhost:8501",
        "port": 8501
    },
    {
        "id": "exp6",
        "name": "Exp 6: MediAssist AI (Clinical Decision Support)",
        "cwd": os.path.join(BASE_DIR, "exp_6", "GPT_4_Exp_6-main"),
        "cmd": [PYTHON, "app.py"],
        "env": {"PORT": "5006"},
        "url": "http://127.0.0.1:5006",
        "port": 5006
    }
]

def kill_stale_ports():
    """Ensure all target ports are completely free before launching."""
    try:
        port_args = " ".join([f"-i :{p}" for p in PORTS])
        cmd = f"lsof -t {port_args} 2>/dev/null"
        pids = subprocess.check_output(cmd, shell=True).decode().strip().split()
        if pids:
            print(f"[*] Freeing stale processes on target ports: {', '.join(pids)}")
            subprocess.run(f"kill -9 {' '.join(pids)} 2>/dev/null", shell=True)
            time.sleep(1)
    except Exception:
        pass

processes = []

def cleanup(sig=None, frame=None):
    print("\n\nShutting down all experiment servers...")
    for item in processes:
        proc = item["proc"]
        name = item["name"]
        try:
            proc.terminate()
            print(f" [STOPPED] {name}")
        except Exception:
            pass
    print("All services stopped.")
    sys.exit(0)

signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

def main():
    print("=" * 75)
    print("   🤖 LAUNCHING ALL 6 AI EXPERIMENTS CONCURRENTLY")
    print("=" * 75)

    kill_stale_ports()

    for app in APPS:
        env = os.environ.copy()
        env.update(app.get("env", {}))

        log_path = os.path.join(LOG_DIR, f"{app['id']}.log")
        log_file = open(log_path, "w")

        proc = subprocess.Popen(
            app["cmd"],
            cwd=app["cwd"],
            env=env,
            stdout=log_file,
            stderr=subprocess.STDOUT
        )
        processes.append({"name": app["name"], "proc": proc, "log_file": log_file})
        print(f"  ✅ [STARTED] {app['name']}")
        print(f"               🔗 URL  : {app['url']}")
        print(f"               📝 Log  : logs/{app['id']}.log (PID {proc.pid})\n")

    print("=" * 75)
    print("  🚀 ALL 6 APPS ARE LIVE AND READY IN YOUR BROWSER!")
    print("  Press CTRL+C anytime to stop all servers.")
    print("=" * 75)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        cleanup()

if __name__ == "__main__":
    main()
