resource "aws_sns_topic" "alerts" {
 name = "support-agent-alerts"
}
resource "aws_sns_topic_subscription" "email" {
 count = var.alert_email == "" ? 0 : 1
 topic_arn = aws_sns_topic.alerts.arn
 protocol = "email"
 endpoint = var.alert_email
}
resource "aws_cloudwatch_metric_alarm" "latency_p99" {
 alarm_name = "support-agent-latency-p99"
 alarm_description = "p99 latency of the support agent is too high"
 namespace = "SupportAgent"
 metric_name = "llm.latency"
 dimensions = { Service = "support-agent" }
 extended_statistic = "p99"
 period = 60
 evaluation_periods = 5
 datapoints_to_alarm = 3
 threshold = var.alarm_threshold_ms
 comparison_operator = "GreaterThanThreshold"
 treat_missing_data = "notBreaching"
 alarm_actions = [aws_sns_topic.alerts.arn]
 ok_actions = [aws_sns_topic.alerts.arn]
}
