resource "aws_api_gateway_rest_api" "api" {
  name        = "schafkopf-api"

  endpoint_configuration {
    types = ["REGIONAL"]
  }
}


resource "aws_api_gateway_domain_name" "api" {
  domain_name      = local.api_sub_domain
  regional_certificate_arn = aws_acm_certificate.certs.arn
  endpoint_configuration {
    types = ["REGIONAL"]
  }
}
/*
resource "aws_api_gateway_base_path_mapping" "api" {
  domain_name = aws_api_gateway_domain_name.api.domain_name
  stage_name  = aws_api_gateway_stage.api.stage_name
  api_id      = aws_api_gateway_rest_api.api.id
}*/


resource "aws_api_gateway_rest_api_policy" "api_policy" {
  rest_api_id = aws_api_gateway_rest_api.api.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = "*",  # Change this to specific principals in production
        Action   = "execute-api:Invoke",
        Resource = "${aws_api_gateway_rest_api.api.execution_arn}/*"  # Allows access to all resources and methods
      }
    ]
  })
}


/*resource "aws_api_gateway_deployment" "api" {
  rest_api_id       = aws_api_gateway_rest_api.api.id
  triggers = {
    # NOTE: The configuration below will satisfy ordering considerations,
    #       but not pick up all future REST API changes. More advanced patterns
    #       are possible, such as using the filesha1() function against the
    #       Terraform configuration file(s) or removing the .id references to
    #       calculate a hash against whole resources. Be aware that using whole
    #       resources will show a difference after the initial implementation.
    #       It will stabilize to only change when resources change afterwards.
    redeployment = sha1(jsonencode([
      aws_api_gateway_resource.api.id,
      aws_api_gateway_method.api.id,
      aws_api_gateway_integration.api.id,
      aws_api_gateway_rest_api.api.id
    ]))
  }

  depends_on = [
    aws_api_gateway_integration.api,
  ]
}

resource "aws_api_gateway_stage" "api" {
  deployment_id = aws_api_gateway_deployment.api.id
  rest_api_id   = aws_api_gateway_rest_api.api.id
  stage_name    = "v1"
}*/

resource "aws_api_gateway_resource" "api" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  parent_id   = aws_api_gateway_rest_api.api.root_resource_id
  path_part   = "{proxy+}"
}

resource "aws_api_gateway_method" "api" {
  rest_api_id      = aws_api_gateway_rest_api.api.id
  resource_id      = aws_api_gateway_resource.api.id
  http_method      = "ANY"
  authorization    = "NONE"

  request_parameters = {
    "method.request.path.proxy" = true
  }
}
/*
resource "aws_api_gateway_integration" "api" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.api.id
  http_method             = aws_api_gateway_method.api.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.api.invoke_arn
}
*/