data "aws_route53_zone" "domain" {
  name = "lukas-bernhard.de"
}

data "aws_acm_certificate" "cert" {
  domain = "*.lukas-bernhard.de"
}
