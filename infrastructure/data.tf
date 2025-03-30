data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

data "aws_secretsmanager_secret" "gmail_credentials" {
  name = "gmail_access_credentials"
}

data "aws_secretsmanager_secret_version" "gmail_credentials" {
  secret_id = data.aws_secretsmanager_secret.gmail_credentials.id
}
