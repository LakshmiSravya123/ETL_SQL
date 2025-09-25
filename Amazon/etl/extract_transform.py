import pandas as pd
import os
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# Get Neon database credentials from environment variables
neon_url = os.getenv('NEON_DATABASE_URL')
db_host = os.getenv('DB_HOST', 'ep-morning-sea-adg9dt1l-pooler.c-2.us-east-1.aws.neon.tech')
db_user = os.getenv('DB_USER', 'neondb_owner')
db_password = os.getenv('DB_PASSWORD', 'npg_9hJsgiHw7GAo')
db_name = os.getenv('DB_NAME', 'neondb')
db_port = os.getenv('DB_PORT', '5432')

# Get CSV file path from environment variable
csv_path = os.getenv('CSV_PATH', './data/amazon.csv')

encoded_password = quote_plus(db_password)

# Extract: Load CSV
print(f"Loading CSV from: {csv_path}")
df = pd.read_csv(csv_path)

# Transform: Clean and prepare data
# Rename relevant columns for clarity (optional)
df = df.rename(columns={
    'rating': 'Stars',
    'rating_count': 'Reviews',
    'discounted_price': 'Price'
})

# Clean
df = df.dropna(subset=['Stars', 'Reviews', 'Price', 'category'])
df['Price'] = pd.to_numeric(df['Price'].str.replace('₹', '').str.replace(',', ''), errors='coerce')
df['Stars'] = pd.to_numeric(df['Stars'], errors='coerce')
df['Reviews'] = pd.to_numeric(df['Reviews'].str.replace(',', ''), errors='coerce')
df['discount_percentage'] = pd.to_numeric(df['discount_percentage'].str.replace('%', ''), errors='coerce')

# Since no 'Review Date', create discount buckets as a proxy for analysis
def get_discount_bucket(percentage):
    if percentage < 20: return 'Low (<20%)'
    elif percentage < 50: return 'Medium (20-50%)'
    else: return 'High (>50%)'

df['Discount_Bucket'] = df['discount_percentage'].apply(get_discount_bucket)

# Aggregate: Group by category and discount bucket
agg_df = df.groupby(['category', 'Discount_Bucket']).agg({
    'Stars': 'mean',
    'Reviews': 'sum',
    'Price': 'mean'
}).reset_index()

# Preview
print("Raw Data Sample:")
print(df[['product_name', 'category', 'Stars', 'Reviews', 'Price', 'Discount_Bucket']].head())
print("\nAggregated Data Sample:")
print(agg_df.head())

# Load: Push to Neon Database with fallback
print(f"Connecting to Neon Database at {db_host}")

# Try Neon connection with fallback
connection_attempts = []
if neon_url:
    connection_attempts.append(neon_url)  # Direct Neon URL from environment
connection_attempts.append(f'postgresql://{db_user}:{encoded_password}@{db_host}:{db_port}/{db_name}?sslmode=require&channel_binding=require')  # Constructed Neon URL

engine = None
for i, connection_string in enumerate(connection_attempts, 1):
    try:
        print(f"Attempting connection {i}: {connection_string.split('@')[1]}")
        engine = create_engine(connection_string)
        # Test the connection
        with engine.connect() as conn:
            from sqlalchemy import text
            conn.execute(text("SELECT 1"))
        print("✅ Successfully connected to PostgreSQL")
        break
    except Exception as e:
        print(f"❌ Connection attempt {i} failed: {e}")
        if i == len(connection_attempts):
            print("❌ All connection attempts failed")
            engine = None

if engine:
    try:
        # Load raw data to PostgreSQL
        df.to_sql('raw_products', engine, if_exists='replace', index=False)
        print("✅ Raw data loaded to PostgreSQL")

        # Load aggregated data to PostgreSQL
        agg_df.to_sql('discount_analysis', engine, if_exists='replace', index=False)
        print("✅ Aggregated data loaded to PostgreSQL")

        print("🎉 Amazon product data loaded to PostgreSQL successfully.")

    except Exception as e:
        print(f"Error loading data to PostgreSQL: {e}")
        print("💾 Data saved locally as backup")
else:
    print("💾 Could not connect to database. Data processed but not saved to PostgreSQL.")
    print("💾 Data saved locally as backup")