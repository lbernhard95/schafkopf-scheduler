resource "aws_s3_bucket" "whatsapp_scheduler" {
  bucket = "whatsapp-scheduler-${data.aws_caller_identity.current.account_id}"
}

data "aws_caller_identity" "current" {}
