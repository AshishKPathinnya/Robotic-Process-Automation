# zoomlog.py

# Import the necessary variables from email_1.py
from email_1 import meeting_date, meeting_time

import requests
from datetime import datetime, timedelta, timezone

# Replace with your client ID
client_id = "Your_client_ID"

# Replace with your account ID
account_id = "your_account_ID"

# Replace with your client secret
client_secret = "your_client_secret"

auth_token_url = "https://zoom.us/oauth/token"
api_base_url = "https://api.zoom.us/v2"

# Create the Zoom link function
def create_meeting(topic, duration, start_date, start_time):
    data = {
        "grant_type": "account_credentials",
        "account_id": account_id,
        "client_secret": client_secret
    }
    response = requests.post(auth_token_url, auth=(client_id, client_secret), data=data)

    if response.status_code != 200:
        print("Unable to get access token")
        return

    response_data = response.json()
    access_token = response_data["access_token"]

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Convert the meeting date and time to UTC format
    meeting_datetime_str = f"{start_date} {start_time}"
    local_timezone = datetime.strptime(meeting_datetime_str, "%Y-%m-%d %I:%M %p").replace(tzinfo=timezone.utc)
    utc_timezone = local_timezone - timedelta(hours=local_timezone.utcoffset().total_seconds() / 3600)
    utc_start_time = utc_timezone.strftime("%Y-%m-%dT%H:%M:%S")

    payload = {
        "topic": topic,
        "duration": duration,
        "start_time": utc_start_time,  # Use the converted UTC start time
        "type": 2
    }

    resp = requests.post(f"{api_base_url}/users/me/meetings", headers=headers, json=payload)

    if resp.status_code != 201:
        print("Unable to generate meeting link")
        return

    response_data = resp.json()

    content = {
        "meeting_url": response_data["join_url"],
        "password": response_data["password"],
        "meetingTime": response_data["start_time"],
        "purpose": response_data["topic"],
        "duration": response_data["duration"],
        "message": "Success",
        "status": 1
    }

    # Write the meeting URL to urlsend.py
    with open('urlsend.py', 'w') as urlsend_file:
        urlsend_file.write(f'meeting_url = "{content["meeting_url"]}"\n')

    print(content)

# Call the create_meeting function with the desired parameters
meeting_topic = "Important Meeting"
meeting_duration = 60  # Duration of the meeting in minutes (e.g., 60 minutes)

# Use the imported meeting_date and meeting_time variables here
meeting_start_date = meeting_date
meeting_start_time = meeting_time

create_meeting(meeting_topic, meeting_duration, meeting_start_date, meeting_start_time)
