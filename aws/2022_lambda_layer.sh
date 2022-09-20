sudo amazon-linux-extras install python3.8
curl -O https://bootstrap.pypa.io/get-pip.py
python3.8 get-pip.py --user
mkdir python
python3.8 -m pip install pandas numpy -t python/
zip -r layer.zip python
aws lambda publish-layer-version --layer-name pandas-layer --zip-file fileb://layer.zip --compatible-runtimes python3.8 --region eu-west-1


https://aws.amazon.com/premiumsupport/knowledge-center/lambda-import-module-error-python/


sudo amazon-linux-extras install python3.8

curl -O https://bootstrap.pypa.io/get-pip.py

python3.8 get-pip.py --user

mkdir python

python3.8 -m pip install pandas numpy psycopg2 SQLAlchemy -t python/

zip -r layer.zip python

aws lambda publish-layer-version \
 --layer-name mics-layer \
 --description "Pandas Numpy psycopg2-binary SQLAlchemy" \
 --zip-file fileb://layer.zip \
 --compatible-runtimes python3.8 python3.9 \
 --region eu-west-1
