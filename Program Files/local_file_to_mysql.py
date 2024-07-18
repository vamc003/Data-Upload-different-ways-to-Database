import ftplib
import zipfile
import pandas as pd
from io import BytesIO
import mysql.connector
from mysql.connector import Error

# FTP server details
ftp_server = "server.com"
ftp_user = "user"
ftp_password = "password"
zip_file_name = "millend.zip"
csv_file_name = "item_info.csv"

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

# Function to clean column names for MySQL
def clean_column_name(column_name):
    return column_name.replace(" ", "_").replace(".", "").replace("-", "_")

# Generate the SQL for creating a table
table_name = "item_info"
columns = df.columns
dtypes = df.dtypes
create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ("
for col, dtype in zip(columns, dtypes):
    clean_col = clean_column_name(col)
    create_table_query += f"`{clean_col}` {map_dtype(dtype)}, "
create_table_query = create_table_query.rstrip(", ") + ");"

print("Create Table Query:\n", create_table_query)

# MySQL connection details
mysql_host = "localhost"
mysql_user = "vamshi"
mysql_password = "password"
mysql_database = "DB"

connection = None

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

        # Handle NaN values
        df = df.where(pd.notnull(df), None)

        # Insert data into table
        insert_query_template = f"INSERT INTO {table_name} ({', '.join([f'`{clean_column_name(col)}`' for col in columns])}) VALUES ({', '.join(['%s'] * len(columns))})"
        for index, row in df.iterrows():
            cursor.execute(insert_query_template, tuple(None if pd.isna(value) else value for value in row))

        connection.commit()
        print("Data inserted successfully")

        # Fetch and print the first 10 records from the table
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 10")
        rows = cursor.fetchall()
        for row in rows:
            print(row)

except Error as e:
    print(f"Error: {e}")
finally:
    if connection is not None and connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
