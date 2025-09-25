# Elasticsearch Configuration Guide

## 🔌 Connection Options

The Finnhub ETL script supports multiple Elasticsearch connection methods:

### 1. Local Elasticsearch (Default)
```bash
# No configuration needed - works out of the box
python etl/finnhub_etl_elasticsearch.py
```

### 2. Environment Variables
```bash
# Set environment variables for custom configuration
export ELASTICSEARCH_HOST="https://your-deployment.es.region.aws.cloud.elastic.co:9243"
export ELASTICSEARCH_USERNAME="your-username"
export ELASTICSEARCH_PASSWORD="your-password"

python etl/finnhub_etl_elasticsearch.py
```

### 3. Direct Code Modification
Edit `etl/finnhub_etl_elasticsearch.py` and uncomment/modify the cloud configuration:

```python
# Option 3: Elasticsearch Cloud (replace with your actual endpoint)
{
    "hosts": ['https://your-actual-deployment.es.region.aws.cloud.elastic.co:9243'],
    "basic_auth": ('your-username', 'your-password'),
    "verify_certs": True,
    "request_timeout": 30,
    "description": "Elasticsearch Cloud"
}
```

## 🌐 Elasticsearch Cloud Setup

### Step 1: Get Your Endpoint
1. Log into [Elastic Cloud](https://cloud.elastic.co/)
2. Go to your deployment
3. Copy the **Elasticsearch endpoint** (looks like: `https://xyz.es.region.aws.cloud.elastic.co:9243`)

### Step 2: Get Credentials
1. In your deployment, go to **Security** → **Users**
2. Use the `elastic` user or create a new user
3. Copy the username and password

### Step 3: Configure Connection
Choose one of the methods above and replace:
- `your-deployment` with your actual deployment ID
- `region` with your region (e.g., `us-east-1`)
- `your-username` with your Elasticsearch username
- `your-password` with your Elasticsearch password

## 🔧 Troubleshooting

### Connection Errors
```
Failed to resolve 'your-deployment.es.us-east-1.aws.cloud.elastic.co'
```
**Solution**: Replace placeholder URL with your actual Elasticsearch Cloud endpoint

### Authentication Errors
```
AuthenticationException: [401] security_exception
```
**Solution**: Verify your username and password are correct

### SSL/TLS Errors
```
SSLError: certificate verify failed
```
**Solution**: For testing, you can set `verify_certs: False`, but use `True` for production

### Network Errors
```
ConnectionError: Connection timeout
```
**Solution**: Check your firewall settings and network connectivity

## 📊 Verification

After successful connection, you should see:
```
✅ Connected to Elasticsearch 8.x.x (description)
✅ Successfully indexed 150 documents to Elasticsearch.
```

## 🔍 Viewing Data

### Kibana (Elasticsearch Cloud)
1. Go to your Elastic Cloud deployment
2. Click **Kibana**
3. Navigate to **Discover**
4. Select the `finnhub_stocks` index

### Direct API Query
```bash
# Count documents
curl -X GET "your-endpoint/finnhub_stocks/_count" \
  -u "username:password"

# Search documents
curl -X GET "your-endpoint/finnhub_stocks/_search?size=5" \
  -u "username:password"
```

## 🚀 Production Recommendations

1. **Use Environment Variables**: Keep credentials out of code
2. **Enable SSL**: Always use `verify_certs: True` in production
3. **Monitor Performance**: Set appropriate `request_timeout` values
4. **Index Management**: Consider index lifecycle policies for large datasets
5. **Security**: Use dedicated service accounts with minimal permissions

## 📝 Example .env File

Create a `.env` file in your project root:
```bash
# Elasticsearch Configuration
ELASTICSEARCH_HOST=https://your-deployment.es.region.aws.cloud.elastic.co:9243
ELASTICSEARCH_USERNAME=your-username
ELASTICSEARCH_PASSWORD=your-password

# Finnhub API (optional)
FINNHUB_API_KEY=your-finnhub-api-key
```

Then load it in your script:
```python
from dotenv import load_dotenv
load_dotenv()
```
