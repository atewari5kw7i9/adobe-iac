resource "aws_sns_topic" "email_updates" {
  name = "email-notification-topic"
}

resource "aws_sns_topic_subscription" "user_updates_email_target" {
  topic_arn = aws_sns_topic.email_updates.arn
  protocol  = "email"
  endpoint  = "aditya.tewari@yahoo.com"
  depends_on = [aws_sns_topic.email_updates]
}