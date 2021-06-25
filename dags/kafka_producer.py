import tweepy
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
import tweepy as tw
from confluent_kafka import Producer
import socket

api_key = 'mIUDtuXy6b9C4tcV1CeNYfoPU'
api_secret = 'CrBbb9OhrYQmGKS78F1T4OX6w7cRNjseONTDtDyaf4gaYUtpm0'
access_token = '757946485-fXc95aDgG9tNSND05GbAm5CJUSRPH4tvoBD6XR6N'
access_token_secret = '8OyEjacpvFb0yReAnMrhwFE6yQHEDH2agEscNbu0smTt5'

args = {
    'owner': 'airflow',
    'start_date': days_ago(2),
}

def kafkaproducer:
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


with DAG as ( 'Produce App', default_args=args, catchup= false) as dag:
    start = PythonOperator(
        task_id="prodcuder",
        python_callable=kafkaproducer
    )
