from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.bash import BashOperator
from airflow.utils.task_group import TaskGroup
from datetime import datetime

args = {
    'owner': 'airflow',
    'start_date': datetime(2020, 1, 1),
}

with DAG('try_task_grp', schedule_interval= None, catchup= False, description= 'try task grp function',
         default_args=args) as dag:

    t1 = DummyOperator(
        task_id="Start"
    )

    with TaskGroup("New_task_group") as new_task_grp:
        t2 = BashOperator(
            task_id="Task1",
            bash_command='echo "Calling task 1"'
        )
        t3 = BashOperator(
            task_id='task2',
            bash_command='echo "calling task 2"'
        )
        t2>>t3

t1 >> new_task_grp