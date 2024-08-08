from airflow import DAG
from airflow.providers.mysql.operators.mysql import MySqlOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
}

dag = DAG(
    'load_new_data_to_oltp',
    default_args=default_args,
    schedule_interval='@once',
)


load_new_data = MySqlOperator(
    task_id='load_new_data_to_oltp',
    mysql_conn_id='mysql_default',
    sql="""
    insert into sales.orders
    values (10001,"P093",790,"2024-08-08",517.91),(10002,"P118",954,"2024-08-05",595.31),(10003,"P070",22,"2024-08-13",294.33),(10004,"P107",936,"2024-08-12",471.43),(10005,"P158",166,"2024-08-07",940.28);
    """,
    dag=dag,
)

load_new_data

