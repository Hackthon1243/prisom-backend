import time

print("[BRAIN] ML Brain is starting up...")
print("[CAMERA] Analyzing camera feed (pretending for 10 seconds)...")

# Wait 10 seconds to simulate the ML model "thinking"
time.sleep(10) 

fake_server_id = "i-0123456789abcdef0"
print(f"\n[DANGER] THREAT DETECTED! Sending kill order for server: {fake_server_id}")

# This writes the danger code into your text file!
with open("status.txt", "w") as file:
    file.write(fake_server_id)

print("[Success] Kill order written to status.txt!")