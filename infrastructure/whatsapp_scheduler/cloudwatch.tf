resource "aws_cloudwatch_log_group" "whatsapp_scheduler" {
  name              = "/aws/ecs/whatsapp_scheduler"
  retention_in_days = 30
}


resource "aws_cloudwatch_event_rule" "whatsapp_scheduler" {
  name                = "whatsapp_scheduler"
  schedule_expression = "rate(14 days)"
}

resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.whatsapp_scheduler.name
  target_id = "MyLambdaFunction"
  arn       = aws_lambda_function.whatsapp_scheduler.arn
}
