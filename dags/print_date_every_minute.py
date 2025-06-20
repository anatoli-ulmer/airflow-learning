from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
import datetime
import time

def print_date():
    print(datetime.datetime.now())

with DAG(
    dag_id='minutely_dag_without_catchup',
    description='My DAG that\'s triggered every minute',
    tags=['tutorial', 'datascientest'],
    schedule_interval='* * * * *',
    default_args={
        'owner': 'airflow',
        'start_date': days_ago(0, minute=1),
    },
    catchup=False
) as my_dag:

    my_task = PythonOperator(
        task_id='print_date_task',
        python_callable=print_date
    )
    
    

def sleep_20_seconds():
    time.sleep(20)

with DAG(
    dag_id='too_long_dag',
    description='My DAG that\'s triggered every 10 seconds',
    tags=['tutorial', 'datascientest'],
    schedule_interval=datetime.timedelta(seconds=10),
    default_args={
        'owner': 'airflow',
        'start_date': days_ago(0, minute=1),
    },
    catchup=False
) as my_dag:

    my_task = PythonOperator(
        task_id='sleep_20_seconds',
        python_callable=sleep_20_seconds
    )