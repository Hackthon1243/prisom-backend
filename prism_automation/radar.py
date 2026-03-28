import boto3

def scan_for_servers():
    print("Initializing AWS Radar...")
    ec2 = boto3.client('ec2', region_name='ap-south-1')
    
    try:
        # Ask AWS for a list of all servers
        response = ec2.describe_instances()
        
        print("\n--- Scan Complete. Results: ---")
        
        # This loops through the complicated AWS data to pull out just the IDs and Status
        found_any = False
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                found_any = True
                instance_id = instance['InstanceId']
                status = instance['State']['Name']
                print(f"Server ID: {instance_id} | Current Status: {status}")
                
        if not found_any:
            print("No servers found! Person 1 might not have created them yet.")
            
    except Exception as e:
        print(f"Error scanning: {e}")

# Run the scanner
scan_for_servers()