resource "aws_route53_record" "api" {
  zone_id = data.aws_route53_zone.domain.id
  name    = aws_api_gateway_domain_name.api.domain_name
  type    = "A"

  alias {
    name = aws_api_gateway_domain_name.api.domain_name
    zone_id = aws_api_gateway_domain_name.api.regional_zone_id
    evaluate_target_health = false
  }
}