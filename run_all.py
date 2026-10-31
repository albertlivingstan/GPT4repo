#!/usr/bin/env python3
"""
Runner script to launch all 6 GPT-4 lab experiments simultaneously on separate ports.
"""
import os
import sys
import time
import signal
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

PYTHON = os.path.join(BASE_DIR, ".venv_shared", "bin", "python")
STREAMLIT = os.path.join(BASE_DIR, ".venv_shared", "bin", "streamlit")

APPS = [
    {
        "id": "exp1",
        "name": "Exp 1: ECommerceGPT (RAG Chatbot)",
        "cwd": os.path.join(BASE_DIR, "exp_1", "GPT-main"),
        "cmd": [PYTHON, "app.py"],
        "env": {"PORT": "5001"},
        "url": "http://127.0.0.1:5001",
        "port": 5001
    },
    {
        "id": "exp2",
        "name": "Exp 2: AI Blog Content Generator",
        "cwd": os.path.join(BASE_DIR, "exp_2", "GPT_4_Exp_2-main"),
        "cmd": [PYTHON, "app.py"],
        "env": {"PORT": "5002"},
        "url": "http://127.0.0.1:5002",
        "port": 5002
    },
    {
        "id": "exp3",
        "name": "Exp 3: Intelligent Email Assistant",
        "cwd": os.path.join(BASE_DIR, "exp_3", "GPT_4_Exp_3-main"),
        "cmd": [PYTHON, "app.py"],
        "env": {"PORT": "5003"},
        "url": "http://127.0.0.1:5003",
        "port": 5003
    },
    {
        "id": "exp4",
        "name": "Exp 4: Personalized Recommendation System",
        "cwd": os.path.join(BASE_DIR, "exp_4", "GPT_4_Exp_4-main"),
        "cmd": [PYTHON, "app.py"],
        "env": {"PORT": "5004"},
        "url": "http://127.0.0.1:5004",
        "port": 5004
    },
    {
        "id": "exp5",
        "name": "Exp 5: Automated Legal Document Analyzer",
        "cwd": os.path.join(BASE_DIR, "exp_5", "GPT_4_Exp_5-main"),
        "cmd": [
            STREAMLIT, "run", "app.py",
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
        "name": "Exp 6: Clinical Decision Support Assistant",
        "cwd": os.path.join(BASE_DIR, "exp_6", "GPT_4_Exp_6-main"),
        "cmd": [PYTHON, "app.py"],
        "env": {"PORT": "5006"},
        "url": "http://127.0.0.1:5006",
        "port": 5006
    }
]

processes = []

def cleanup(sig=None, frame=None):
    print("\nShutting down all experiment servers...")
    for item in processes:
        proc = item["proc"]
        name = item["name"]
        try:
            proc.terminate()
            print(f" - Stopped {name} (PID {proc.pid})")
        except Exception:
            pass
    sys.exit(0)

signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

print("=" * 70)
print("  LAUNCHING ALL 6 EXPERIMENTS ON SEPARATE PORTS")
print("=" * 70)

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
    print(f" [STARTED] {app['name']}")
    print(f"           URL : {app['url']}")
    print(f"           Log : logs/{app['id']}.log (PID {proc.pid})\n")

print("=" * 70)
print("All servers are running. Press Ctrl+C to terminate all services.")
print("=" * 70)

try:
    while True:
        time.sleep(1)
        # Check if any process terminated unexpectedly
        for item in processes:
            ret = item["proc"].poll()
            if ret is not None:
                print(f"[WARNING] {item['name']} exited with code {ret}")
except KeyboardInterrupt:
    cleanup()

