from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

with DAG(
    dag_id='my_dag_of_the_morning',
    description='My DAG to know what to do in the morning',
    tags=['tutorial', 'datascientest'],
    schedule_interval=None,
    default_args={
        'owner': 'airflow',
        'start_date': days_ago(2),
    }
) as my_dag:

    def print_text(text):
        print(text)

    texts = [
        'Pulling on trousers',
        'Pull on right sock',
        'Pull on right shoe',
        'Pull on left sock',
        'Put on left shoe',
        'Take out'
    ]

    ids = [
        'trousers',
        'right_sock',
        'right_shoe',
        'sock_left',
        'left_shoe',
        'exit'
    ]

    tasks = []
    for t, i in zip(texts, ids):
        task = PythonOperator(
            task_id=i,
            python_callable=print_text,
            op_kwargs={'text': t}
        )
        tasks.append(task)

    # tasks[0] >> tasks[1]
    # tasks[0] >> tasks[3]
    # tasks[1] >> tasks[2]
    # tasks[3] >> tasks[4]
    # tasks[2] >> tasks[5]
    # tasks[4] >> tasks[5]
    ## or: 
    tasks[0] >> [tasks[1], tasks[3]]
    tasks[1] >> tasks[2]
    tasks[3] >> tasks[4]
    [tasks[2], tasks[4]] >> tasks[5]