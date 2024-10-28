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


resource "aws_iam_policy" "schafkopf_scheduler" {
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = "logs:CreateLogGroup"
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = "logs:CreateLogStream"
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = "logs:PutLogEvents"
        Resource = "*"
      },
    ]
  })
}


resource "aws_iam_role_policy_attachment" "schafkopf_scheduler" {
  role       = aws_iam_role.schafkopf_scheduler.name
  policy_arn = aws_iam_policy.schafkopf_scheduler.arn
}


resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.schafkopf_scheduler.function_name
  principal     = "events.amazonaws.com"

  # Reference the ARN of the CloudWatch event rule
  source_arn    = aws_cloudwatch_event_rule.every_day_at_five.arn
}