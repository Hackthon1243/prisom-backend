import boto3

def stop_rogue_server(server_id):
    print(f"Alert received! Attempting to stop server: {server_id}")

    # 1. We create our "remote control" for the EC2 service
    # Note: 'ap-south-1' is the code for Mumbai. Ask Person 1 which region they picked!
    ec2 = boto3.client('ec2', region_name='ap-south-1') 

    try:
        # 2. The Magic Switch! We tell AWS to stop the server.
        response = ec2.stop_instances(InstanceIds=[server_id])
        
        print("Success! Command sent to AWS.")
        print("Current Status:", response['StoppingInstances'][0]['CurrentState']['Name'])
        
    except Exception as e:
        print(f"Uh oh, something went wrong: {e}")

# This is a test command. 
# Right now, it will fail because we haven't given your laptop the AWS keys yet!
stop_rogue_server('i-0123456789abcdef0')