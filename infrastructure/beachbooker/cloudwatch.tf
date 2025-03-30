resource "aws_cloudwatch_log_group" "beachbooker_logs" {
  name              = "/aws/lambda/beachbooker"
  retention_in_days = 30
}

resource "aws_cloudwatch_event_rule" "beachbooker" {
  name                = "beachbooker"
  schedule_expression = "cron(0 22 ? * MON *)"  # This triggers at 10 PM UTC on mondays (midnight german summer time)
}

resource "aws_cloudwatch_event_target" "lambda_beachbooker_target" {
  rule      = aws_cloudwatch_event_rule.beachbooker.name
  target_id = "BeachBooker"
  arn       = aws_lambda_function.beachbooker.arn
}
