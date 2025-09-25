import pandas as pd
import boto3
from io import BytesIO
from sqlalchemy import create_engine
from datetime import datetime
import pyarrow.parquet as pq
from urllib.parse import quote_plus
import os
# Get database credentials from environment variables
db_host = os.getenv('DB_HOST', 'postgres')
db_user = os.getenv('DB_USER', 'sravya')
db_password = os.getenv('DB_PASSWORD', 'Swami@123')
db_name = os.getenv('DB_NAME', 'nyc_taxi')  # Use existing database
db_port = os.getenv('DB_PORT', '5432')
encoded_password = quote_plus(db_password)

# S3 Setup - Use unsigned requests for public NYC TLC data
from botocore import UNSIGNED
from botocore.config import Config

s3 = boto3.client('s3',
                  region_name='us-east-1',
                  config=Config(signature_version=UNSIGNED))
bucket = 'nyc-tlc'
prefix = 'trip data/'  # Folder in S3
# Extract: List and read recent Parquet files (smaller sample for testing)
# Use only 1-2 months to avoid large downloads
sample_months = [4, 5]  # 2024-04 and 2024-05 only
files_to_fetch = []
for month in sample_months:
    key = f'yellow_tripdata_2024-{month:02d}.parquet'
    files_to_fetch.append(f'{prefix}{key}')

df_list = []
for key in files_to_fetch:
    try:
        print(f"Fetching {key}...")
        obj = s3.get_object(Bucket=bucket, Key=key)
        parquet_file = pq.ParquetFile(BytesIO(obj['Body'].read()))
        df_chunk = parquet_file.read().to_pandas()

        # Take only a sample to reduce processing time
        if len(df_chunk) > 100000:
            df_chunk = df_chunk.sample(n=100000, random_state=42)
            print(f"Sampled 100,000 rows from {len(df_chunk)} total rows")

        df_list.append(df_chunk)
        print(f"Successfully loaded {len(df_chunk)} rows from {key}")

    except Exception as e:
        print(f"Error fetching {key}: {e}")
        print("Continuing with available data...")
        continue

if not df_list:
    print("No data could be fetched from S3. Creating sample data for testing...")
    # Create sample data for testing
    import numpy as np
    sample_data = {
        'tpep_pickup_datetime': pd.date_range('2024-04-01', periods=1000, freq='h'),
        'pickup_location_id': np.random.randint(1, 265, 1000),
        'fare_amount': np.random.uniform(5, 50, 1000),
        'trip_distance': np.random.uniform(0.5, 20, 1000)
    }
    df = pd.DataFrame(sample_data)
    print(f"Created sample dataset with {len(df)} rows")
else:
    df = pd.concat(df_list, ignore_index=True)
    print(f"Loaded {len(df)} total rows from S3.")

# Transform: Clean and enrich
df = df.dropna(subset=['tpep_pickup_datetime', 'pickup_location_id', 'fare_amount'])
df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
df['pickup_hour'] = df['tpep_pickup_datetime'].dt.hour
df['pickup_month'] = df['tpep_pickup_datetime'].dt.month
df['trip_date'] = df['tpep_pickup_datetime'].dt.date

def get_season(month):
    if month in [12, 1, 2]: return 'Winter'
    elif month in [3, 4, 5]: return 'Spring'
    elif month in [6, 7, 8]: return 'Summer'
    elif month in [9, 10, 11]: return 'Fall'
    return 'Unknown'

df['Season'] = df['pickup_month'].apply(get_season)
df['fare_amount'] = pd.to_numeric(df['fare_amount'], errors='coerce')

# Aggregates
hourly_agg = df.groupby(['pickup_month', 'pickup_hour', 'Season']).agg({
    'fare_amount': 'mean',
    'trip_distance': 'mean'
}).reset_index()
zonal_agg = df.groupby(['pickup_location_id', 'pickup_month', 'Season']).agg({
    'fare_amount': 'sum'
}).reset_index()

print("Sample raw data:")
print(df[['tpep_pickup_datetime', 'pickup_location_id', 'fare_amount', 'Season', 'pickup_hour']].head())

# Load: Push to PostgreSQL
print(f"Connecting to PostgreSQL at {db_host}:{db_port}")

# Try Docker network connection first, then fallback to localhost
connection_attempts = [
    f'postgresql://{db_user}:{encoded_password}@{db_host}:{db_port}/{db_name}',  # Docker network
    f'postgresql://{db_user}:{encoded_password}@localhost:5433/{db_name}',       # Host network with specified db
    f'postgresql://{db_user}:{encoded_password}@localhost:5433/mydb'             # Host network with default db
]

engine = None
for connection_string in connection_attempts:
    try:
        print(f"Attempting connection: {connection_string.split('@')[1]}")
        engine = create_engine(connection_string)
        # Test the connection
        engine.connect().close()
        print(f"✅ Successfully connected to PostgreSQL")
        break
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        continue

if engine is None:
    print("❌ Could not connect to PostgreSQL with any method")
    raise Exception("Database connection failed")

try:
    df.to_sql('raw_trips', engine, if_exists='replace', index=False)
    hourly_agg.to_sql('hourly_analysis', engine, if_exists='replace', index=False)
    zonal_agg.to_sql('zonal_analysis', engine, if_exists='replace', index=False)
    print("🎉 NYC Taxi data loaded to PostgreSQL successfully.")
except Exception as e:
    print(f"❌ Error loading data to PostgreSQL: {e}")
    raise

# Real-Time Scheduling (Optional: Run monthly)
# Use schedule library: import schedule; schedule.every().month.do(lambda: exec(open('nyc_taxi_etl.py').read()))