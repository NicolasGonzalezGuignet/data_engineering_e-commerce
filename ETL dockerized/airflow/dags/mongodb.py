from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
from pymongo import MongoClient
import json
import csv

mongo_host = 'airflow-mongo-1'
mongo_port = 27017
mongo_user = 'root'
mongo_password = 'example'
mongo_auth_db = 'admin'

def create_load_and_export():

    uri = f'mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}/{mongo_auth_db}'
    client = MongoClient(uri)
    db = client.catalog
    collection = db.electronics
    
    data=[]
    with open ("/data/catalog.json","r") as file:
        for line in file:
            data.append(json.loads(line))

    collection.insert_many(data)
    collection.create_index([('type',1)])

def export_to_csv():
    uri = f'mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}/{mongo_auth_db}'
    client = MongoClient(uri)
    db = client.catalog
    collection = db.electronics

    cursor = collection.find({}, {'_id': 1,'product_id': 1, 'type': 1, 'model': 1})

    with open('/data/electronics.csv', 'w', newline='') as csvfile:
        fieldnames = ['_id','product_id', 'type', 'model']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader() 

        for document in cursor:
            writer.writerow(document)


default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'retries': 1,
}

dag=DAG(dag_id='create_mongo_db_and_collection_pymongo',
        default_args=default_args,
        schedule_interval=None)

create_and_load_task = PythonOperator(
        task_id='create_db_and_collection_task',
        python_callable=create_load_and_export,
        dag=dag
    )

export_task = PythonOperator(
        task_id='export_task',
        python_callable=export_to_csv,
        dag=dag
    )

create_and_load_task >> export_task
