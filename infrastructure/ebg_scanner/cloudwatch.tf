resource "aws_cloudwatch_log_group" "ebg_scanner_logs" {
  name              = "/aws/ecs/ebg_scanner"
  retention_in_days = 30
}


resource "aws_cloudwatch_event_rule" "ebg_scanner" {
  name                = "ebg_scanner"
  schedule_expression = "cron(0 12,19 * * ? *)" # Triggers every day at 12 PM and 7 PM UTC
  arn                 = aws_lambda_function.ebg_scanner.arn
}
