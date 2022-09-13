# Step 01 - Inside Cloudshell Create a run.sh
touch run.sh
vi run.sh # copy the bash scripts below
sudo chmod 755 run.sh

# ---------RUN.SH ----------------------
PYTHON_VERSION="python3.8"
PIP_DIR="lambda_layers/python/lib/${PYTHON_VERSION}/site-packages/" 
LAYER_NAME="dev_packages_layer"
ZIP_FILE=${LAYER_NAME}".zip"

echo "===>>>>> Step 01 - Cloudshell install dependencies "
sudo amazon-linux-extras install ${PYTHON_VERSION}
curl -O https://bootstrap.pypa.io/get-pip.py
${PYTHON_VERSION} get-pip.py --user

echo "===>>>>> Step 02 - create dir "
mkdir -p ${PIP_DIR}

echo "===>>>>> Step 03 - Download Pip packages  "
${PYTHON_VERSION} -m pip install smart-open xmltodict cffi -t ${PIP_DIR}

echo "===>>>>> Step 04 - remove unused files "
find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf
find . -path "*/*.pyc"  -delete
find . -path "*/*.pyo"  -delete
find . -path "*/*dist-info"  -delete
find . -path "*/__pycache__" -type d -exec rm -r {} ';'

echo "===>>>>> Step 05 - Zip the lambda_layers folder"
zip -r ${ZIP_FILE} ${PIP_DIR}

echo "===>>>>> Step 06 -  publish layer in AWS Lambda layers"
aws lambda publish-layer-version \
--layer-name ${LAYER_NAME} \
--compatible-runtimes python3.6 python3.7 python3.8 python3.9  \
--zip-file fileb://${ZIP_FILE} \
--compatible-architectures "arm64" "x86_64" \
--region eu-west-1 # change for your zone

# $ aws lambda publish-layer-version --layer-name pandas-layer --zip-file fileb://layer.zip --compatible-runtimes python3.8 --region us-east-1

echo "-*- Done -*-"
