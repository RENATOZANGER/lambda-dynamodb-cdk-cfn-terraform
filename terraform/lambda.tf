#Create Lambda
resource "aws_lambda_function" "lambda_function" {
  depends_on = [aws_s3_object.upload_zip]
  function_name = var.function_name
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.12"
  filename      = data.archive_file.lambda_zip.output_path
  role          = aws_iam_role.lambda_execution_role.arn

  environment {
    variables = {
      TABLE_NAME = var.table_name
    }
  }
}

# Create the public url for lambda
resource "aws_lambda_function_url" "lambda_function_url" {
  function_name      = aws_lambda_function.lambda_function.function_name
  authorization_type = "NONE"
}
