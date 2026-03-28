import boto3
import time

def check_database():
    # Right now, this reads our fake text-file database. 
    # Later, we will swap this to read a real cloud database if needed!
    try:
        with open("status.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return "SAFE"

def stop_ec2_server(target_id):
    print(f"\n[DANGER] DETECTED! Pulling the plug on server: {target_id} [DANGER]")
    ec2 = boto3.client('ec2', region_name='ap-south-1')
    
    try:
        response = ec2.stop_instances(InstanceIds=[target_id])
        print("[Success] Server is shutting down.")
        
        # Reset the database back to SAFE so we don't keep killing it!
        with open("status.txt", "w") as file:
            file.write("SAFE")
            
    except Exception as e:
        print(f"[ERROR] AWS Error: {e}")

print("[BOT] Auto-Shutdown Bot is online and watching the database...")

# The Infinite Loop
while True:
    server_status = check_database()
    
    if server_status != "SAFE":
        # If the file says ANYTHING other than SAFE, treat it as a server ID and kill it!
        stop_ec2_server(server_status)
    else:
        # The end="\r" trick makes it overwrite the same line instead of spamming the terminal
        print("Status: SAFE. Checking again in 5 seconds...", end="\r")
        
    time.sleep(5)
