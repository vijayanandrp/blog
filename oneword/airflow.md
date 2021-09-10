**Airflow** is the best orchestrator to run the multiple workflows (Compared to Oozie)

Install
-------
Docker for ubuntu 
Astro CLI 

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
Worker ------> Where? (on which we want to run the job/workflow example - localexecutor->local process)


**Architecture** 

One node (simple architecture)
Web Server -----> MetaStore (DB) ----> Scheduler <----TASK OBJECT ---> Executor/Queue <-----pulled by ---- Worker 
![image](https://user-images.githubusercontent.com/3804538/132122327-83a52b89-86d5-4da6-8b89-8b63e560bacc.png)

Multinode
![image](https://user-images.githubusercontent.com/3804538/132122513-7d1a33af-31dd-4ae8-be7e-7fa05030b682.png)

Core Concepts [DAGs -> Operators -> Task -> Task Instance]
------------------------------------------------------------
#### DAGs - Directed Acyclic Graphs (Operators)

An acyclic graph is **a graph without cycles (a cycle is a complete circuit)**. When following the graph from node to node, you will never visit the same node twice. This graph (the thick black line) is acyclic, as it has no cycles (complete circuits). A connected acyclic graph, like the one above, is called a tree.

DAGs is a group of operators in each node.
1. Nodes and Edges are directed
2. No loops
![image](https://user-images.githubusercontent.com/3804538/132123025-8b3bb6f5-29a1-413d-96a7-1a145a28ae15.png)


#### Operators (Task)
Task (T1) in the DAG is called Operator.
1. Action Operators
2. Transfer Operators (Src->Dest transfer data)
3. Sensor Operators (wait for Something to happen before run anything)

#### Task
Instance of an Operator
#### Task Instance
Represents a sepcific run of a task: DAG + TASK + Point in time

![image](https://user-images.githubusercontent.com/3804538/132122894-b3a36a30-99e9-485f-b402-a1211aad2a2a.png)

Webserver parses Folder Dags for every 30s <br>
Scheduler parses Folder Dags for every 300s / 5min <br>

![image](https://user-images.githubusercontent.com/3804538/132123177-ee33aab5-1731-4919-8158-3fe9de3064c4.png)


How to access DAGs? - UI, CLI, Rest API

ORDER OF COMMANDS
-------------------
`docker ps` <br> 
`docker exec -it <CONTAINER_ID> /bin/bash` <br>
`airflow db init` <br>
`airflow db upgrade` <br>
`ariflow db reset` <br>
`airflow webserver` <br>
`ariflow scheduler ` <br>
`airflow celery worker` <br>
`airlfow dags paues|unpause|list` <br>
`airflow tasks list <DAG_ID>` <br>
`airflow tasks test <DAG_ID> <OPERATOR_ID> <DATE_STAMP>` <br>

