  101  mkdir install_spark;
  102  cd install_spark;
  103  sudo apt install default-jdk scala git 
  104  cd ~ && cd Documents;
  105  mkdir install_spark;
  106  cd install_spark;
  107  sudo apt install default-jdk scala git 
  108  java -version; javac -version; scala -version; git --version
  109  echo "[+] Dowloading the Spark binary............"
  110  wget https://downloads.apache.org/spark/spark-3.1.1/spark-3.1.1-bin-hadoop2.7.tgz
  111  tar xvf spark-*
  112  sudo mv spark-3*-bin-hadoop2.7 /opt/spark
  113  echo "export SPARK_HOME=/opt/spark" >> ~/.profile
  114  echo "export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin" >> ~/.profile
  115  echo "export PYSPARK_PYTHON=/usr/bin/python3" >> ~/.profile
  116  source ~/.profile
  117  echo "export SPARK_HOME=/opt/spark" >> ~/.bashrc
  118  echo "export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin" >> ~/.bashrc
  119  echo "export PYSPARK_PYTHON=/usr/bin/python3" >> ~/.bashrc
  120  source ~/.bashrc
  121  start-master.sh
  122  start-slave.sh -m 512M spark://ubuntu1:7077
  123  # start-slave.sh -c 1 spark://ubuntu1:7077
  124  #start-all.sh
  125  spark-shell 
  126  git status
  127  ls
