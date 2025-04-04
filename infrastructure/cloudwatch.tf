resource "aws_cloudwatch_log_group" "tasks_service" {
  name              = "/aws/lambda/schafkopf_scheduler"
  retention_in_days = 30
}


resource "aws_cloudwatch_event_rule" "every_day_at_five" {
  name                = "every_day_at_five"
  schedule_expression = "cron(0 5 * * ? *)" # This triggers at 5 AM UTC every day
}

resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.every_day_at_five.name
  target_id = "MyLambdaFunction"
  arn       = aws_lambda_function.schafkopf_scheduler.arn
}
