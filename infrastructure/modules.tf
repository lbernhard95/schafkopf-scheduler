
module "web" {
  source = "./web"
  providers = {
    aws        = aws
    aws.us-east = aws.us-east
  }
}

module "api" {
  source = "./api"
  dynamodb_email_arn = aws_dynamodb_table.emails.arn
  dynamodb_polls_arn = aws_dynamodb_table.polls.arn
}