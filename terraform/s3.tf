data "aws_caller_identity" "current" {}

#Create bucket
resource "aws_s3_bucket" "lambda_src" {
  bucket = "lambda-src-${data.aws_caller_identity.current.account_id}"
}

#zip lambda_function
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../src"
  output_path = "${path.module}/lambda_function.zip"
}

# Send zip file to bucket
resource "aws_s3_object" "upload_zip" {
  bucket = aws_s3_bucket.lambda_src.bucket
  key    = "lambda_function.zip"
  source = "../terraform/lambda_function.zip"
  acl    = "private"
}
