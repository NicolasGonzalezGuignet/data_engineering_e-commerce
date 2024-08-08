from airflow import DAG
from airflow.providers.mysql.operators.mysql import MySqlOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
}

dag = DAG(
    'create_database_and_table_and_load_dag',
    default_args=default_args,
    schedule_interval='@once',
)

# Tarea para crear la base de datos
create_database = MySqlOperator(
    task_id='create_database',
    mysql_conn_id='mysql_default',
    sql="""
        CREATE DATABASE IF NOT EXISTS sales;
    """,
    dag=dag,
)

# Tarea para crear la tabla dentro de la base de datos recién creada
create_table_customers = MySqlOperator(
    task_id='create_table1',
    mysql_conn_id='mysql_default',
    sql="""
        USE sales;
        CREATE TABLE IF NOT EXISTS customers(
        customer_id INTEGER PRIMARY KEY,
        first_name VARCHAR(255),
        last_name VARCHAR(255),
        email VARCHAR(255),
        country VARCHAR(255),
        registration_date DATE
        );
    """,
    dag=dag,
)


create_table_orders = MySqlOperator(
    task_id='create_table2',
    mysql_conn_id='mysql_default',
    sql="""
        USE sales;
        CREATE TABLE IF NOT EXISTS orders(
        order_id INT PRIMARY KEY,
        product_id VARCHAR(255),
        customer_id INT,
        order_date DATE,
        order_total FLOAT,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        );
    """,
    dag=dag,
)



load_data_orders = MySqlOperator(
    task_id='load_data2',
    mysql_conn_id='mysql_default',
    sql="""
        LOAD DATA INFILE "/data/orders.csv"
        INTO TABLE sales.orders         
        FIELDS TERMINATED BY ','
        IGNORE 1 LINES;
    """,
    dag=dag,
)

load_data_customers = MySqlOperator(
    task_id='load_data1',
    mysql_conn_id='mysql_default',
    sql="""
        LOAD DATA INFILE "/data/customers.csv"
        INTO TABLE sales.customers         
        FIELDS TERMINATED BY ','
        IGNORE 1 LINES;
    """,
    dag=dag,
)

export_data_customers = MySqlOperator(
    task_id='export_data1',
    mysql_conn_id='mysql_default',
    sql="""
        SELECT * FROM sales.customers
        INTO OUTFILE '/data/exported_customers.csv'
        FIELDS TERMINATED BY ',' 
        LINES TERMINATED BY '\n';
    """,
    dag=dag,
)


export_data_orders = MySqlOperator(
    task_id='export_data2',
    mysql_conn_id='mysql_default',
    sql="""
        SELECT * FROM sales.orders
        INTO OUTFILE '/data/exported_orders.csv'
        FIELDS TERMINATED BY ',' 
        LINES TERMINATED BY '\n';
    """,
    dag=dag,
)


create_database >> create_table_customers >> create_table_orders


create_table_customers >> load_data_customers
create_table_orders >> load_data_orders

load_data_customers >> export_data_customers
load_data_orders >> export_data_orders
