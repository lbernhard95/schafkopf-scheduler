resource "aws_cloudwatch_log_group" "whatsapp_scheduler" {
  name              = "/aws/lambda/whatsapp_scheduler"
  retention_in_days = 30
}

resource "aws_scheduler_schedule" "whatsapp_scheduler" {
  name                         = "whatsapp_scheduler"
  schedule_expression          = "rate(14 days)"
  schedule_expression_timezone = "Europe/Berlin"
  start_date                   = "2026-03-07T10:00:00+01:00"

  flexible_time_window {
    mode = "OFF"
  }

  target {
    arn      = aws_lambda_function.whatsapp_scheduler.arn
    role_arn = aws_iam_role.whatsapp_scheduler_scheduler.arn
  }
}
