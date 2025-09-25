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
