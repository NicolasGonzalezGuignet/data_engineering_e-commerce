from airflow import DAG
from airflow.providers.mysql.operators.mysql import MySqlOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
}

dag = DAG(
    'create_datawarehouse',
    default_args=default_args,
    schedule_interval='@once',
)

# Tarea para crear la base de datos
create_database = MySqlOperator(
    task_id='create_database',
    mysql_conn_id='mysql_default',
    sql="""
        CREATE DATABASE IF NOT EXISTS datawarehouse;
    """,
    dag=dag,
)

# Tarea para crear la tabla dentro de la base de datos recién creada
create_table_customers = MySqlOperator(
    task_id='create_table1',
    mysql_conn_id='mysql_default',
    sql="""
        USE datawarehouse;
        CREATE TABLE IF NOT EXISTS dim_customers(
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
        USE datawarehouse;
        CREATE TABLE IF NOT EXISTS fact_orders(
        order_id INT PRIMARY KEY,
        product_id VARCHAR(255),
        customer_id INT,
        date_id INT,
        order_total FLOAT,
        FOREIGN KEY (product_id) REFERENCES dim_products(product_id),
        FOREIGN KEY (customer_id) REFERENCES dim_customers(customer_id),
        FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
        );
    """,
    dag=dag,
)


create_table_products = MySqlOperator(
    task_id='create_table3',
    mysql_conn_id='mysql_default',
    sql="""
        USE datawarehouse;
        CREATE TABLE IF NOT EXISTS dim_products(
        product_id VARCHAR(255) PRIMARY KEY,
        type VARCHAR(255),
        model VARCHAR(255)
        );
    """,
    dag=dag,
)

create_table_date = MySqlOperator(
    task_id='create_table4',
    mysql_conn_id='mysql_default',
    sql="""
        USE datawarehouse;
        CREATE TABLE IF NOT EXISTS dim_date(
        date_id INT PRIMARY KEY,
        date DATE,
        year INT,
        quarter INT,
        month INT,
        day_of_month INT,
        day_of_week INT,
        is_weekend BOOLEAN
        );
    """,
    dag=dag,
)

load_data_date = MySqlOperator(
    task_id='load_data4',
    mysql_conn_id='mysql_default',
    sql="""
        CREATE TABLE IF NOT EXISTS staging.number_sequence (
            n INT PRIMARY KEY
        );

        TRUNCATE TABLE staging.number_sequence;

        INSERT INTO staging.number_sequence (n)
        SELECT @rownum := @rownum + 1 AS n
        FROM information_schema.columns, (SELECT @rownum := 0) r
        LIMIT 3650;


        INSERT INTO datawarehouse.dim_date (date_id, date, year, quarter, month, day_of_month, day_of_week, is_weekend)
        SELECT 
            n AS date_id,
            DATE_ADD('2021-01-01', INTERVAL n - 1 DAY) AS date,
            YEAR(DATE_ADD('2021-01-01', INTERVAL n - 1 DAY)) AS year,
            QUARTER(DATE_ADD('2021-01-01', INTERVAL n - 1 DAY)) AS quarter,
            MONTH(DATE_ADD('2021-01-01', INTERVAL n - 1 DAY)) AS month,
            DAY(DATE_ADD('2021-01-01', INTERVAL n - 1 DAY)) AS day_of_month,
            DAYOFWEEK(DATE_ADD('2021-01-01', INTERVAL n - 1 DAY)) AS day_of_week,
            CASE 
                WHEN DAYOFWEEK(DATE_ADD('2021-01-01', INTERVAL n - 1 DAY)) IN (1, 7) THEN TRUE 
                ELSE FALSE 
            END AS is_weekend
        FROM staging.number_sequence
        WHERE DATE_ADD('2021-01-01', INTERVAL n - 1 DAY) <= '2030-01-01';
    """,
    dag=dag,
)


load_data_products = MySqlOperator(
    task_id='load_data3',
    mysql_conn_id='mysql_default',
    sql="""
        INSERT INTO datawarehouse.dim_products(product_id,type,model)
        SELECT product_id,type,model
        FROM staging.products;
    """,
    dag=dag,
)

load_data_customers = MySqlOperator(
    task_id='load_data1',
    mysql_conn_id='mysql_default',
    sql="""
        INSERT INTO datawarehouse.dim_customers
        SELECT *
        FROM staging.customers;
    """,
    dag=dag,
)

load_data_orders = MySqlOperator(
    task_id='load_data2',
    mysql_conn_id='mysql_default',
    sql="""
        INSERT INTO datawarehouse.fact_orders(order_id, product_id, customer_id, date_id, order_total)
        SELECT c.order_id,c.product_id,c.customer_id,d.date_id,c.order_total
        FROM staging.orders c 
        INNER JOIN datawarehouse.dim_date d ON c.order_date = d.date;
    """,
    dag=dag,
)


create_database >> create_table_customers >> create_table_orders
create_database >> create_table_products
create_database >> create_table_date

create_table_customers >> load_data_customers
create_table_orders >> load_data_orders
create_table_products >> load_data_products
create_table_date >> load_data_date


