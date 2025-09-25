import pandas as pd
import numpy as np
from elasticsearch import Elasticsearch, helpers
import requests
import time
import os
from datetime import datetime

# Elasticsearch Setup
print("🔌 Connecting to Elasticsearch...")

# Get configuration from environment variables (optional)
ES_HOST = os.getenv('ELASTICSEARCH_HOST', 'http://localhost:9200')
ES_USERNAME = os.getenv('ELASTICSEARCH_USERNAME', 'elastic')
ES_PASSWORD = os.getenv('ELASTICSEARCH_PASSWORD', 'BII3iKRTigPZX0Cm4Fiyq9YO')

# Configuration options - modify these for your setup
ELASTICSEARCH_CONFIGS = [
    # Option 1: Local Elasticsearch (no auth)
    {
        "hosts": ['http://localhost:9200'],
        "verify_certs": False,
        "request_timeout": 30,
        "description": "Local Elasticsearch (no auth)"
    },
    # Option 2: Local Elasticsearch (with auth)
    {
        "hosts": ['http://localhost:9200'],
        "basic_auth": ('elastic', 'BII3iKRTigPZX0Cm4Fiyq9YO'),
        "verify_certs": False,
        "request_timeout": 30,
        "description": "Local Elasticsearch (with auth)"
    },
    # Option 3: Environment-based configuration
    {
        "hosts": [ES_HOST],
        "basic_auth": (ES_USERNAME, ES_PASSWORD) if ES_USERNAME and ES_PASSWORD else None,
        "verify_certs": ES_HOST.startswith('https://'),
        "request_timeout": 30,
        "description": f"Environment config ({ES_HOST})"
    }
]

# Filter out None basic_auth
for config in ELASTICSEARCH_CONFIGS:
    if config.get('basic_auth') == (None, None):
        config.pop('basic_auth', None)

es = None
for i, config in enumerate(ELASTICSEARCH_CONFIGS, 1):
    try:
        print(f"🔄 Attempt {i}: {config['description']}...")
        description = config.pop('description')  # Remove description from config
        es = Elasticsearch(**config)

        # Test connection
        info = es.info()
        print(f"✅ Connected to Elasticsearch {info['version']['number']} ({description})")
        break

    except Exception as e:
        print(f"❌ Failed: {str(e)[:100]}...")
        continue

if es is None:
    print("❌ All Elasticsearch connection attempts failed!")
    print("\n💡 To fix this:")
    print("1. For local Elasticsearch: Make sure it's running on localhost:9200")
    print("2. For Elasticsearch Cloud: Update the script with your actual endpoint and credentials")
    print("3. Check your network connection and firewall settings")
    exit(1)

index_name = 'finnhub_stocks'

# Create index with mappings
mapping = {
    "mappings": {
        "properties": {
            "@timestamp": {"type": "date"},
            "symbol": {"type": "keyword"},
            "open": {"type": "float"},
            "high": {"type": "float"},
            "low": {"type": "float"},
            "close": {"type": "float"},
            "volume": {"type": "long"},
            "price_change": {"type": "float"},
            "volume_change": {"type": "float"},
            "hour": {"type": "keyword"},
            "month": {"type": "integer"},
            "season": {"type": "keyword"},
            "sentiment": {"type": "keyword"},
            "price_per_volume": {"type": "float"},
            "trip_date": {"type": "keyword"}
        }
    }
}

try:
    if es.indices.exists(index=index_name):
        print(f"📋 Index '{index_name}' already exists")
    else:
        es.indices.create(index=index_name, body=mapping)
        print(f"✅ Created index '{index_name}'")
except Exception as e:
    print(f"⚠️  Index creation warning: {e}")
    print("Continuing with existing index...")

# Finnhub API Key
API_KEY = 'd3arja1r01qrtc0dhbegd3arja1r01qrtc0dhbf0'  # Replace with your key
symbols = ['AAPL', 'TSLA', 'MSFT', 'GOOGL', 'AMZN']  # Top trending stocks; expand as needed

# Fetch real-time/historical data (last 6 months for demo)
df_list = []
for symbol in symbols:
    print(f"Fetching data for {symbol}...")
    try:
        # Historical candles (daily)
        url = f'https://finnhub.io/api/v1/stock/candle?symbol={symbol}&resolution=D&from=1714521600&to={int(time.time())}&token={API_KEY}'
        response = requests.get(url)
        data = response.json()

        if data.get('s') == 'ok' and data.get('t'):
            temp_df = pd.DataFrame({
                'symbol': symbol,
                '@timestamp': pd.to_datetime(data['t'], unit='s'),
                'open': data['o'],
                'high': data['h'],
                'low': data['l'],
                'close': data['c'],
                'volume': data['v']
            })
            temp_df['price_change'] = temp_df['close'] - temp_df['open']
            temp_df['volume_change'] = temp_df['volume'].pct_change()
            temp_df['hour'] = temp_df['@timestamp'].dt.hour.astype(str)
            temp_df['month'] = temp_df['@timestamp'].dt.month
            temp_df['trip_date'] = temp_df['@timestamp'].dt.date
            temp_df['price_per_volume'] = temp_df['close'] / temp_df['volume'].replace(0, np.nan)
            temp_df['sentiment'] = 'Neutral'  # Default sentiment
            df_list.append(temp_df)
            print(f"✅ Fetched {len(temp_df)} records for {symbol}")
        else:
            print(f"❌ No data available for {symbol}: {data.get('s', 'unknown error')}")
    except Exception as e:
        print(f"❌ Error fetching data for {symbol}: {e}")

    time.sleep(1)  # Rate limit

# Check if we have any data before proceeding
if not df_list:
    print("❌ No stock data fetched. Creating sample data for testing...")
    # Create sample data for testing
    sample_data = []
    for symbol in symbols:
        for i in range(30):  # 30 days of sample data
            date = datetime.now() - pd.Timedelta(days=i)
            sample_data.append({
                'symbol': symbol,
                '@timestamp': date,
                'open': np.random.uniform(100, 200),
                'high': np.random.uniform(200, 250),
                'low': np.random.uniform(50, 100),
                'close': np.random.uniform(100, 200),
                'volume': np.random.randint(1000000, 10000000),
                'price_change': np.random.uniform(-10, 10),
                'volume_change': np.random.uniform(-0.5, 0.5),
                'hour': str(np.random.randint(0, 24)),
                'month': date.month,
                'trip_date': date.date(),
                'price_per_volume': np.random.uniform(0.00001, 0.0001),
                'sentiment': np.random.choice(['Positive', 'Negative', 'Neutral'])
            })
    df = pd.DataFrame(sample_data)
else:
    df = pd.concat(df_list, ignore_index=True)

print(f"Loaded {len(df)} rows from Finnhub.")

def get_season(month):
    if month in [12, 1, 2]: return 'Winter'
    elif month in [3, 4, 5]: return 'Spring'
    elif month in [6, 7, 8]: return 'Summer'
    elif month in [9, 10, 11]: return 'Fall'
    return 'Unknown'

df['season'] = df['month'].apply(get_season)
df = df.dropna(subset=['@timestamp', 'symbol', 'close', 'volume'])

print(f"Sample data after processing:")
print(df[['@timestamp', 'symbol', 'close', 'volume', 'season', 'hour', 'sentiment']].head())

# Index to Elasticsearch
def generate_actions(df):
    for _, row in df.iterrows():
        try:
            doc = {
                "_index": index_name,
                "_source": {
                    "@timestamp": row['@timestamp'].isoformat() if pd.notna(row['@timestamp']) else None,
                    "symbol": str(row['symbol']),
                    "close": float(row['close']) if pd.notna(row['close']) else None,
                    "volume": int(row['volume']) if pd.notna(row['volume']) else None,
                    "hour": str(row['hour']) if pd.notna(row['hour']) else "0",
                    "month": int(row['month']) if pd.notna(row['month']) else None,
                    "season": str(row['season']) if pd.notna(row['season']) else "Unknown",
                    "sentiment": str(row['sentiment']) if pd.notna(row['sentiment']) else "Neutral"
                }
            }

            # Add optional fields if they exist and are not NaN
            if 'open' in row and pd.notna(row['open']):
                doc["_source"]["open"] = float(row['open'])
            if 'high' in row and pd.notna(row['high']):
                doc["_source"]["high"] = float(row['high'])
            if 'low' in row and pd.notna(row['low']):
                doc["_source"]["low"] = float(row['low'])
            if 'price_change' in row and pd.notna(row['price_change']):
                doc["_source"]["price_change"] = float(row['price_change'])
            if 'volume_change' in row and pd.notna(row['volume_change']):
                doc["_source"]["volume_change"] = float(row['volume_change'])
            if 'price_per_volume' in row and pd.notna(row['price_per_volume']):
                doc["_source"]["price_per_volume"] = float(row['price_per_volume'])
            if 'trip_date' in row and pd.notna(row['trip_date']):
                doc["_source"]["trip_date"] = str(row['trip_date'])

            yield doc
        except Exception as e:
            print(f"Error processing row: {e}")
            continue

try:
    print("🔄 Indexing data to Elasticsearch...")
    success_count, failed_items = helpers.bulk(es, generate_actions(df), stats_only=False)
    print(f"✅ Successfully indexed {success_count} documents to Elasticsearch.")
    if failed_items:
        print(f"⚠️  Failed to index {len(failed_items)} documents")
except Exception as e:
    print(f"❌ Elasticsearch indexing error: {e}")
    print("Creating sample data and retrying...")

    # Fallback: create minimal sample data
    sample_df = pd.DataFrame({
        '@timestamp': [datetime.now()],
        'symbol': ['AAPL'],
        'close': [150.0],
        'volume': [1000000],
        'hour': ['14'],
        'month': [datetime.now().month],
        'season': ['Fall'],
        'sentiment': ['Neutral']
    })

    try:
        helpers.bulk(es, generate_actions(sample_df))
        print(f"✅ Indexed {len(sample_df)} sample documents to Elasticsearch.")
    except Exception as e2:
        print(f"❌ Failed to index even sample data: {e2}")

print("\n📊 Final data summary:")
print(f"Total records: {len(df)}")
print(f"Unique symbols: {df['symbol'].nunique()}")
print(f"Date range: {df['@timestamp'].min()} to {df['@timestamp'].max()}")
print("\nSample data:")
print(df[['@timestamp', 'symbol', 'close', 'volume', 'season', 'hour', 'sentiment']].head())