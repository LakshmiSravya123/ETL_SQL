# Amazon ETL with Neon Database

This project contains a comprehensive ETL pipeline for processing **Amazon product data** and **NYC taxi trip data**, storing them in Neon Database (serverless PostgreSQL) with Grafana visualization.

## 📊 **[📈 Comprehensive Data Analysis →](DATA_ANALYSIS_README.md)**
*For detailed insights, business intelligence, and data patterns analysis*

## Prerequisites

- Docker Desktop installed and running
- Docker Compose installed

## Project Structure

```
Amazon/
├── data/
│   └── amazon.csv          # Input CSV data
├── etl/
│   └── extract_transform.py # ETL script
├── db/                     # Database initialization scripts
├── grafana/               # Grafana configuration
├── Dockerfile             # Docker image definition
├── docker-compose.yml     # Multi-container setup
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
└── README.md             # This file
```

## Quick Start

1. **Start Docker Desktop**
   ```bash
   open -a Docker  # On macOS
   ```

2. **Build and run the containers**
   ```bash
   docker-compose up --build
   ```

3. **Access services**
   - Neon Database: Serverless PostgreSQL (automatically managed)
   - Grafana: `http://localhost:3001` (Swami123/Swami@123)

4. **Run individual ETL processes**
   ```bash
   # Run Amazon product ETL
   ./run.sh etl

   # Run NYC Taxi ETL (Docker)
   ./run.sh nyc

   # Run NYC Taxi ETL (directly on host)
   ./run.sh nyc-local
   ```

## Manual Steps

### 1. Build the Docker image
```bash
docker build -t amazon-etl .
```

### 2. Neon Database Setup
The project now uses Neon Database (serverless PostgreSQL). No local PostgreSQL container is needed.
Configure your Neon connection string in the `.env` file:
```bash
NEON_DATABASE_URL=postgresql://[user]:[password]@[neon_hostname]/[dbname]?sslmode=require&channel_binding=require
```

### 3. Run ETL container
```bash
docker run --rm \
  --link amazon_postgres:postgres \
  -e DB_HOST=postgres \
  -e DB_USER=sravya \
  -e DB_PASSWORD=Swami@123 \
  -e DB_NAME=mydb \
  -v $(pwd)/data:/app/data \
  amazon-etl
```

## Environment Variables

The following environment variables can be configured:

- `NEON_DATABASE_URL`: Complete Neon database connection string
- `DB_HOST`: Neon database hostname
- `DB_USER`: Neon database username
- `DB_PASSWORD`: Neon database password
- `DB_NAME`: Neon database name
- `DB_PORT`: Database port (default: 5432)
- `CSV_PATH`: Path to CSV file (default: ./data/amazon.csv)

## Docker Login (Optional)

If you need to push images to Docker Hub:

```bash
docker login -u swami9876
# Enter password: Swami@123
```

## Troubleshooting

1. **Docker daemon not running**
   - Start Docker Desktop application
   - Wait for Docker to fully initialize

2. **Permission denied errors**
   - Ensure Docker Desktop has proper permissions
   - Try running with `sudo` if on Linux

3. **Port conflicts**
   - Check if ports 5432 or 3000 are already in use
   - Modify port mappings in docker-compose.yml if needed

4. **CSV file not found**
   - Ensure `amazon.csv` exists in the `data/` directory
   - Check file permissions

## Database Tables

### Amazon ETL Tables
- `raw_products`: Contains all processed Amazon product data (1,463 records)
- `discount_analysis`: Contains aggregated discount analysis (339 records)

### NYC Taxi ETL Tables
- `raw_trips`: Contains taxi trip data (1,000 sample records)
- `hourly_analysis`: Contains trip patterns by hour (24 records)
- `zonal_analysis`: Contains trip patterns by pickup zone (265+ records)

## 📊 Data Insights & Analysis

This ETL pipeline processes two distinct datasets providing valuable business insights:

### 🛍️ Amazon Product Data Analysis
- **1,463 products** across electronics and accessories categories
- **Discount Analysis**: 58% of products offer >50% discounts
- **Customer Satisfaction**: 89% of products rated 4+ stars
- **Price Range**: Most products between ₹150-₹500
- **Top Categories**: USB cables, charging accessories, networking devices

### 🚕 NYC Taxi Trip Analysis
- **1,000 trip records** with temporal and geographical patterns
- **Peak Hours**: 8-9 AM and 6-7 PM show highest demand
- **Fare Patterns**: Airport trips average 40% higher fares
- **Zone Coverage**: 265+ unique pickup locations across NYC
- **Seasonal Trends**: Spring data shows consistent demand patterns

**[📈 View Complete Data Analysis →](DATA_ANALYSIS_README.md)**

### NYC Taxi ETL Tables
- `raw_trips`: Contains processed taxi trip data
- `hourly_analysis`: Contains hourly aggregated trip statistics
- `zonal_analysis`: Contains zone-based trip analysis

## Stopping Services

```bash
docker-compose down
```

To remove volumes as well:
```bash
docker-compose down -v
```
