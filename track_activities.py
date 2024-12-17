import os
import requests
from datetime import datetime, timedelta
import json

def fetch_github_activities(username, token):
    """Fetch recent GitHub activities for a user."""
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    url = f'https://api.github.com/users/{username}/events'
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching GitHub activities: {e}")
        return []

def log_activities(activities):
    """Log activities to a markdown file."""
    today = datetime.now().strftime('%Y-%m-%d')
    log_file = f'activity_logs/{today}_activities.md'
    
    # Ensure logs directory exists
    os.makedirs('activity_logs', exist_ok=True)
    
    with open(log_file, 'w') as f:
        f.write(f"# Daily Activity Log - {today}\n\n")
        
        if not activities:
            f.write("No activities found today.\n")
            return
        
        for activity in activities:
            event_type = activity.get('type', 'Unknown')
            repo = activity.get('repo', {}).get('name', 'Unknown Repo')
            timestamp = activity.get('created_at', 'Unknown Time')
            
            f.write(f"## {event_type} in {repo}\n")
            f.write(f"- **Time:** {timestamp}\n")
            f.write(f"- **Details:** {json.dumps(activity, indent=2)}\n\n")

def main():
    # Get GitHub username and token from environment variables
    username = os.environ.get('USERNAME')
    token = os.environ.get('GITHUB_TOKEN')
    
    if not username or not token:
        print("GitHub username or token not set!")
        return
    
    # Fetch activities
    activities = fetch_github_activities(username, token)
    
    # Log activities
    log_activities(activities)

if __name__ == '__main__':
    main()
