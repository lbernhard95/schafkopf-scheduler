resource "aws_lambda_function" "schafkopf_scheduler" {
  function_name    = "schafkopf_scheduler"
  package_type     = "Image"
  image_uri        = "${aws_ecr_repository.schafkopf_scheduler.repository_url}:latest"
  source_code_hash = replace(data.aws_ecr_image.schafkopf_scheduler.image_digest, "sha256:", "")
  timeout          = 60
  memory_size      = 512

  role = aws_iam_role.schafkopf_scheduler.arn

  environment {
    variables = {
      GMAIL_SENDER_ADDRESS = jsondecode(data.aws_secretsmanager_secret_version.gmail_credentials.secret_string)["GMAIL_SENDER_ADDRESS"]
      GMAIL_SENDER_PASSWORD = jsondecode(data.aws_secretsmanager_secret_version.gmail_credentials.secret_string)["GMAIL_SENDER_PASSWORD"]
    }
  }
}

resource "aws_iam_role" "schafkopf_scheduler" {
  name = "schafkopf_scheduler"
  assume_role_policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Action" : "sts:AssumeRole",
        "Principal" : {
          "Service" : [
            "lambda.amazonaws.com"
          ]
        },
        "Effect" : "Allow",
      }
    ]
  })
}
