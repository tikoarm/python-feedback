import os
import subprocess
from datetime import datetime

log_dir = "logs/checker_log"
os.makedirs(log_dir, exist_ok=True)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

tools = [
    ("isort", ["isort", "."]),
    ("flake8", ["flake8", ".", "--ignore=E501,W503"]),
    ("black", ["black", "."]),
    ("bandit", ["bandit", "-r", ".", "--exclude", "code_check.py"]),
]

for name, command in tools:
    log_path = os.path.join(log_dir, f"{name}_{timestamp}.log")
    print(f"[CHECKER] Running {name}...")
    with open(log_path, "w") as log_file:
        subprocess.run(command, stdout=log_file, stderr=log_file)

print(f"[DONE] Logs saved to {log_dir}/")
