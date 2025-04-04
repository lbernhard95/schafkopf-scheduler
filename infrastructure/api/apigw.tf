resource "aws_apigatewayv2_api" "schafkopf_api" {
  name          = "schafkopf_api"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "schafkopf_api" {
  api_id           = aws_apigatewayv2_api.schafkopf_api.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.api.invoke_arn
}

resource "aws_apigatewayv2_route" "schafkopf_api" {
  api_id    = aws_apigatewayv2_api.schafkopf_api.id
  route_key = "$default" # Catch-all route
  target    = "integrations/${aws_apigatewayv2_integration.schafkopf_api.id}"
}

resource "aws_apigatewayv2_stage" "default_stage" {
  api_id      = aws_apigatewayv2_api.schafkopf_api.id
  name        = "$default"
  auto_deploy = true
}

resource "aws_apigatewayv2_domain_name" "custom_domain" {
  domain_name = local.api_sub_domain
  domain_name_configuration {
    certificate_arn = aws_acm_certificate_validation.cert-validation.certificate_arn
    endpoint_type   = "REGIONAL"
    security_policy = "TLS_1_2"
  }
}

resource "aws_apigatewayv2_api_mapping" "custom_domain_mapping" {
  api_id      = aws_apigatewayv2_api.schafkopf_api.id
  domain_name = aws_apigatewayv2_domain_name.custom_domain.domain_name
  stage       = aws_apigatewayv2_stage.default_stage.name
}
