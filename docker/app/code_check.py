import subprocess
import os
from datetime import datetime

log_dir = "logs/checker_log"
os.makedirs(log_dir, exist_ok=True)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

flake8_log = os.path.join(log_dir, f"flake8_{timestamp}.log")
black_log = os.path.join(log_dir, f"black_{timestamp}.log")
bandit_log = os.path.join(log_dir, f"bandit_{timestamp}.log")

print("[CHECKER] Running flake8...")
with open(flake8_log, "w") as f:
    subprocess.run(["flake8", ".", "--ignore=E501,W503"], stdout=f, stderr=f)

print("[CHECKER] Running black...")
with open(black_log, "w") as f:
    subprocess.run(["black", "."], stdout=f, stderr=f)

print("[CHECKER] Running Bandit...")
with open(bandit_log, "w") as f:
    subprocess.run(
        ["bandit", "-r", ".", "--exclude", "code_check.py"], stdout=f, stderr=f
    )

print(f"[DONE] Logs saved to {log_dir}/")
