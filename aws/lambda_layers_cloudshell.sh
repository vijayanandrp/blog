# Step 01 - Inside Cloudshell Create a run.sh
touch run.sh
vi run.sh # copy the bash scripts below
sudo chmod 755 run.sh

# ---------RUN.SH ----------------------
PYTHON_VERSION="python3.8"
ROOT_DIR="lambda_layers/python/lib/${PYTHON_VERSION}/site-packages/" 
LAYER_NAME="dev_packages_layer"
ZIP_FILE=${LAYER_NAME}".zip"

echo "===>>>>> Step 01 - Cloudshell install dependencies "
sudo amazon-linux-extras install ${PYTHON_VERSION}
curl -O https://bootstrap.pypa.io/get-pip.py
${PYTHON_VERSION} get-pip.py --user

cd ~
rm -rf ${ROOT_DIR}* 
mkdir -p ${ROOT_DIR}

echo "===>>>>> Step 02 - Activate virutal environment  "
${PYTHON_VERSION} -m venv venv
source venv/bin/activate

echo "===>>>>> Step 03 - Download Pip packages  "
${PYTHON_VERSION} -m pip install cffi -t ${ROOT_DIR}
pip3 install smart-open xmltodict -t ${ROOT_DIR}

echo "===>>>>> Step 04 - remove unused files  "
cd  ${ROOT_DIR}
rm -r *dist-info */__pycache__ # remove unused files
cd -
deactivate

echo "===>>>>> Step 05 - Zip the lambda_layers folder"
cd lambda_layers
zip -r ${ZIP_FILE} *

echo "===>>>>> Step 06 -  publish layer in AWS Lambda layers"
aws lambda publish-layer-version \
    --layer-name ${LAYER_NAME} \
    --license-info "MIT" \
    --compatible-runtimes ${PYTHON_VERSION} \
    --zip-file fileb://${ZIP_FILE} \
    --compatible-architectures "arm64" "x86_64" 
    
echo "-*- Done -*-"
