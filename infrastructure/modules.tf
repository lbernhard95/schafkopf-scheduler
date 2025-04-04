
module "web" {
  source = "./web"
  providers = {
    aws         = aws
    aws.us-east = aws.us-east
  }
}

module "api" {
  source                = "./api"
  dynamodb_email_arn    = aws_dynamodb_table.emails.arn
  dynamodb_polls_arn    = aws_dynamodb_table.polls.arn
  gmail_sender_address  = local.gmail_sender_email
  gmail_sender_password = local.gmail_sender_password
}

module "beachbooker" {
  source                = "./beachbooker"
  gmail_sender_email    = local.gmail_sender_email
  gmail_sender_password = local.gmail_sender_password
}
