resource "aws_lambda_function" "api" {
  function_name    = "schafkopf_api"
  package_type     = "Image"
  image_uri        = "${aws_ecr_repository.api.repository_url}:latest"
  source_code_hash = replace(data.aws_ecr_image.api.image_digest, "sha256:", "")
  timeout          = 60
  memory_size      = 512

  role = aws_iam_role.api.arn
}

resource "aws_iam_role" "api" {
  name = "schafkopf_api"
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


resource "aws_iam_policy" "api" {
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


resource "aws_iam_role_policy_attachment" "api" {
  role       = aws_iam_role.api.name
  policy_arn = aws_iam_policy.api.arn
}


resource "aws_lambda_permission" "wheatley-api" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.api.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.api.execution_arn}/*"
}
