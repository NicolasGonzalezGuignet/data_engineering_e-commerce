from airflow import DAG
from airflow.providers.mysql.operators.mysql import MySqlOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
}

dag = DAG(
    'load_incremental_data',
    default_args=default_args,
    schedule_interval='@once',
)


load_new_data_staging = MySqlOperator(
    task_id='load_new_data_to_staging',
    mysql_conn_id='mysql_default',
    sql="""
    insert into staging.orders (order_id, product_id, customer_id, order_date, order_total)
    select *
    from sales.orders
    where order_id>(select max(order_id) from datawarehouse.fact_orders);
    """,
    dag=dag,
)

load_new_data_warehouse = MySqlOperator(
    task_id='load_new_data_to_warehouse',
    mysql_conn_id='mysql_default',
    sql="""
    insert into datawarehouse.fact_orders (order_id, product_id, customer_id, date_id, order_total)
    select o.order_id,o.product_id,o.customer_id,d.date_id,o.order_total
    from staging.orders o
    INNER JOIN datawarehouse.dim_date d ON o.order_date = d.date
    where o.order_id>(select max(order_id) from datawarehouse.fact_orders);
    """,
    dag=dag,
)

load_new_data_staging >> load_new_data_warehouse
