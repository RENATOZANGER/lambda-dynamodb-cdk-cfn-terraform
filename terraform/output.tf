#Create the output to display the lambda url
output "product_list_url" {
  description = "URL to access the Lambda function"
  value       = aws_lambda_function_url.lambda_function_url.function_url
}