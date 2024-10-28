resource "aws_s3_bucket" "state_bucket" {
  bucket = "schafkop-scheduler-tf-state-${local.account_id}"
}

resource "aws_dynamodb_table" "terraform_state_lock_table" {
  name         = "schafkopf-tf-state-lock"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }

  lifecycle {
    prevent_destroy = true
  }
}