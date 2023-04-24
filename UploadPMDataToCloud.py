"""
UploadPMDataToCloud.py - uploads collected PM data from the previous day to the cloud, currently Google Drive
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


file_name = Path(str(date.today() - timedelta(days=1)) + '.json')
print(f"Uploading {file_name} to GCloud at {datetime.utcnow()}")
file_path = script_dir / 'output' / file_name
file_drive = drive.CreateFile({'title': str(file_name)})
file_drive.Upload()
file_drive.SetContentFile(str(file_path))
file_drive.Upload()
print(f"Successfully uploaded {file_name} to GCloud at {datetime.utcnow()}")
