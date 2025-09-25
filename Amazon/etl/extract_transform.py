import pandas as pd
import numpy as np
import os
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# Get database credentials from environment variables
db_host = os.getenv('DB_HOST', 'postgres')
db_user = os.getenv('DB_USER', 'sravya')
db_password = os.getenv('DB_PASSWORD', 'Swami@123')
db_name = os.getenv('DB_NAME', 'mydb')
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

# Load: Push to PostgreSQL
print(f"Connecting to PostgreSQL at {db_host}:{db_port}")
engine = create_engine(f'postgresql://{db_user}:{encoded_password}@{db_host}:{db_port}/{db_name}')

try:
    df.to_sql('raw_products', engine, if_exists='replace', index=False)
    agg_df.to_sql('discount_analysis', engine, if_exists='replace', index=False)
    print("Data loaded to PostgreSQL successfully.")
except Exception as e:
    print(f"Error loading data to PostgreSQL: {e}")
    raise