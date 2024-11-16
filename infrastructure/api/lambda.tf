resource "aws_lambda_function" "api" {
  function_name    = "schafkopf_api"
  package_type     = "Image"
  image_uri        = "${aws_ecr_repository.api.repository_url}:latest"
  source_code_hash = replace(data.aws_ecr_image.api.image_digest, "sha256:", "")
  timeout          = 60
  memory_size      = 512

  role = aws_iam_role.api.arn

  environment {
    variables = {
      GMAIL_SENDER_ADDRESS = var.gmail_sender_address
      GMAIL_SENDER_PASSWORD = var.gmail_sender_password
    }
  }
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
      {
        "Effect": "Allow",
        "Action": [
            "dynamodb:BatchGetItem",
            "dynamodb:DescribeTable",
            "dynamodb:GetItem",
            "dynamodb:Query",
            "dynamodb:Scan"
        ],
        "Resource": [
          var.dynamodb_email_arn,
          var.dynamodb_polls_arn,
        ]
      },
      {
        "Effect": "Allow",
        "Action": [
            "dynamodb:PutItem",
            "dynamodb:UpdateItem",
            "dynamodb:DeleteItem",
        ],
        "Resource": var.dynamodb_email_arn,
      }
    ]
  })
}


resource "aws_iam_role_policy_attachment" "api" {
  role       = aws_iam_role.api.name
  policy_arn = aws_iam_policy.api.arn
}

resource "aws_lambda_permission" "api_gateway_invoke" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.api.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.schafkopf_api.execution_arn}/*"
}