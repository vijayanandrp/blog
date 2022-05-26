# Windows
1. Download a plugin from chrome https://chrome.google.com/webstore/detail/create-aws-credentials-by/diodlmdnepfflhpmlhbgbjlbgbifakkp?hl=en
2. Download the `credentials` file to Download
3. create the `.aws` directory in the user directory
4. create file `config` in `.aws` directory

`config`
```
[default]
region = us-west-1
```

Run the below script in the Git Bash
`bash aws_creds.sh`

```
#!/usr/bin/bash

cd ~;

USER_DIR=$(pwd)
DOWNLOADED=${USER_DIR}/Downloads/credentials
CRED_PATH=${USER_DIR}/.aws/credentials

echo "[+] moving aws credenetials from downloaded path..."
mv ${DOWNLOADED} ${CRED_PATH}

echo " "
echo "[+] Testing some aws s3 ls commands locally..."
aws s3 ls
```
