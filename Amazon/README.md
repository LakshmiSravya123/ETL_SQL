# Amazon ETL Docker Setup

This project contains a containerized ETL pipeline for processing Amazon product data and storing it in PostgreSQL with Grafana visualization.

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
   - PostgreSQL: `localhost:5433` (external port, avoids conflict with local PostgreSQL)
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

### 2. Run PostgreSQL container
```bash
docker run -d \
  --name amazon_postgres \
  -e POSTGRES_DB=mydb \
  -e POSTGRES_USER=sravya \
  -e POSTGRES_PASSWORD=Swami@123 \
  -p 5433:5432 \
  postgres:15
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

- `DB_HOST`: Database hostname (default: postgres)
- `DB_USER`: Database username (default: sravya)
- `DB_PASSWORD`: Database password (default: Swami@123)
- `DB_NAME`: Database name (default: mydb)
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
