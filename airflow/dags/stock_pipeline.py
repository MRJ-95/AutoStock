from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.providers.mysql.operators.mysql import MySqlOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

def scrape_and_store():
    from scraper.stock_scraper import main as scraper_main
    scraper_main()

def run_predictions():
    from analysis.prediction import main as prediction_main
    prediction_main()

dag = DAG(
    'stock_analysis_pipeline',
    default_args=default_args,
    description='End-to-end stock analysis pipeline',
    schedule_interval='0 20 * * 1-5',  # 8PM UTC = 4PM EST (after market close)
    catchup=False,
)

create_tables = MySqlOperator(
    task_id='create_tables',
    mysql_conn_id='stock_db',
    sql='database/stock_schema.sql',
    dag=dag,
)

scrape_task = PythonOperator(
    task_id='scrape_and_store_data',
    python_callable=scrape_and_store,
    dag=dag,
)

prediction_task = PythonOperator(
    task_id='run_predictions',
    python_callable=run_predictions,
    dag=dag,
)

data_quality_check = MySqlOperator(
    task_id='data_quality_check',
    mysql_conn_id='stock_db',
    sql="SELECT COUNT(*) FROM stock_data WHERE date = CURDATE()",
    dag=dag,
)

# Set up dependencies
create_tables >> scrape_task >> data_quality_check >> prediction_task