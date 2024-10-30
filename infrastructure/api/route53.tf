resource "aws_route53_record" "api" {
  zone_id = data.aws_route53_zone.domain.id
  name    = aws_api_gateway_domain_name.api.domain_name
  type    = "A"
}