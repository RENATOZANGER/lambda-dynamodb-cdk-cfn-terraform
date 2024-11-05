# lambda-dynamodb-cdk-cfn-terraform ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Terraform](https://img.shields.io/badge/terraform-%235835CC.svg?style=for-the-badge&logo=terraform&logoColor=white) ![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white) ![AmazonDynamoDB](https://img.shields.io/badge/Amazon%20DynamoDB-4053D6?style=for-the-badge&logo=Amazon%20DynamoDB&logoColor=white)

This project was created to implement an infrastructure that includes a Lambda with a public URL for inserting and retrieving data from DynamoDB, creating policies and roles, and creating DynamoDB.

The infrastructure was provisioned using CloudFormation, Terraform, and AWS CDK.

The Lambda function code is centralized in a single file `lambda_function.py`, responsible for connecting to DynamoDB to insert records and fetch data.

## Prerequisites
[Installing CDK with Python]( https://docs.aws.amazon.com/pt_br/cdk/v2/guide/work-with-cdk-python.html)

Validate the installed CDK
  ```bash
  cdk --version
  ```

[Installing the AWS CLI](https://docs.aws.amazon.com/pt_br/cli/latest/userguide/getting-started-install.html)
  ```bash
  aws --version
  ```

## Configure AWS Access
[Configure your AWS credentials](https://docs.aws.amazon.com/pt_br/cli/v1/userguide/cli-configure-files.html)
  ```bash
  aws configure
  ```

Validate aws access with an example to get the account_id
  ```bash
  aws sts get-caller-identity 
  ```

### Using CDK with Python
**_NOTE:_** Don't forget to run the `npm install -g aws-cdk` command to install the CDK globally.
After installation, you can use commands such as cdk init, cdk deploy, cdk synth, and cdk destroy to create, modify, and destroy infrastructure stacks in your AWS account.

In AWS CDK, the `cdk bootstrap` command prepares your AWS account and region environment to receive the infrastructure you want to provision.
  ```bash
 cdk bootstrap <Account_id>/us-east-1
   ```

Below is the example I made for using CDK with python:
  ```bash
  mkdir cdk_python # I created the folder cdk_python
  cd cdk_python # Access the folder cdk_python
  cdk init sample-app --language python # Initialize a new CDK project with a sample application using Python
  source .venv/bin/activate  # Activate the virtual environment on Linux or Mac
  python.exe -m pip install --upgrade pip # Upgrade pip
  pip install -r requirements.txt # Install the packages
  ```

CDK Main Commands
  
  ```bash
  cdk synth # Compile the project

  cdk deploy # Deploy the code

  cdk destroy # Destroy the project
   ```

### Preparing for CloudFormation and Terraform
**_NOTE:_** For CloudFormation and Terraform, you need to zip the lambda_function.py code and upload it to the S3 bucket you created.
  ```bash
  aws s3 mb s3://<bucket-name> # Create an S3 bucket to store the Lambda code

  zip lambda_function.zip lambda_function.py # Zip the code
  
  aws s3 cp lambda_function.zip s3://<bucket-name>/ # Upload zip to bucket
  ```

After creating the bucket, change the bucket name in the files:
- Terraform
```bash
# variables.tf
variable "bucket_name" {
  type    = string
  default = "<bucket-name>"
}
```

- CloudFormation
```bash
# lambda_dynamodb.yaml
  BucketName:
    Type: String
    Default: "<bucket-name>"
    Description: Bucket Name
```


### CloudFormation

```bash
  cd cloudFormation # Access the folder cloudFormation

  aws cloudformation create-stack --stack-name my-stack --template-body file://lambda_dynamodb.yaml --capabilities CAPABILITY_IAM # Create the CloudFormation stack

  aws cloudformation delete-stack --stack-name my-stack # Destroy the stack
   ```

### Terraform
```bash
cd terraform # Access the folder terraform

terraform init # Initialize Terraform

terraform plan # To check the resources that will be created

terraform apply -auto-approve # Apply settings

terraform destroy -auto-approve # Do the destroy
   ```

## Testing the Lambda Public URL
To test Lambda, use the curl commands below with the generated public URL:

Insert item:
```bash
curl -X POST "<lambda-url>" -H "Content-Type: application/json" -d '{"name": "Example Product", "price": 29.99}'
   ```

Search for items:
```bash
curl -X GET "<lambda-url>"
   ```

With this, the infrastructure and Lambda function will be ready to use.

For more details, see the documentation:
- [AWS CDK](https://docs.aws.amazon.com/cdk/v2/guide/home.html) 
- [CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html)
- [Terraform](https://developer.hashicorp.com/terraform/docs)