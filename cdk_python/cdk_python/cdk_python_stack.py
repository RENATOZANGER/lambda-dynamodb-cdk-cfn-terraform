import os
from constructs import Construct
from aws_cdk import (
    RemovalPolicy,
    Stack,
    aws_dynamodb as dynamodb,
    aws_lambda as lambda_,
    CfnOutput
)


class CdkPythonStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create Table
        products_table = dynamodb.Table(
            self, 'TableDynamoDB',
            table_name='ProductsTable',
            partition_key=dynamodb.Attribute(
                name='id',
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY
        )

        # Create Lambda
        lambda_function = lambda_.Function(
            self, 'LambdaFunction',
            function_name='Lambda_and_dynamodb',
            code=lambda_.Code.from_asset('../src'),
            handler='lambda_function.lambda_handler',
            runtime=lambda_.Runtime.PYTHON_3_12,
            environment={
                'TABLE_NAME': products_table.table_name
            })
        
        # Granting permissions to the lambda function to read data from DynamoDB table
        products_table.grant_read_write_data(lambda_function.role)

        # Adding a Lambda URL to tje Lambda Function to execute it from the Internet
        function_url = lambda_function.add_function_url(auth_type=lambda_.FunctionUrlAuthType.NONE)

        # Adding a stack output for the function URL to access it easily
        CfnOutput(self, 'ProductListUrl', value=function_url.url)
