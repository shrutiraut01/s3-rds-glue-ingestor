import boto3
import pandas as pd
from sqlalchemy import create_engine
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env variables

def download_csv_from_s3(bucket, key, local_path):
    s3 = boto3.client('s3')
    s3.download_file(bucket, key, local_path)
    print(f"✅ Downloaded {key} from S3 bucket {bucket}")

def upload_to_rds(df, table_name):
    try:
        engine = create_engine(f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}")
        df.to_sql(table_name, con=engine, if_exists='replace', index=False)
        print("✅ Data uploaded to RDS")
        return True
    except Exception as e:
        print("❌ RDS Upload Failed:", e)
        return False

def register_with_glue():
        def register_with_glue():
    print("📣 Entered register_with_glue() function")

    # Initialize Glue client
    try:
        glue = boto3.client('glue')
        print("✅ Glue client initialized")
    except Exception as e:
        print("❌ Failed to create Glue client:", e)
        return

    database_name = os.getenv("GLUE_DB", "fallback_db")
    table_name = os.getenv("TABLE_NAME", "students")
    s3_path = f"s3://{os.getenv('S3_BUCKET')}/{os.getenv('CSV_KEY')}"
    print("📍 Registering S3 path:", s3_path)

    # Create Glue database
    try:
        glue.create_database(DatabaseInput={'Name': database_name})
        print(f"✅ Glue database '{database_name}' created")
    except glue.exceptions.AlreadyExistsException:
        print(f"ℹ️ Glue database '{database_name}' already exists")
    except Exception as e:
        print("❌ Failed to create Glue database:", e)
        return
    # Create Glue table
    try:
        glue.create_table(
            DatabaseName=database_name,
            TableInput={
                'Name': table_name,
                'StorageDescriptor': {
                    'Columns': [
                        {'Name': 'id', 'Type': 'int'},
                        {'Name': 'name', 'Type': 'string'},
                        {'Name': 'email', 'Type': 'string'}
                    ],
                    'Location': s3_path,
                    'InputFormat': 'org.apache.hadoop.mapred.TextInputFormat',
                    'OutputFormat': 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat',
                    'SerdeInfo': {
                        'SerializationLibrary': 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe',
                        'Parameters': {'field.delim': ','}
                    }
                },
                'TableType': 'EXTERNAL_TABLE',
            }
        )
        print("✅ Fallback table created in AWS Glue Catalog")
    except glue.exceptions.AlreadyExistsException:
        print("ℹ️ Table already exists in AWS Glue")
    except Exception as e:
        print("❌ Failed to create Glue table:", e)
def main():
    bucket = os.getenv("S3_BUCKET")
    key = os.getenv("CSV_KEY")
    local_file = "data.csv"

    # Step 1: Download from S3
    download_csv_from_s3(bucket, key, local_file)

    # Step 2: Read CSV
    df = pd.read_csv(local_file)
    print("📄 CSV Content Preview:")
    print(df.head())

    # Step 3: Upload to RDS
    success = upload_to_rds(df, os.getenv("TABLE_NAME"))

    # Step 4: Fallback to Glue
    if not success:
    print("⚠️ Upload failed, triggering fallback to Glue...")
        register_with_glue()

if __name__ == "__main__":
    main()
