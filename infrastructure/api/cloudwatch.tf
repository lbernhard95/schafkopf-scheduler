resource "aws_cloudwatch_log_group" "tasks_service" {
  name              = "/aws/lambda/schafkopf_api"
  retention_in_days = 30
}
