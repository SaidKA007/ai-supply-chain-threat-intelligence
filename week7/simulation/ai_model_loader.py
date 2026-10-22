import subprocess
import os

print("[AI MODEL LOADER — SECURITY LAB]")
print("Python PID:", os.getpid())
print("Starting a harmless command shell...")

subprocess.run([
    "cmd.exe",
    "/c",
    "echo WEEK7_CAR_TEST && timeout /t 120 /nobreak"
])

print("Simulation completed.")
