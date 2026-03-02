resource "aws_lambda_function" "whatsapp_scheduler" {
  function_name    = "whatsapp_scheduler"
  package_type     = "Image"
  image_uri        = "${aws_ecr_repository.whatsapp_scheduler.repository_url}:latest"
  source_code_hash = replace(data.aws_ecr_image.whatsapp_scheduler.image_digest, "sha256:", "")
  timeout          = 60
  memory_size      = 256

  role = aws_iam_role.whatsapp_scheduler.arn
}

resource "aws_iam_role" "whatsapp_scheduler" {
  name = "whatsapp_scheduler"
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

resource "aws_iam_policy" "whatsapp_scheduler" {
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = "s3:*"
        Resource = [
          aws_s3_bucket.whatsapp_scheduler.arn,
          "${aws_s3_bucket.whatsapp_scheduler.arn}/*"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "whatsapp_scheduler" {
  role       = aws_iam_role.whatsapp_scheduler.name
  policy_arn = aws_iam_policy.whatsapp_scheduler.arn
}

/*
resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.whatsapp_scheduler.function_name
  principal     = "events.amazonaws.com"

  # Reference the ARN of the CloudWatch event rule
  source_arn = aws_cloudwatch_event_rule.whatsapp_scheduler.arn
}
*/
