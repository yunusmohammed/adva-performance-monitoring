"""
DownloadPMDataFromCloud.py - downloads collected PM data from the previous two days from the cloud, currently Google Drive
"""

from datetime import datetime, timedelta, date
from pathlib import Path
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials

script_dir = Path(__file__).resolve().parent
key_file = script_dir / Path("client_secrets.json")
creds = ServiceAccountCredentials.from_json_keyfile_name(
    str(key_file), scopes=['https://www.googleapis.com/auth/drive'])

# Authenticate with the Google Drive API
gauth = GoogleAuth()
gauth.credentials = creds
drive = GoogleDrive(gauth)

print(f"Downloading files from GDrive at {datetime.now()}")

for days in range(1, 3):
    file_name = Path(str(date.today() - timedelta(days=days)) + '.json')
    file_path = Path(Path.home().root or Path.home().drive) / \
        'data' / 'ymm26' / 'adva-performance-monitoring' / file_name

    print(f"Downloading {file_name} at {datetime.now()}")
    file_list = drive.ListFile(
        {'q': 'title = "' + str(file_name) + '"'}).GetList()
    if len(file_list) == 0:
        print(f"File {file_name} not found in Google Drive")
    else:
        file_drive = file_list[0]
        file_drive.GetContentFile(file_path)
        print('Successfully downloaded file %s with ID %s' %
              (file_drive['title'], file_drive['id']))
