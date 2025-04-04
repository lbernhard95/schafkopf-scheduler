locals {
  account_id            = data.aws_caller_identity.current.account_id
  region                = data.aws_region.current.name
  gmail_sender_email    = jsondecode(data.aws_secretsmanager_secret_version.gmail_credentials.secret_string)["GMAIL_SENDER_ADDRESS"]
  gmail_sender_password = jsondecode(data.aws_secretsmanager_secret_version.gmail_credentials.secret_string)["GMAIL_SENDER_PASSWORD"]
}
