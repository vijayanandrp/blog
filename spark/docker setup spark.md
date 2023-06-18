
https://hub.docker.com/r/jupyter/all-spark-notebook


# 1. Docker pull local image
`docker pull jupyter/all-spark-notebook`

# 2. Start Services in windows 
``` 
docker run -it --rm -p 8888:8888 jupyter/all-spark-notebook  
```

# 3. to mount local drive to Docker Container 

##  IN DOCKER CLI
![image](https://user-images.githubusercontent.com/3804538/185597774-323ec718-450a-4d26-b693-23f07ba1a05f.png)

```bash

docker ps

docker exec -it <container_id or name> /bin/bash

```

## Run in the Docker App (container) 

`chown -R 1000 work/`


### 4. QUIT and RESTART DOCKER RUN FROM WINDOWS
```

docker run -p 8888:8888 -v C:\Users\hai\Documents\GitHub\blog:/home/jovyan/work  jupyter/all-spark-notebook  

docker run -p 8888:8888 -v C:\Users\vijay\GitHub\blog:/home/jovyan/work  jupyter/all-spark-notebook  

```


Reference - https://devtonight.com/questions/how-to-run-jupyter-notebooks-locally-in-a-docker-container
