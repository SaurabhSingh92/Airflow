from dag_factory.generic_dag import CreateDagOperator
from airflow import DAG

default_args = { 'owner': "Saurabh "}

dag = CreateDagOperator.CreateDag("Generic_test_dag",  default_args)
