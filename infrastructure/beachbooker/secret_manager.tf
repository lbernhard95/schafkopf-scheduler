resource "aws_secretsmanager_secret" "zhs_user_secret" {
  name = "zhs_user_secret_3"
}

data "aws_secretsmanager_secret_version" "zhs_user_secret" {
  secret_id = aws_secretsmanager_secret.zhs_user_secret.id
}