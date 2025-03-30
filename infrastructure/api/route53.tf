resource "aws_route53_record" "custom_domain_record" {
  zone_id = data.aws_route53_zone.domain.zone_id
  name    = local.api_sub_domain
  type    = "A"

  alias {
    name                   = aws_apigatewayv2_domain_name.custom_domain.domain_name_configuration[0].target_domain_name
    zone_id                = aws_apigatewayv2_domain_name.custom_domain.domain_name_configuration[0].hosted_zone_id
    evaluate_target_health = false
  }
}
