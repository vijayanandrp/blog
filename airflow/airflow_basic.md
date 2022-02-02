**Airflow** is the best orchestrator to run the multiple workflows (Compared to Oozie)

Install
-------
1. Docker for ubuntu  <br>
2. Astro CLI <br>

Run commnads
------------
astro dev init <br>
astro dev start <br>
astro dev ps  <br>
astro dev stop <br>

Core Components
---------------
1. Web Server
2. Metadatabase
3. Scheduler  
4. Executor
5. Worker

Behind the components there are two main components
---------------------------------------------------
Executor -----> How? ( Example - localexecutor, sequentialexecutor, kubernetesexecutor) <br><br>
Worker ------> Where? (on which we want to run the job/workflow example - localexecutor->local process) <br>


**Architecture** <br> <br>
**One node** (simple architecture) <br>
Web Server -----> MetaStore (DB) ----> Scheduler <----TASK OBJECT ---> Executor/Queue <-----pulled by ---- Worker <br>

<img src="https://user-images.githubusercontent.com/3804538/132122327-83a52b89-86d5-4da6-8b89-8b63e560bacc.png"  style="height:75%; width:75%" > <br>
**Multinode**<br><br>
<img src="https://user-images.githubusercontent.com/3804538/132122513-7d1a33af-31dd-4ae8-be7e-7fa05030b682.png"  style="height:75%; width:75%" > <br>

Core Concepts [DAGs -> Operators -> Task -> Task Instance]
------------------------------------------------------------
#### DAGs - Directed Acyclic Graphs (Operators)

An acyclic graph is **a graph without cycles (a cycle is a complete circuit)**. When following the graph from node to node, you will never visit the same node twice. This graph (the thick black line) is acyclic, as it has no cycles (complete circuits). A connected acyclic graph, like the one above, is called a tree.
<br>
DAGs is a group of operators in each node.
1. Nodes and Edges are directed
2. No loops
<br>
<img src="https://user-images.githubusercontent.com/3804538/132123025-8b3bb6f5-29a1-413d-96a7-1a145a28ae15.png"  style="height:50%; width:50%" > <br>

#### Operators (Task)
Task (T1) in the DAG is called Operator.
1. Action Operators
2. Transfer Operators (Src->Dest transfer data)
3. Sensor Operators (wait for Something to happen before run anything)

#### Task
Instance of an Operator

#### Task Instance
Represents a sepcific run of a task: DAG + TASK + Point in time

<img src="https://user-images.githubusercontent.com/3804538/132122894-b3a36a30-99e9-485f-b402-a1211aad2a2a.png"  style="height:75%; width:75%" > <br>

Webserver parses **Folder Dags** for every 30s <br>
Scheduler parses **Folder Dags** for every 300s / 5min <br>
<img src="https://user-images.githubusercontent.com/3804538/132123177-ee33aab5-1731-4919-8158-3fe9de3064c4.png"  style="height:75%; width:75%" > <br>


### How to access DAGs? - UI, CLI, Rest API

ORDER OF COMMANDS
-------------------
`docker ps`  Pick the **container_id** <br>
`docker exec -it <CONTAINER_ID> /bin/bash` <br>
`airflow db init` <br>
`airflow dags list` Pick the **dag_id** <br>
`airflow tasks list <DAG_ID>` <br>
`airflow tasks test <DAG_ID> <OPERATOR_ID> <DATE_STAMP>` <br>

`airflow dags backfill -s <START_DATE> -e <END_DATE> --reset_dagruns <DAG_ID>` Run the history <br>
`airflow db upgrade` <br>
`ariflow db reset` <br>
`airflow webserver` <br>
`ariflow scheduler ` <br>
`airflow celery worker` <br>
`airlfow dags paues|unpause|list` Turn on or pause or list dags <br>

Code
=====
```python
from os import wait
from airflow import DAG 
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator, task
from airflow.operators.bash import BashOperator
from airflow.sensors.filesystem import FileSensor
from airflow.utils.dates import days_ago
from airflow.models.baseoperator import chain, cross_downstream

from datetime import datetime, timedelta
from pprint import pprint

default_args ={
  'retry': 5,
  'retry_delay': timedelta(minutes=5),
#   'email_on_failure': True,
#   'email_on_retry': True,
#   'email': 'vijay@anand.com'
}

def _downloading_data(ti, **kwargs):
    print("===>>>> downloading_data - test ")
    pprint(kwargs)
    with open("/tmp/my_file.txt", "w") as fp:
        fp.write(f"{kwargs}")
    ti.xcom_push(key="my_key", value="5555")
        
def _checking_data(ti):
    my_xcom = ti.xcom_pull(key='my_key', task_ids=['downloading_data'])
    print("===>>> check data = ", my_xcom)
    
def _failure(context):
    print('====>>>> On failure callback')
    pprint(context)
    
    
with DAG(dag_id='simple_dag', 
        start_date=days_ago(3),
        schedule_interval="@daily", 
        default_args=default_args,
        catchup=True) as dag:
    
    downloading_data = PythonOperator(
        task_id = "downloading_data",
        python_callable=_downloading_data
    )
    
    checking_data = PythonOperator(
        task_id="checking_data",
        python_callable=_checking_data
    )
    waiting_for_data = FileSensor(
        task_id = "waiting_for_data",
        fs_conn_id = "fs_default1",
        filepath="my_file.txt"
    )
    
    processing_data = BashOperator(
        task_id = "processing_data",
        bash_command='exit 1',
        on_failure_callback = _failure
    )   
    
    # cross_downstream([downloading_data, checking_data], [waiting_for_data, processing_data])
    chain(downloading_data, checking_data, waiting_for_data, processing_data)
    
    # downloading_data >> waiting_for_data >> processing_data
    # downloading_data >> [waiting_for_data, processing_data]
    
    # downloading_data.set_downstream(waiting_for_data)
    # waiting_for_data.set_downstream(processing_data)
    
    # task_1 = DummyOperator(
    #     task_id = "task_1"
    # )
    
    # task_2 = DummyOperator(
    #     task_id = "task_2",
    #     retry = 3
    # )
    
    # task_3 = DummyOperator(
    #     task_id = "task_3"
    # )
    

```
