resource "aws_lambda_function" "beachbooker" {
  function_name    = "beachbooker"
  package_type     = "Image"
  image_uri        = "${aws_ecr_repository.beachbooker.repository_url}:latest"
  source_code_hash = replace(data.aws_ecr_image.beachbooker.image_digest, "sha256:", "")
  timeout          = 60
  memory_size      = 512

  role = aws_iam_role.beachbooker.arn

  environment {
    variables = {
      LOG_GROUP_NAME = aws_cloudwatch_log_group.beachbooker_logs.name
      ZHS_USERNAME = jsondecode(data.aws_secretsmanager_secret_version.zhs_user_secret.secret_string)["ZHS_USERNAME"]
      ZHS_PASSWORD = jsondecode(data.aws_secretsmanager_secret_version.zhs_user_secret.secret_string)["ZHS_PASSWORD"]
    }
  }
  
  depends_on = [
    aws_iam_role_policy_attachment.beachbooker,
    aws_cloudwatch_log_group.beachbooker_logs,
  ]
}

resource "aws_iam_role" "beachbooker" {
  name = "beachbooker"
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

resource "aws_iam_policy" "beachbooker" {
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
      }
    ]
  })
}


resource "aws_iam_role_policy_attachment" "beachbooker" {
  role       = aws_iam_role.beachbooker.name
  policy_arn = aws_iam_policy.beachbooker.arn
}


resource "aws_lambda_permission" "allow_cloudwatch_beachbooker" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.beachbooker.function_name
  principal     = "events.amazonaws.com"

  # Reference the ARN of the CloudWatch event rule
  source_arn    = aws_cloudwatch_event_rule.every_monday_at_ten.arn
}