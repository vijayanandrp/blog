ROOT_DIR="lambda_layers/python/lib/python3.7/site-packages/" 

ZIP_FILE="aws_s3_security_layer.zip"

LAYER_NAME="aws_s3_security_layer"

cd ~

rm -rf ${ROOT_DIR}* 

mkdir -p ${ROOT_DIR}

python3 -m venv venv

source venv/bin/activate

# 1) install the dependencies in the desired folder

python3 -m pip install cffi  -t  ${ROOT_DIR}

pip3 install smart-open cryptography  -t  ${ROOT_DIR}.

cd  ${ROOT_DIR}

rm -r *dist-info __pycache__

cd -

deactivate

# 2) Zip the lambda_layers folder

cd lambda_layers

zip -r ${ZIP_FILE} *

# 3) publish layer

aws lambda publish-layer-version \
    --layer-name ${LAYER_NAME} \
    --license-info "MIT" \
    --compatible-runtimes python3.6 python3.7 python3.8 python3.9  \
    --zip-file fileb://${ZIP_FILE} \
    --compatible-architectures "arm64" "x86_64" 
    
    
# aws lambda publish-layer-version --layer-name my-layer --description "My layer"  \ 
# --license-info "MIT" --content S3Bucket=lambda-layers-us-east-2-123456789012,S3Key=layer.zip \
# --compatible-runtimes python3.6 python3.7 python3.8 \
# --compatible-architectures "arm64" "x86_64" 

# https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html

echo "-*- Done -*-"