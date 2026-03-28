import boto3
import pandas as pd
import requests
from sklearn.ensemble import IsolationForest
from datetime import datetime, timedelta

# --- CONFIGURATION ---
# Fixed: Added quotes around the token string to prevent NameError
GITHUB_TOKEN = "ghp_GiV6GbGlsGP8DH5LAdoStYjLVDlLeC2WBRtH" 
REPO_OWNER = "Hackthon1243"
REPO_NAME = "prism"

def get_github_metrics():
    """Fetches real-time commit velocity and identifies top contributor."""
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/commits"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            commits = response.json()
            authors = [c['author']['login'] for c in commits if c.get('author')]
            top_author = max(set(authors), key=authors.count) if authors else "None"
            
            return {
                "Resource ID": f"GH-{REPO_NAME}",
                "Type": "Repository",
                "CPU (%)": len(commits), 
                "Cost ($/hr)": 0.00,
                "Service": "SourceControl",
                "Top_User": top_author
            }
    except Exception:
        return None
    return None

def get_aws_metrics():
    rows = [] # Fixed: Initialized at the very start
    top_user = "Scanning..."
    
    try:
        ec2 = boto3.client('ec2')
        cw = boto3.client('cloudwatch')
        instances = ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
        for res in instances['Reservations']:
            for inst in res['Instances']:
                i_id = inst['InstanceId']
                stats = cw.get_metric_statistics(
                    Namespace='AWS/EC2', MetricName='CPUUtilization',
                    Dimensions=[{'Name': 'InstanceId', 'Value': i_id}],
                    StartTime=datetime.now() - timedelta(hours=1),
                    EndTime=datetime.now(), Period=3600, Statistics=['Average']
                )
                cpu = stats['Datapoints'][0]['Average'] if stats['Datapoints'] else 0.5
                rows.append({
                    "Resource ID": i_id, "Type": "EC2", "CPU (%)": round(cpu, 2), 
                    "Cost ($/hr)": 0.04, "Service": "ComputeEngine"
                })
    except Exception:
        pass

    gh_row = get_github_metrics()
    if gh_row:
        top_user = gh_row.pop("Top_User")
        rows.append(gh_row)

    if not rows:
        rows = [{"Resource ID": "i-demo-1", "Type": "EC2", "CPU (%)": 1.2, "Cost ($/hr)": 0.04, "Service": "ComputeEngine"}]
        
    return pd.DataFrame(rows), top_user

def run_ml_engine(df):
    if df.empty or len(df) < 2:
        df['anomaly_score'] = 1 
        return df
    model = IsolationForest(contamination=0.2, random_state=42)
    df['anomaly_score'] = model.fit_predict(df[['CPU (%)', 'Cost ($/hr)']])
    return df