from airflow import DAG
import json
import os
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago


class CreateDagOperator:

    @staticmethod
    def get_config(path, filename):
        with open(os.path.join(path, filename), "r") as sample:
            config = json.load(sample)
            return config

    @staticmethod
    def CreateDag(dag_name, default_args):
        home_path = "/Users/saurabhsingh/PycharmProjects/airflow/dags/jobconfig"
        job_dict = CreateDagOperator.get_config(home_path, "jobconfig.json")

        default_args_upt = job_dict["args"].update(default_args)

        with DAG(dag_id=dag_name,
                 default_args=default_args_upt,
                 start_date=eval(job_dict["default"]["start_date"]),
                 catchup=eval(job_dict["default"]["catchup"]),
                 ) as dag:

            for job, task in job_dict["Task"].items():

                job = eval(task["operator"])(
                    task_id=task["task_name"],
                )

                job

            return dag
