import io
import os

from googleapiclient import discovery  # focuses on connecting to Google APIs
from httplib2 import Http  # provides an HTTP client for the app to use
from oauth2client import file, client, tools  # helps us manage OAuth2 credentials
import pandas as pd  # to make and manage as a dataframe

pd.set_option('display.max_columns', None)
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

# Application SCOPES are the permissions an app will ask of the user running it. To keep user data secure,
# apps can't run without being granted permission A best practice is to use the most restrictive permissions your app
# needs to function. Why? Isn't it annoying when an app asks for a large set of permissions when you install or run
# it? Guess what? You're on the other side of the coin now, asking your users for all these permissions. Using more
# restrictive scopes make users feel better about installing your app because you're asking for less access. Most all
# scopes look like long URLs, and the Drive metadata scope is no exception.
SCOPES = 'https://www.googleapis.com/auth/drive.readonly'

# A token is required for apps to communicate with Google servers. Valid tokens coming back from Google will be saved
# in the token storage file, storage.json. If you don't save these tokens, you'll have to re-authorize your app each
# time you run it.
store = file.Storage('storage.json')

# This app first checks whether we have valid credentials already in storage (see the if statement conditional).
creds = store.get()
if not creds or creds.invalid:
    # If you have no or expired credentials, a new authorization flow must be built [via
    # oauth2client.client.flow_from_clientsecrets()] from your OAuth client ID & secret in credentials.json file that
    # you downloaded].
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)

    # Once your app has a flow, it needs to execute in order to present the OAuth2 permissions screen to the user [
    # via oauth2client.tools.run_flow()] described and illustrated above.
    creds = tools.run_flow(flow, store)

# By clicking Allow, users consent to your app accessing their Google Drive file metadata, and Google servers return
# tokens to access the API. They're returned as creds and cached in the storage.json file. At this point,
# your app now has valid credentials to make API calls. Calling googleapiclient.discovery.build() creates a service
# endpoint to the API you're using. To use build(), pass in the API name ('drive') & version desired (currently
# 'v3'). The final parameter is an HTTP client to use for encrypted API calls.
DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http()))


#
# folder_id = "13JtdoGqVp_cn-I3RtuAJ0crVcbKssyFp"
# query = f"parents = '{folder_id}'"
# # The next line of code calls the list() method in the files() collection for the Drive API to build the request,
# # which is immediately called with execute(). A Python dict is returned from which we ask for the 'files' key to get
# # the 100 file & folder names from the user's Google Drive (or less if you have fewer files). Why 100? That's the
# # default from DRIVE.files().list(). If you want to change this number, say to only 10 files or 1000,
# # add the pageSize parameter to your request: DRIVE.files().list(pageSize=10). The final part of the script loops
# # through each file and adds it to a list (so rows is a list of dictionaries)
# files = DRIVE.files().list(pageSize=1000, q=query).execute().get('files', [])
# rows = []
# for f in files:
#     rows.append(f)
#
# # We then take the list of dictionaries and convert them to a pandas dataframe
# df = pd.DataFrame(rows)
# print(df.head(10))
# print(df["mimeType"].unique())
# print(df[df['mimeType'] == "application/vnd.google-apps.folder"])

def view_files(folder_id=""):
    if folder_id != "":
        query = f"parents = '{folder_id}'"
        # query = f"'{folder_id}' in parents"
        files = DRIVE.files().list(pageSize=1000, q=query).execute().get('files', [])
        rows = []
        for f in files:
            rows.append(f)
        df = pd.DataFrame(rows)
        # print(df.head(10))
        # print(df["mimeType"].unique())
        return df
    else:
        files = DRIVE.files().list(pageSize=1000, q=None).execute().get('files', [])
        rows = []
        for f in files:
            rows.append(f)
        df = pd.DataFrame(rows)
        # print(df.head(10))
        # print(df["mimeType"].unique())
        return df


def download_file(real_file_id, file_type, file_name, path):
    try:
        # create drive api client
        service = build("drive", "v3", credentials=creds)

        file_id = real_file_id
        if file_type == 'application/vnd.google-apps.folder':
            os.mkdir(os.path.join(path, file_name))
            download_all_files_in_this_folder(real_file_id, os.path.join(path, file_name))
        elif file_type.startswith("application/vnd.google-apps"):
            request = service.files().export_media(fileId=file_id, mimeType="application/pdf")
            file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(f"Download {int(status.progress() * 100)}.")

            with open(os.path.join(path, file_name + ".pdf"), 'wb') as f:
                f.write(file.getvalue())

            f.close()
        else:
            request = service.files().get_media(fileId=file_id)
            file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(f"Download {int(status.progress() * 100)}.")

            with open(os.path.join(path, file_name), 'wb') as f:
                f.write(file.getvalue())

            f.close()

    except HttpError as error:
        print(f"An error occurred for {file_id}: {error}")


def download_all_files_in_this_folder(folder_id, path):
    df = view_files(folder_id)
    df.apply(lambda row: download_file(row['id'], row['mimeType'], row['name'], path), axis=1)


download_all_files_in_this_folder("12e1Ll_AOK_RyfgjVy8DiS7ckHrvOxrRa", "/Volumes/WD/HDD backup/")

