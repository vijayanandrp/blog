https://hub.docker.com/r/jupyter/all-spark-notebook

`docker pull jupyter/all-spark-notebook`


# To Run in windows 

``` 
docker run -it --rm -p 8888:8888 jupyter/all-spark-notebook  
```

### DOCKER CLI

`chown -R 1000 work/`


```
docker run -p 8888:8888 -v /full/path/to/work:/home/jovyan/work  jupyter/all-spark-notebook  
```
