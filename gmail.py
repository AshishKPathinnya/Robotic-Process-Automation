# Add the missing imports
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path
import base64
import email
from bs4 import BeautifulSoup

# Define the SCOPES. If modifying it, delete the token.pickle file.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def getEmails(service):  # Pass 'service' as an argument
    # ... (existing code)

    # request a list of the first 5 messages
    result = service.users().messages().list(userId='me', maxResults=5).execute()

    # messages is a list of dictionaries where each dictionary contains a message id.
    messages = result.get('messages')

    # Variable to keep track of the number of emails processed
    num_emails_processed = 0

    # Variable to store sender's email address
    sender_email = None

    # iterate through all the messages
    for msg in messages:
        # Get the message from its id
        txt = service.users().messages().get(userId='me', id=msg['id']).execute()

        # Use try-except to avoid any Errors
        try:
            # Get value of 'payload' from dictionary 'txt'
            payload = txt['payload']
            headers = payload['headers']

            # Look for Subject and Sender Email in the headers
            for d in headers:
                if d['name'] == 'Subject':
                    subject = d['value']
                if d['name'] == 'From':
                    sender_email = d['value']

            # Get the body of the email from the payload
            body = None
            if 'parts' in payload:
                for part in payload['parts']:
                    if part['mimeType'] == 'text/plain':
                        data = part['body']['data']
                        data = data.replace("-","+").replace("_","/")
                        decoded_data = base64.b64decode(data)
                        body = decoded_data.decode('utf-8')
                        break

            # Check if the keywords "zoom" and "meeting" are present in the subject or body
            if 'zoom' in subject.lower() or 'meeting' in subject.lower() or (body and 'zoom' in body.lower() and 'meeting' in body.lower()):
                # Printing the subject, sender's email, and message
                print("Subject: ", subject)
                print("From: ", sender_email)
                print("Message: ", body)
                print('\n')

                # Extract the date and time from the email body
                meeting_date = ""
                meeting_time = ""
                if body:
                    # You may need to adjust the parsing logic based on the actual email body format
                    # For this example, let's assume the date and time are enclosed in double quotes
                    date_start = body.find('"') + 1
                    date_end = body.find('"', date_start)
                    time_start = body.find('"', date_end + 1) + 1
                    time_end = body.find('"', time_start)

                    if date_start != -1 and date_end != -1:
                        meeting_date = body[date_start:date_end]
                    if time_start != -1 and time_end != -1:
                        meeting_time = body[time_start:time_end]

                # Store the email subject, sender's email, body, date, and time in "email_1.py"
                with open('email_1.py', 'w') as email_file:
                    email_file.write(f'# Subject: {subject}\n')
                    email_file.write(f'sender_email = "{sender_email}"\n')
                    email_file.write(f'body = """{body}"""\n')
                    email_file.write(f'meeting_date = "{meeting_date}"\n')
                    email_file.write(f'meeting_time = "{meeting_time}"\n')

            # Increment the number of emails processed
            num_emails_processed += 1

            # Break the loop if 5 emails are processed
            if num_emails_processed == 5:
                break

        except Exception as e:
            print("Error processing email:", e)
            pass

# Main function to authenticate and call getEmails
def main():
    # Variable creds will store the user access token.
    # If no valid token found, we will create one.
    creds = None

    # The file token.pickle contains the user access token.
    # Check if it exists
    if os.path.exists('token.pickle'):
        # Read the token from the file and store it in the variable creds
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If credentials are not available or are invalid, ask the user to log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the access token in token.pickle file for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Connect to the Gmail API
    service = build('gmail', 'v1', credentials=creds)

    # Call getEmails and pass 'service' as an argument
    getEmails(service)

if __name__ == "__main__":
    main()

