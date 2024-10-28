resource "aws_cloudwatch_log_group" "tasks_service" {
  name              = "/aws/lambda/schafkopf_scheduler"
  retention_in_days = 30
}
