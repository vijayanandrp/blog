https://hub.docker.com/r/jupyter/all-spark-notebook

`docker pull jupyter/all-spark-notebook`


# To Run in windows 

``` 
docker run -it --rm -p 8888:8888 jupyter/all-spark-notebook  
```

### DOCKER CLI

`chown -R 1000 work/`


```
docker run -p 8888:8888 -v C:\Users\hai\Documents\GitHub\blog:/home/jovyan/work  jupyter/all-spark-notebook  
docker run -p 8888:8888 -v C:\Users\vpandian\blog:/home/jovyan/work  jupyter/all-spark-notebook  
```


Reference - https://devtonight.com/questions/how-to-run-jupyter-notebooks-locally-in-a-docker-container
