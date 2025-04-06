resource "aws_cloudwatch_log_group" "beachbooker_logs" {
  name              = "/aws/ecs/beachbooker"
  retention_in_days = 30
}


resource "aws_cloudwatch_event_rule" "beachbooker" {
  name                = "beachbooker"
  schedule_expression = "cron(0 22 ? * MON *)" # This triggers at 10 PM UTC on mondays (midnight german summer time)
}
