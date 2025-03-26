
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
  gmail_sender_address = jsondecode(data.aws_secretsmanager_secret_version.gmail_credentials.secret_string)["GMAIL_SENDER_ADDRESS"]
  gmail_sender_password = jsondecode(data.aws_secretsmanager_secret_version.gmail_credentials.secret_string)["GMAIL_SENDER_PASSWORD"]
}

module "beachbooker" {
  source = "./beachbooker"
}