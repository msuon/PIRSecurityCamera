from __future__ import print_function
import httplib2
import os


from oauth2client import client
from oauth2client import tools
from googleapiclient.http import MediaFileUpload
from oauth2client.file import Storage

from apiclient import discovery

# Give the client ecret file path for requesting token
CLIENT_SECRET_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "client_secret.json")
# Give the scope of access for the drive
SCOPES = "https://www.googleapis.com/auth/drive.file"
# Application Name
APPLICATION_NAME = "DRIVE API FOR PI SECURITY IMAGES"

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

def get_credentials():
    home_dir = os.path.expanduser("~")
    credential_dir = os.path.join(home_dir, ".credentials")

    if not os.path.exists(credential_dir):
        os.mkdir(credential_dir)
    credential_path = os.path.join(credential_dir, "drive-python-generial.json")

    store = Storage(credential_path)
    credentials = store.get()

    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def find_file(file_name):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    drive_servce = discovery.build("drive", "v3", http=http)

    results = drive_servce.files().list(
        pageSize=10,fields="nextPageToken, files(id, name)", q="name='{}'".format(file_name)).execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
        return None
    else:
        return items[0]

def add_folder(folder_name):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    drive_service = discovery.build("drive", "v3", http=http)

    folder_meta = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    f = drive_service.files().create(body=folder_meta,
                                    fields='id').execute()
    print("Created folder {} with ID {}".format(f.get('name'), f.get('id')))
    return f.get('id')

def add_file(local_path, remote_folder="root"):
    ''' This function adds file from local_path to a "remote_folder" in the Google Drive'''
    # Initialize drive_service
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    drive_service = discovery.build("drive", "v3", http=http)
    # Create media payload
    media = MediaFileUpload(local_path, 'image/jpg', resumable=True)

    # Add metadata about parent folder to upload file to
    if remote_folder != "root":
        try:
            folder_id = find_file(remote_folder)["id"]

        except TypeError:
            print("Could not find parent folder, creating a folder")
            folder_id = add_folder(remote_folder)
        file_meta = {
            'name': os.path.basename(local_path),
            'parents': [folder_id]
        }
    else:
        file_meta = {
            'name': os.path.basename(local_path)
        }

    request = drive_service.files().create(media_body=media, body=file_meta)
    response = None

    while response == None:
       status, response = request.next_chunk()
       if status:
           print("Uploaded %d%%." % int(status.progress() * 100))
    print("Upload Complete!")


# def remove_file(local_path, remote_path):
#     # This add file from local path to remote
#     credentials = get_credentials()
#     http = credentials.authorize(httplib2.Http())
#     drive_service = discovery.build("drive", "v3", http=http)
#
#     media = MediaFileUpload(local_path, 'image/jpg', resumable=True)
#
#     request = drive_service.files().delete(fileId="")
#     response = None
#
#     while response == None:
#         status, response = request.next_chunk()
#         if status:
#             print("Uploaded %d%%." % int(status.progress() * 100))
#     print("Upload Complete!")


