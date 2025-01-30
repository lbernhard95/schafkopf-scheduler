resource "aws_dynamodb_table" "emails" {
  name         = "schafkopf_emails"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "email"

  attribute {
    name = "email"
    type = "S"
  }
}

resource "aws_dynamodb_table" "polls" {
  name         = "schafkopf_polls"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "uuid"

  attribute {
    name = "uuid"
    type = "S"
  }
}

resource "aws_dynamodb_table" "scheduler" {
  name         = "schafkopf_scheduler"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "partition_key"
  range_key    = "sort_key"

  attribute {
    name = "partition_key"
    type = "S"
  }

  attribute {
    name = "sort_key"
    type = "S"
  }
}

resource "aws_dynamodb_table" "subscriber" {
  name         = "schafkopf_subscriber"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "partition_key"

  attribute {
    name = "partition_key"
    type = "S"
  }
}