**Airflow** is the best orchestrator to run the multiple workflows

Install
-------
Docker for ubuntu 
Astro CLI 

Run commnads
------------
astro dev init
astro dev start
astro dev ps 
astro dev stop

Core Components
---------------
1. Web Server
2. Scheduler
3. Metadatabase 
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

Core Concepts
---------------
#### DAGs - Directed Acyclic Graphs
