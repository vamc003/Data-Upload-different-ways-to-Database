import ftplib
import zipfile
import pandas as pd
from io import BytesIO
import mysql.connector
from mysql.connector import Error

print("Program started")

# FTP server details
ftp_server = "YourServer"
ftp_user = "User"
ftp_password = "password"
zip_file_name = "millend.zip"#Zip File Name
csv_file_name = "item_info.csv"#Unzip File Name

# Connect to the FTP server
ftp = ftplib.FTP(ftp_server)
ftp.login(user=ftp_user, passwd=ftp_password)
print('Server login successfully')

# Download the zip file from the FTP server
with BytesIO() as f:
    ftp.retrbinary(f"RETR {zip_file_name}", f.write)
    f.seek(0)
    with zipfile.ZipFile(f) as z:
        if csv_file_name in z.namelist():
            with z.open(csv_file_name) as file:
                df = pd.read_csv(file)
                print(df.head())  # Print the first few rows to inspect the columns
        else:
            print(f"{csv_file_name} not found in the zip archive")
ftp.quit()

print("ftp server closed")

# Define a function to map pandas dtypes to MySQL types
def map_dtype(dtype):
    if pd.api.types.is_integer_dtype(dtype):
        return "INT"
    elif pd.api.types.is_float_dtype(dtype):
        return "DECIMAL(10, 2)"
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return "DATETIME"
    else:
        return "VARCHAR(255)"

# Generate the SQL for creating a table
table_name = "item_info"
columns = df.columns
dtypes = df.dtypes
create_table_query = f"CREATE TABLE {table_name} ("
for col, dtype in zip(columns, dtypes):
    create_table_query += f"{col} {map_dtype(dtype)}, "
create_table_query = create_table_query.rstrip(", ") + ");"

# MySQL connection details
mysql_host = "localhost"
mysql_user = "root"
mysql_password = "passwor"
mysql_database = "database"

print("mysql started here...")

try:
    # Connect to MySQL
    connection = mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password,
        database=mysql_database
    )
    if connection.is_connected():
        cursor = connection.cursor()
        # Create table
        cursor.execute(create_table_query)
        print("Table created successfully")

        # Insert data into table
        for index, row in df.iterrows():
            insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))})"
            cursor.execute(insert_query, tuple(row))

        connection.commit()
        print("Data inserted successfully")

except Error as e:
    print(f"Error: {e}")
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
