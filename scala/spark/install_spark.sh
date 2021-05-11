cd ~ && cd Documents;
mkdir install_spark && cd install_spark;

sudo apt install default-jdk scala git -y

java -version; javac -version; scala -version; git --version

echo "[+] Dowloading the Spark binary............"
wget https://downloads.apache.org/spark/spark-3.1.1/spark-3.1.1-bin-hadoop2.7.tgz

tar xvf spark-*

sudo mv spark-3*-bin-hadoop2.7 /opt/spark

echo "export SPARK_HOME=/opt/spark" >> ~/.profile
echo "export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin" >> ~/.profile
echo "export PYSPARK_PYTHON=/usr/bin/python3" >> ~/.profile

# nano .profile
# export SPARK_HOME=/opt/spark
# export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin
# export PYSPARK_PYTHON=/usr/bin/python3

source ~/.profile

# start-master.sh
# start-slave.sh -m 512M spark://ubuntu1:7077
# start-slave.sh -c 1 spark://ubuntu1:7077

start-all.sh



