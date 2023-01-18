import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GmailClient:

    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

    def __init__(self, credentialsFile="credentials.json", port=80):
        """Shows basic usage of the Gmail API.
        Lists the user's Gmail labels.
        """
        self._credentialsFile = credentialsFile
        print(f'init using credentials file: {credentialsFile}')

    def open_session_to_Gmail(self):
        print('*** Open session to Gmail')
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self._credentialsFile, self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            # Call the Gmail API
            self._service = build('gmail', 'v1', credentials=creds)
        except HttpError as error:
            print(f'An error occurred: {error}')

    def saveAttachment(self, messageId, fileName):
        # Get the message it self
        message = self._service.users().messages().get(userId='me', id=messageId['id']).execute()
        # message['snippet'] is the message it self
        print(message['snippet'])    
        for part in message['payload']['parts']:
            # Check if there is an attachment to the email 
            if part['filename']:
                # Checks if the file is part of the email itself (such as an image)
                if 'data' in part['body']:
                    data = part['body']['data']
                # If the file is not a part of the email itself, it is probably an attachment
                else:
                    att_id = part['body']['attachmentId']
                    # Fetch the attachment
                    att = self._service.users().messages().attachments().get(userId='me', messageId=message['id'],
                                                                    id=att_id).execute()
                    data = att['data']
                # Encode it
                import base64
                file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
                path = part['filename']
                path = 'SN-Data-Encrypted.txt'
                path = fileName
                # Save to a file stored locally, matching to the `path` variable with the same name of the file in the email
                with open(path, 'wb') as f:
                    f.write(file_data)
                print(f'Succesfully stored attachment {path}')

    def Download_Latest_Export(self, fileName):
        print(f"Download latest export")
        results = self._service.users().messages().list(userId='me', q='label:standardnotesbackup', maxResults=1).execute() # q='label:standardnotesbackup' labelIds='standardnotesbackup'
        messages = results.get('messages', [])
        print(messages[0])
        self.saveAttachment(messages[0], fileName)
