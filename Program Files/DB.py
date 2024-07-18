import ftplib
import zipfile
import pandas as pd
from io import BytesIO

# FTP server details
ftp_server = ""
ftp_user = ""
ftp_password = ""
zip_file_name = "millend.zip"
csv_file_name = "item_info.csv"

# Connect to the FTP server
ftp = ftplib.FTP(ftp_server)

# Login to the FTP server
ftp.login(user=ftp_user, passwd=ftp_password)

print('Server login successfully')

# Download the zip file from the FTP server
with BytesIO() as f:
    ftp.retrbinary(f"RETR {zip_file_name}", f.write)
    f.seek(0)
    with zipfile.ZipFile(f) as z:
        # Check if the specified CSV file exists in the zip
        if csv_file_name in z.namelist():
            with z.open(csv_file_name) as file:
                df = pd.read_csv(file)
                #print(df.head())  # Print the first few rows to inspect the columns
                #columns = df.columns.tolist()
                #print(columns)
                print(df.head())
        else:
            print(f"{csv_file_name} not found in the zip archive")

# Close the FTP connection
ftp.quit()
