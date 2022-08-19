
https://hub.docker.com/r/jupyter/all-spark-notebook


# 1. Docker pull local 
`docker pull jupyter/all-spark-notebook`

# Start Services in windows 
``` 
docker run -it --rm -p 8888:8888 jupyter/all-spark-notebook  
```

# 2. to mount local drive to Docker Container 

## 3. IN DOCKER CLI
### Run in the Docker App (container) 

`chown -R 1000 work/`


### 4. DOCKER RUN FROM WINDOWS
```

docker run -p 8888:8888 -v C:\Users\hai\Documents\GitHub\blog:/home/jovyan/work  jupyter/all-spark-notebook  

docker run -p 8888:8888 -v C:\Users\vpandian\VijayAnandRP\GitHub\blog:/home/jovyan/work  jupyter/all-spark-notebook  

```


Reference - https://devtonight.com/questions/how-to-run-jupyter-notebooks-locally-in-a-docker-container
