Folder Structure if you clone.
README.md
├── scraper/
│   ├── stock_scraper.py
│   └── requirements.txt
├── airflow/
│   └── dags/
│       └── stock_pipeline.py
├── database/
│   └── schema.sql
├── config/
│   └── config.ini.example
└── docker-compose.yml


# Stock Analysis Pipeline

End-to-end solution for real-time stock data ingestion, storage, and predictive analysis using Python, MySQL, Airflow, and Tableau.

## Key Features
- Automated 15-min interval data collection via Alpha Vantage API
- MySQL database with optimized schema for financial time-series data
- Airflow-powered orchestration with Docker containers
- Tableau dashboards for real-time visualization
- ML price predictions (Random Forest/LSTM models)

## Prerequisites
- Python 3.9+
- MySQL 8.0+
- Tableau Desktop 2023+
- Docker Desktop
- [Alpha Vantage API Key](https://www.alphavantage.co/support/#api-key)

## Setup

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/Stock-Analysis-Pipeline.git
cd Stock-Analysis-Pipeline
```

### 2. Configure Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r scraper/requirements.txt
```

### 3. Configuration
Create `config/config.ini` from template:
```ini
[mysql]
host = localhost
user = root
password = your_mysql_password
database = stock_db

[alpha_vantage]
api_key = your_api_key
```

### 4. Database Setup
```sql
-- Create database
CREATE DATABASE stock_db;

-- Import schema
mysql -u root -p stock_db < database/schema.sql
```

### 5. Run Scraper
```bash
python scraper/stock_scraper.py
```

### 6. Airflow Orchestration (Docker)
```bash
docker-compose up -d
```
Access Airflow UI at `http://localhost:8080` (user: airflow, pass: airflow)

## Usage

### Real-Time Dashboard
1. Open `Tableau/StockDashboard.twb`
2. Connect to MySQL:
   - Server: localhost
   - Port: 3306
   - Database: stock_db
   - Authentication: MySQL credentials


## Contributing
1. Fork repository
2. Create feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -m 'Add feature'`)
4. Push branch (`git push origin feature/improvement`)
5. Open Pull Request
