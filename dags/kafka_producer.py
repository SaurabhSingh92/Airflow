import tweepy
from airflow import DAG
from airflow.models import Variable
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import tweepy as tw
from confluent_kafka import Producer

api_key = Variable.get("tw_api")
api_secret = Variable.get("tw_api_secret")
access_token = Variable.get("tw_access_token")
access_token_secret = Variable.get("tw_access_token_secret")

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
    conf = {'bootstrap.servers': "localhost:9092"}
    producer=Producer(conf)

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
        print(tweet.text)
        producer.flush()


# Using a DAG context manager, you don't have to specify the dag property of each task
with DAG('kafka_example_dag',
         start_date=datetime(2019, 1, 1),
         max_active_runs=3,
         schedule_interval=None,  # https://airflow.apache.org/docs/stable/scheduler.html#dag-runs
         default_args=default_args,
         catchup=False # enable if you don't want historical dag runs to run
         ) as dag:

    start = PythonOperator(
        task_id="prodcuder",
        python_callable=kafkaproducer,
        connection_id=kafka_conn_id,
    )

    end = BashOperator(
        task_id="sshlocalhost",
        bash_command='echo "Done"'
    )

    start >> end
