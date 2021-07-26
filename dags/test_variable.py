from airflow import DAG
from airflow.models import Variable
from airflow.utils.dates import timedelta
from datetime import datetime
from airflow.operators.bash_operator import BashOperator
import json

conf = json.loads(json.dumps(Variable.get("Test", deserialize_json=True)))


# Default settings applied to all tasks
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG("test_variable", start_date=datetime(2019, 1, 1),
         max_active_runs=3,
         schedule_interval=timedelta(minutes=60),
         default_args=default_args,
         catchup=False) as dag:

    task1 = BashOperator(
        task_id="Print1",
        bash_command=f"echo { conf['first'] }"
    )

    task2 = BashOperator(
        task_id="Print2",
        bash_command=f"echo {conf['second']}"
    )

    task1 >> task2
