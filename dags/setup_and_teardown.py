import random
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
import datetime

def successful_task():
    print('success')


def failed_task():
    raise Exception('This task did not work!')


def random_fail_task():
    random.seed()
    a = random.random() 
    print(a)
    if a < .9:
        raise Exception('This task randomly failed')

with DAG(
    dag_id='fork1_dag',
    tags=['tutorial', 'datascientest'],
    schedule_interval=datetime.timedelta(seconds=10),
    default_args={
        'owner': 'airflow',
        'start_date': days_ago(0, minute=1)
    },
    catchup=False
) as my_dag:

    task1 = PythonOperator(
        task_id='task1',
        python_callable=successful_task
    )

    task2 = PythonOperator(
        task_id='task2',
        python_callable=random_fail_task
    )

    task3 = PythonOperator(
        task_id='task3',
        python_callable=random_fail_task
    )

    task4 = PythonOperator(
        task_id='task4',
        python_callable=successful_task
    )

    task1.as_setup() >> [task2, task3]
    [task2, task3] >> task4.as_teardown()
    task1 >> task4


with DAG(
    dag_id='failing_dag',
    tags=['tutorial', 'datascientest'],
    schedule_interval=datetime.timedelta(seconds=10),
    default_args={
        'owner': 'airflow',
        'start_date': days_ago(0, minute=1)
    },
    catchup=False
) as my_dag2:

    task1 = PythonOperator(
        task_id='task1',
        python_callable=successful_task
    )

    task2 = PythonOperator(
        task_id='task2',
        python_callable=random_fail_task
    )

    task3 = PythonOperator(
        task_id='task3',
        python_callable=random_fail_task
    )

    task4 = PythonOperator(
        task_id='task4',
        python_callable=successful_task
    )

    task1.as_setup() >> [task2, task3]
    [task2, task3] >> task4.as_teardown()
    task1 >> task4
    
    
    
with DAG(
    dag_id='teardown_dag',
    tags=['tutorial', 'datascientest'],
    schedule_interval=datetime.timedelta(seconds=30),
    default_args={
        'owner': 'airflow',
        'start_date': days_ago(0, minute=1)
    },
    catchup=False
) as my_dag3:

    task1 = PythonOperator(
        task_id='task1',
        python_callable=successful_task
    )

    task2 = PythonOperator(
        task_id='task2',
        python_callable=random_fail_task
    )

    task3 = PythonOperator(
        task_id='task3',
        python_callable=random_fail_task
    )

    task4 = PythonOperator(
        task_id='task4',
        python_callable=successful_task
    )

    task1.as_setup() >> [task2, task3]
    [task2, task3] >> task4.as_teardown()
    task1 >> task4
    
    
with DAG(
    dag_id='failed_email_dag',
    tags=['tutorial', 'datascientest'],
    schedule_interval=datetime.timedelta(seconds=30),
    default_args={
        'owner': 'airflow',
        'start_date': days_ago(0, minute=1)
    },
    catchup=False
) as my_dag4:
    
    task1 = PythonOperator(
        task_id="my_failed_task",
        python_callable=failed_task,
        retries=3,
        retry_delay=datetime.timedelta(seconds=30),
        dag=my_dag,
        email_on_retry=True,
        email=['anatoli.ulmer@gmail.com']
    )
    
    task1
