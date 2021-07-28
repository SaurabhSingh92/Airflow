# airflow
Let's dance with airflow

Airflow as an orchestration tool is getting used extensively in the Foturne 500 Companies. It's an open source product with good support in varioud public cloud providers. 

Mostly it's a repeatative code and this repository help you develop a generic DAG, helping reduce development time and standarize various airflow related process.

------------------------------------------------------------------------------------------------------------------------------------------------------------------

<b>Steps to install Airflow on local Machine</b>

Kindly refer the artical which will help you with steps to install airflow on local machine. 

https://exploringcloud.medium.com/airflow-setup-astronomer-on-local-machine-window-628fedea346b

------------------------------------------------------------------------------------------------------------------------------------------------------------------

<b> Generic Dag </b>

It will include 2 files configuration file and generic dag. 

Configutation file: It could be a json/yaml file with details of the various task. 
Generic Dag: Python code which reads and creates the dag using the details present in the json/yaml files on run time. 
Main Dag: Actual DAG calling the generic dag with configuration file passed as parameter to differenciate different feature/Subject Area. 

-------------------------------------------------------------------------------------------------------------------------------------------------------------------

<b>Parent-Child Dag</b>

This feature is to show how to trigger child dag, set dependency using task senor and various other features used on day-to-day basis. 

<in - progess>
