locals {
  account_id = data.aws_caller_identity.current.account_id
  web_sub_domain = "schafkopf.lukas-bernhard.de"
}
