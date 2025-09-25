#!/usr/bin/env python3
"""
Elasticsearch Cloud Setup Helper
This script helps you configure and test your Elasticsearch Cloud connection.
"""

import os
import getpass
from elasticsearch import Elasticsearch

def test_elasticsearch_connection(host, username, password):
    """Test connection to Elasticsearch Cloud"""
    try:
        print(f"🔌 Testing connection to {host}...")
        es = Elasticsearch(
            [host],
            basic_auth=(username, password),
            verify_certs=True,
            request_timeout=30
        )
        
        # Test connection
        info = es.info()
        print(f"✅ Successfully connected to Elasticsearch {info['version']['number']}")
        print(f"📊 Cluster: {info['cluster_name']}")
        
        # Test index creation
        index_name = 'test_connection'
        if es.indices.exists(index=index_name):
            es.indices.delete(index=index_name)
        
        es.indices.create(index=index_name, body={
            "mappings": {
                "properties": {
                    "test_field": {"type": "text"},
                    "timestamp": {"type": "date"}
                }
            }
        })
        print(f"✅ Successfully created test index: {index_name}")
        
        # Clean up test index
        es.indices.delete(index=index_name)
        print(f"✅ Cleaned up test index")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def create_env_file(host, username, password):
    """Create .env file with Elasticsearch credentials"""
    env_content = f"""# Elasticsearch Cloud Configuration
ELASTICSEARCH_HOST={host}
ELASTICSEARCH_USERNAME={username}
ELASTICSEARCH_PASSWORD={password}

# Finnhub API Configuration (optional)
FINNHUB_API_KEY=your-finnhub-api-key-here

# Neon Database Configuration (already configured)
NEON_DATABASE_URL=postgresql://neondb_owner:npg_9hJsgiHw7GAo@ep-morning-sea-adg9dt1l-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
DB_HOST=ep-morning-sea-adg9dt1l-pooler.c-2.us-east-1.aws.neon.tech
DB_USER=neondb_owner
DB_PASSWORD=npg_9hJsgiHw7GAo
DB_NAME=neondb
DB_PORT=5432
CSV_PATH=./data/amazon.csv

# Grafana Configuration
GF_SECURITY_ADMIN_USER=swami123
GF_SECURITY_ADMIN_PASSWORD=Swami@123
GF_SECURITY_ADMIN_EMAIL=Swami123@example.com
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    print("✅ Created .env file with your credentials")

def main():
    print("🌐 Elasticsearch Cloud Setup Helper")
    print("=" * 50)
    
    # Your Elasticsearch Cloud endpoint
    host = "https://finnhubstockanalysis-bb3c0d.es.us-central1.gcp.cloud.es.io"
    print(f"📍 Endpoint: {host}")
    
    # Get credentials
    print("\n🔐 Please provide your Elasticsearch Cloud credentials:")
    username = input("Username (default: elastic): ").strip() or "elastic"
    password = getpass.getpass("Password: ")
    
    if not password:
        print("❌ Password is required!")
        return
    
    # Test connection
    print(f"\n🧪 Testing connection...")
    if test_elasticsearch_connection(host, username, password):
        print(f"\n🎉 Connection successful!")
        
        # Ask if user wants to save credentials
        save = input("\n💾 Save credentials to .env file? (y/N): ").strip().lower()
        if save in ['y', 'yes']:
            create_env_file(host, username, password)
            print("\n✅ Setup complete! You can now run:")
            print("   python etl/finnhub_etl_elasticsearch.py")
            print("   or")
            print("   ./run.sh finnhub")
        else:
            print("\n💡 To use these credentials, set environment variables:")
            print(f"   export ELASTICSEARCH_HOST='{host}'")
            print(f"   export ELASTICSEARCH_USERNAME='{username}'")
            print(f"   export ELASTICSEARCH_PASSWORD='{password}'")
    else:
        print(f"\n❌ Connection failed. Please check:")
        print("1. Your username and password are correct")
        print("2. Your Elasticsearch Cloud deployment is running")
        print("3. Your network connection is working")

if __name__ == "__main__":
    main()
