locals {
 dim = ["Service", "support-agent"]
}
resource "aws_cloudwatch_dashboard" "golden" {
 dashboard_name = "support-agent-golden-signals"
 dashboard_body = jsonencode({
 widgets = [
 {
 type = "metric", x = 0, y = 0, width = 12, height = 6
 properties = {
 title = "Latency (ms)", region = var.region, period = 60, view = "timeSeries"
 metrics = [
 concat(["SupportAgent", "llm.latency"], local.dim, [{ stat = "p50", label = "p50" }]),
 concat(["SupportAgent", "llm.latency"], local.dim, [{ stat = "p99", label = "p99" }]),
 ]
 }
 },
 {
 type = "metric", x = 12, y = 0, width = 12, height = 6
 properties = {
 title = "Tokens per minute", region = var.region, period = 60, stat = "Sum"
 metrics = [concat(["SupportAgent", "llm.tokens.total"], local.dim)]
 }
 },
 {
 type = "metric", x = 0, y = 6, width = 12, height = 6
 properties = {
 title = "Escalation rate (%)", region = var.region, period = 300
 metrics = [
 [{ expression = "100 * esc / convos", label = "escalation %", id = "e1" }],
 concat(["SupportAgent", "conversation.escalated"], local.dim,
 [{ id = "esc", stat = "Sum", visible = false }]),
 concat(["SupportAgent", "conversations"], local.dim,
 [{ id = "convos", stat = "Sum", visible = false }]),
 ]
 }
 },
 {
 type = "metric", x = 12, y = 6, width = 12, height = 6
 properties = {
 title = "$ per 1,000 conversations", region = var.region, period = 3600
 metrics = [
 [{ expression = "1000 * cost / convos2", label = "$ / 1k conversations", id = "e2" }],
 concat(["SupportAgent", "llm.cost.usd"], local.dim,
 [{ id = "cost", stat = "Sum", visible = false }]),
 concat(["SupportAgent", "conversations"], local.dim,
 [{ id = "convos2", stat = "Sum", visible = false }]),
 ]
 }
 },
 ]
 })
}