import tweepy
from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
import tweepy as tw
from confluent_kafka import Producer
import socket

api_key = 'mIUDtuXy6b9C4tcV1CeNYfoPU'
api_secret = 'CrBbb9OhrYQmGKS78F1T4OX6w7cRNjseONTDtDyaf4gaYUtpm0'
access_token = '757946485-fXc95aDgG9tNSND05GbAm5CJUSRPH4tvoBD6XR6N'
access_token_secret = '8OyEjacpvFb0yReAnMrhwFE6yQHEDH2agEscNbu0smTt5'

# Default settings applied to all tasks
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

def kafkaproducer():
    conf = {'bootstrap.servers': "localhost:9092",
            'client.id': socket.gethostname()}
    producer = Producer(conf)

    auth = tw.OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)

    new_search = "bmw -filter:retweets"

    tweets = tw.Cursor(api.search,
                       q=new_search,
                       lang="en",
                       since='2021-06-21',
                       show_user=True).items(5)

    for tweet in tweets:
        producer.produce('sample', key=f"{tweet.id_str}", value=f"{tweet.text}")
        producer.flush()


# Using a DAG context manager, you don't have to specify the dag property of each task
with DAG('example_dag',
         start_date=datetime(2019, 1, 1),
         max_active_runs=3,
         schedule_interval=timedelta(minutes=1),  # https://airflow.apache.org/docs/stable/scheduler.html#dag-runs
         default_args=default_args,
         catchup=False # enable if you don't want historical dag runs to run
         ) as dag:

    start = PythonOperator(
        task_id="prodcuder",
        python_callable=kafkaproducer
    )

    start
