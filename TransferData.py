"""
Tranfers PM data dated 1 day ago from data collection server to this local machine
"""
import datetime
from pathlib import Path
import paramiko

HOST_NAME = '199.109.33.81'
USERNAME = 'ymm26'
SOURCE_DIR = Path('/home/ymm26/adva-performance-monitoring/output')

print(f"Data Transfer triggered at {datetime.datetime.utcnow()}")
script_dir: Path = Path(__file__).resolve().parent
file_to_transfer = Path(str(datetime.date.today() -
                            datetime.timedelta(days=1)) + '.json')
source_path: Path = SOURCE_DIR / file_to_transfer
destination_path: Path = script_dir / Path("collectedData") / file_to_transfer
private_key: Path = script_dir / Path("keys/nysernetTestbed")

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# ssh.connect('remote-server.example.com', username='myusername', password='mypassword')
ssh.connect(HOST_NAME, username=USERNAME, pkey=str(private_key))

sftp = ssh.open_sftp()
sftp.get(str(source_path), str(destination_path))
sftp.close()
ssh.close()
print("Data Transfered\n")
