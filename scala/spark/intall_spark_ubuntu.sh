tmp_dir="install_spark"
download_url="https://apache.inspire.net.nz/spark/spark-3.1.2/spark-3.1.2-bin-hadoop3.2.tgz"
spark_path="/opt/spark"

cd ~ && cd Documents;

if [ -d $tmp_dir ]; then
  echo "Folder exists - $tmp_dir";
else
   echo "Folder doesnot exists - $tmp_dir";
   mkdir $tmp_dir;
fi

cd $tmp_dir;

if [ -d  $spark_path ]; then
  echo "Folder exists ";
else
   echo "Folder doesnot exists - $spark_path";
   sudo mkdir $spark_path ;
fi

sudo apt install -y default-jdk scala git;

java -version; javac -version; scala -version; git --version;

echo "[+] Dowloading the Spark binary............";
wget $download_url;


tar xvf spark-*

sudo cp -r spark-*/* $spark_path

# Set File ACL for all files and folders in /opt directory
sudo setfacl -R -m u:vijayanandrp:rwx /opt

echo "export SPARK_HOME=/opt/spark" >> ~/.profile
echo "export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin" >> ~/.profile
echo "export PYSPARK_PYTHON=/usr/bin/python3" >> ~/.profile
source ~/.profile

echo "export SPARK_HOME=/opt/spark" >> ~/.bashrc
echo "export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin" >> ~/.bashrc
echo "export PYSPARK_PYTHON=/usr/bin/python3" >> ~/.bashrc
source ~/.bashrc

start-master.sh
start-slave.sh -m 512M spark://ubuntu1:7077

spark-shell


# start-slave.sh -c 1 spark://ubuntu1:7077
# start-all.sh
