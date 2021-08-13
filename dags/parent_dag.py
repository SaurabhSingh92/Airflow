from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime, timedelta

# Default settings applied to all tasks
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# Using a DAG context manager, you don't have to specify the dag property of each task
with DAG('parent_dag',
         start_date=datetime(2019, 1, 1),
         max_active_runs=3,
         schedule_interval=timedelta(minutes=60),
         default_args=default_args,
         # catchup=False # enable if you don't want historical dag runs to run
         ) as dag:

    t1 = TriggerDagRunOperator(
        task_id="Child_Trigger",
        trigger_dag_id="child_dag",
        conf={
            "Date": "2021-01-01"
        }
    )

    t2 = DummyOperator(
        task_id="Dummy"
    )

    t1 >> t2

