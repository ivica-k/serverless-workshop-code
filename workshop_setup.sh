#!/usr/bin/env bash

PROJECT_PATH="savealife"

function setup_folder_venv() {
  python -m pip -qq install virtualenv
  python -m virtualenv -q venv
  source venv/bin/activate
  python -m pip -qq install chalice==1.27.0 awscli==1.25.76
  python -m pip -qq install -r "${PROJECT_PATH}/requirements-dev.txt"
}

#function setup_requirements() {
#  cd ${PROJECT_PATH}
#  cat > requirements.txt <<EOF
#boto3==1.24.75
#botocore>=1.25.2
#EOF
#
#  cat >> requirements-dev.txt <<EOF
#-r requirements.txt
#awscli==1.25.76
#httpie==3.1.0
#pytest==7.1.2
#python-dotenv==0.20.0
#EOF
#
#
#}

function setup_env_file() {
  cd ${PROJECT_PATH}
  cat > .env <<EOF
WORKSHOP_NAME="${entered_name}"
ENV=dev
AWS_PROFILE=workshop
AWS_DEFAULT_REGION=eu-central-1
EOF
}

function setup_chalice_config() {
    mkdir -p "${PROJECT_PATH}/.chalice"
    cat > "${PROJECT_PATH}/.chalice/config.json" <<EOF
{
  "version": "2.0",
  "app_name": "${entered_name}-savealife",
  "stages": {
    "dev": {
      "api_gateway_stage": "api"
    }
  }
}
EOF
}

function setup_aws_credentials() {
  read -sep "Enter AWS_ACCESS_KEY_ID value (will not be echoed): " entered_access_key
  read -sep "Enter AWS_SECRET_ACCESS_KEY value (will not be echoed): " entered_secret_key

  mkdir -p ~/.aws
  cat >> ~/.aws/credentials <<EOF

[workshop_user]
aws_access_key_id = ${entered_access_key}
aws_secret_access_key = ${entered_secret_key}

[workshop]
role_arn = arn:aws:iam::932785857088:role/serverless_workshop_role
source_profile = workshop_user
EOF
}

read -p "What is your first name? " entered_name

safe_name=$(echo $entered_name | iconv -f utf-8 -t us-ascii//TRANSLIT)

setup_folder_venv
setup_env_file
setup_chalice_config
setup_aws_credentials

export WORKSHOP_NAME=$safe_name
export ENV=dev
export AWS_PROFILE=workshop
export AWS_DEFAULT_REGION=eu-central-1

cd ${PROJECT_PATH}

echo -e "\nEnvironment verification:"
echo "------------------------------"
echo -e "Command output:"
env | grep -ie '\(^WORK\|^ENV\|^AWS\)'

echo -e "\nExpected output:"
echo -e "WORKSHOP_NAME=${entered_name}"
echo -e "AWS_PROFILE=workshop"
echo -e "AWS_DEFAULT_REGION=eu-central-1"
echo -e "ENV=dev\n"

echo -e "If the command output is not equal to the expected output, something went wrong. Ask for help :)"

echo -e "\nAWS credentials verification:"
echo "------------------------------"
echo -e "Command output:"
aws sts get-caller-identity

echo -e "\nExpected output:"
echo "{
    "UserId": "AROA5SLS6UJAFYZYO3O3W:botocore-session-1665219547",
    "Account": "932785857088",
    "Arn": "arn:aws:sts::932785857088:assumed-role/serverless_workshop_role/botocore-session-1665219547"
}"

echo -e "\nIf the command output is not similar (they can't be equal) to the expected output, something went wrong. Ask for help :)"