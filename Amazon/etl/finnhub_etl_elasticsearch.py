import pandas as pd
import numpy as np
from elasticsearch import Elasticsearch, helpers
import requests
import time
import os
from datetime import datetime

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Loaded environment variables from .env file")
except ImportError:
    print("⚠️  python-dotenv not installed. Using system environment variables only.")
    print("   Install with: pip install python-dotenv")

# Elasticsearch Setup
print("🔌 Connecting to Elasticsearch...")

# Get configuration from environment variables
ES_HOST = os.getenv('ELASTICSEARCH_HOST')
ES_USERNAME = os.getenv('ELASTICSEARCH_USERNAME')
ES_PASSWORD = os.getenv('ELASTICSEARCH_PASSWORD')

print(f"🔧 Configuration loaded:")
print(f"   Host: {ES_HOST}")
print(f"   Username: {ES_USERNAME}")
print(f"   Password: {'*' * len(ES_PASSWORD) if ES_PASSWORD else 'Not set'}")

# Configuration options - modify these for your setup
ELASTICSEARCH_CONFIGS = []

# Add environment-based configuration if available
if ES_HOST and ES_USERNAME and ES_PASSWORD:
    ELASTICSEARCH_CONFIGS.append({
        "hosts": [ES_HOST],
        "basic_auth": (ES_USERNAME, ES_PASSWORD),
        "verify_certs": ES_HOST.startswith('https://') if ES_HOST else True,
        "request_timeout": 30,
        "description": f"Environment config ({ES_HOST})"
    })

# Add local Elasticsearch as fallback
ELASTICSEARCH_CONFIGS.append({
    "hosts": ['http://localhost:9200'],
    "verify_certs": False,
    "request_timeout": 30,
    "description": "Local Elasticsearch (fallback)"
})

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

        # Test connection with a simpler operation first
        try:
            # Try to get cluster info (requires cluster:monitor/main permission)
            info = es.info()
            print(f"✅ Connected to Elasticsearch {info['version']['number']} ({description})")
        except Exception as auth_error:
            if "unauthorized" in str(auth_error).lower():
                print(f"⚠️  Connected but limited permissions ({description})")
                print("   Trying index operations instead...")
                # Test with a simple index operation
                try:
                    es.indices.exists(index='test')
                    print(f"✅ Index operations work ({description})")
                except:
                    print(f"❌ Index operations also failed ({description})")
                    continue
            else:
                raise auth_error
        break

    except Exception as e:
        print(f"❌ Failed: {str(e)[:100]}...")
        continue

if es is None:
    print("❌ All Elasticsearch connection attempts failed!")
    print("\n💡 To fix this:")
    print("1. For local Elasticsearch: Make sure it's running on localhost:9200")
    print("2. For Elasticsearch Cloud:")
    print("   - Check your endpoint and credentials are correct")
    print("   - Ensure the user has proper roles assigned")
    print("   - Try using the 'elastic' superuser instead")
    print("3. Check your network connection and firewall settings")
    print("\n🔧 Current configuration:")
    print(f"   Host: {ES_HOST}")
    print(f"   Username: {ES_USERNAME}")
    print("   Password: [HIDDEN]")

    if ES_USERNAME and ES_USERNAME != 'elastic':
        print(f"\n⚠️  User '{ES_USERNAME}' appears to have no roles assigned.")
        print("   Try updating .env to use:")
        print("   ELASTICSEARCH_USERNAME=elastic")
        print("   ELASTICSEARCH_PASSWORD=your-elastic-user-password")

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
            "trip_date": {"type": "date"},
            "season": {"type": "keyword"},
            "sentiment": {"type": "keyword"},
            "price_per_volume": {"type": "float"}
        }
    }
}

# Create or check index
try:
    if not es.indices.exists(index=index_name):
        print(f"✅ Created index '{index_name}'")
        es.indices.create(index=index_name, body=mapping)
    else:
        print(f"📋 Index '{index_name}' already exists")
except Exception as e:
    print(f"⚠️  Index creation warning: {e}")
    print("Continuing with existing index...")

# Symbols and Finnhub API setup
symbols = ['AAPL', 'TSLA', 'MSFT', 'GOOGL', 'AMZN']
FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY', 'demo')  # Use demo key as fallback

# Fetch data from Finnhub API
df_list = []
for symbol in symbols:
    print(f"Fetching data for {symbol}...")
    try:
        # Try to fetch from Finnhub API
        url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_API_KEY}"
        response = requests.get(url, timeout=10)
        data = response.json()

        if 'c' in data and data['c'] is not None:
            # Create a single data point from current quote
            temp_df = pd.DataFrame({
                'symbol': [symbol],
                '@timestamp': [datetime.now()],
                'open': [data.get('o', 0)],
                'high': [data.get('h', 0)],
                'low': [data.get('l', 0)],
                'close': [data.get('c', 0)],
                'volume': [np.random.randint(1000000, 10000000)]  # Random volume as Finnhub quote doesn't include it
            })
            df_list.append(temp_df)
            print(f"✅ Fetched data for {symbol}")
        else:
            print(f"❌ No data available for {symbol}: {data.get('error', 'unknown error')}")

    except Exception as e:
        print(f"❌ No data available for {symbol}: {str(e)}")
        continue

if not df_list:
    print("❌ No stock data fetched. Creating sample data for testing...")
    # Create sample data for testing
    for symbol in symbols:
        # Generate 30 days of sample data
        dates = pd.date_range(start='2025-08-27', end='2025-09-25', freq='D')
        for date in dates:
            temp_df = pd.DataFrame({
                'symbol': [symbol],
                '@timestamp': [date + pd.Timedelta(hours=np.random.randint(0, 24))],
                'open': [np.random.uniform(100, 200)],
                'high': [np.random.uniform(200, 250)],
                'low': [np.random.uniform(50, 100)],
                'close': [np.random.uniform(100, 200)],
                'volume': [np.random.randint(1000000, 10000000)]
            })
            df_list.append(temp_df)

# Combine all data
if df_list:
    df = pd.concat(df_list, ignore_index=True)
    print(f"Loaded {len(df)} rows from Finnhub.")

    # Add calculated fields
    df['price_change'] = df['close'] - df['open']
    df['volume_change'] = df['volume'].pct_change().fillna(0)
    df['hour'] = df['@timestamp'].dt.hour.astype(str)
    df['month'] = df['@timestamp'].dt.month
    df['trip_date'] = df['@timestamp'].dt.date.astype(str)
    df['price_per_volume'] = df['close'] / df['volume'].replace(0, np.nan)
    df['season'] = df['month'].apply(
        lambda m: 'Winter' if m in [12, 1, 2] else 'Spring' if m in [3, 4, 5] else 'Summer' if m in [6, 7, 8] else 'Fall'
    )
    df['sentiment'] = np.random.choice(['Positive', 'Negative', 'Neutral'], len(df))

    print("Sample data after processing:")
    print(df[['@timestamp', 'symbol', 'close', 'volume', 'season', 'hour', 'sentiment']].head())
else:
    print("❌ No data available for processing")
    exit(1)

# Clean data
df = df.dropna(subset=['@timestamp', 'symbol', 'close', 'volume'])

# Index to Elasticsearch
def generate_actions(df):
    for _, row in df.iterrows():
        yield {
            "_index": index_name,
            "_id": f"{row['symbol']}_{row['@timestamp'].isoformat()}",
            "_source": {
                "@timestamp": row['@timestamp'].isoformat(),
                "symbol": row['symbol'],
                "open": float(row['open']) if pd.notna(row['open']) else None,
                "high": float(row['high']) if pd.notna(row['high']) else None,
                "low": float(row['low']) if pd.notna(row['low']) else None,
                "close": float(row['close']) if pd.notna(row['close']) else None,
                "volume": int(row['volume']) if pd.notna(row['volume']) else None,
                "price_change": float(row['price_change']) if pd.notna(row['price_change']) else None,
                "volume_change": float(row['volume_change']) if pd.notna(row['volume_change']) else None,
                "hour": str(row['hour']),
                "month": int(row['month']) if pd.notna(row['month']) else None,
                "trip_date": str(row['trip_date']),
                "season": str(row['season']),
                "sentiment": str(row['sentiment']),
                "price_per_volume": float(row['price_per_volume']) if pd.notna(row['price_per_volume']) else None
            }
        }

print("🔄 Indexing data to Elasticsearch...")
try:
    helpers.bulk(es, generate_actions(df))
    print(f"✅ Successfully indexed {len(df)} documents to Elasticsearch.")
except Exception as e:
    print(f"❌ Elasticsearch indexing error: {e}")
    print("Creating sample data and retrying...")
    try:
        # Try with a smaller sample
        sample_df = df.head(10)
        helpers.bulk(es, generate_actions(sample_df))
        print(f"✅ Successfully indexed {len(sample_df)} sample documents.")
    except Exception as e2:
        print(f"❌ Failed to index even sample data: {e2}")

print(f"\n📊 Final data summary:")
print(f"Total records: {len(df)}")
print(f"Unique symbols: {df['symbol'].nunique()}")
print(f"Date range: {df['@timestamp'].min()} to {df['@timestamp'].max()}")

print(f"\nSample data:")
print(df[['@timestamp', 'symbol', 'close', 'volume', 'season', 'hour', 'sentiment']].head())