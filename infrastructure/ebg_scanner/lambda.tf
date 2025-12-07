resource "aws_lambda_function" "ebg_scanner" {
  function_name    = "ebg_scanner"
  package_type     = "Image"
  image_uri        = "${aws_ecr_repository.ebg_scanner.repository_url}:latest"
  source_code_hash = replace(data.aws_ecr_image.ebg_scanner.image_digest, "sha256:", "")
  timeout          = 60
  memory_size      = 512

  role = aws_iam_role.ebg_scanner.arn

}

resource "aws_iam_role" "ebg_scanner" {
  name = "ebg_scanner"
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


resource "aws_iam_policy" "ebg_scanner" {
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = "logs:CreateLogGroup"
        Resource = "*"
      },
      {
        Effect   = "Allow"
        Action   = "logs:CreateLogStream"
        Resource = "*"
      },
      {
        Effect   = "Allow"
        Action   = "logs:PutLogEvents"
        Resource = "*"
      },
    ]
  })
}


resource "aws_iam_role_policy_attachment" "ebg_scanner" {
  role       = aws_iam_role.ebg_scanner.name
  policy_arn = aws_iam_policy.ebg_scanner.arn
}


resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.ebg_scanner.function_name
  principal     = "events.amazonaws.com"

  # Reference the ARN of the CloudWatch event rule
  source_arn = aws_cloudwatch_event_rule.ebg_scanner.arn
}
