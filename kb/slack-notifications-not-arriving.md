# Slack notifications are not being delivered

## Symptoms
Findings and alerts appear in the console but no message arrives in the
configured Slack channel.

## Common causes
1. The Slack app was removed from the workspace or from the specific channel.
2. The notification rule filters on a severity or asset group that the events do
   not match.
3. The channel was archived or renamed.
4. The webhook URL was regenerated in Slack.

## How to fix
1. In Slack, open the channel and confirm the Aegis app is a member. Invite it
   again if it is not.
2. Open Settings > Notifications and check the rule's conditions against a recent
   event that should have matched.
3. Use Send test message on the rule. A test that succeeds while real events do
   not means the rule conditions are the problem, not the connection.
4. If the webhook was regenerated, paste the new URL into the integration.

## Escalate if
The test message succeeds and a matching event is confirmed, but no notification
is sent.
