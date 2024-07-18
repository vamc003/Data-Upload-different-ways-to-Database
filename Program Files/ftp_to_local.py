import ftplib

# FTP server credentials
FTP_HOST = "ftp.example.com"
FTP_USER = "your_username"
FTP_PASS = "your_password"

# Path to the ZIP file on the FTP server and local path to save the file
REMOTE_ZIP_PATH = "/Millend.zip"
LOCAL_ZIP_PATH = "downloaded_file.zip"

def download_zip_from_ftp():
    with ftplib.FTP(FTP_HOST) as ftp:
        try:
            # Connect to the FTP server and login
            ftp.login(FTP_USER, FTP_PASS)
            print(f"Connected to FTP server: {FTP_HOST}")

            # Open the local file in binary write mode
            with open(LOCAL_ZIP_PATH, 'wb') as local_file:
                # Retrieve the remote file and write it to the local file
                ftp.retrbinary(f'RETR {REMOTE_ZIP_PATH}', local_file.write)
            print(f"Downloaded file to: {LOCAL_ZIP_PATH}")
        except ftplib.all_errors as e:
            print(f"FTP error: {e}")

# Call the function to download the ZIP file
download_zip_from_ftp()
