resource "aws_cloudwatch_log_group" "beachbooker_logs" {
  name              = "/aws/lambda/beachbooker"
  retention_in_days = 30
}

resource "aws_cloudwatch_event_rule" "every_monday_at_ten" {
  name                = "every_monday_at_ten"
  schedule_expression = "cron(0 22 ? * MON *)"  # This triggers at 10 PM UTC on mondays (midnight german summer time)
}

resource "aws_cloudwatch_event_target" "lambda_beachbooker_target" {
  rule      = aws_cloudwatch_event_rule.every_monday_at_ten.name
  target_id = "MyLambdaFunction"
  arn       = aws_lambda_function.beachbooker.arn
}