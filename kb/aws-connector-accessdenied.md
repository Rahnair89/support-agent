# AWS connector shows "AccessDenied" after onboarding

## Symptoms
The AWS integration status reads "Error: AccessDenied when calling AssumeRole".
No assets appear from the affected account, and the last successful sync time
stops updating.

## Common causes
1. The external ID in the role's trust policy does not match the one shown in the
   Aegis console for that connector.
2. The trust policy principal is not the Aegis platform account.
3. A service control policy in AWS Organizations denies sts:AssumeRole or the
   read APIs the connector needs.
4. The role was deployed to the management account but not to the member accounts.

## How to fix
1. In IAM, open the role, then the Trust relationships tab. Confirm the Principal
   is the Aegis account ID shown in Settings > Integrations > AWS, and that the
   sts:ExternalId condition matches the external ID on the same page.
2. In CloudTrail, filter eventName = AssumeRole and errorCode = AccessDenied.
   The event names the identity and the condition that failed.
3. Check the SCPs attached to the organizational unit containing the account.
   An explicit deny in an SCP overrides any role policy.
4. If only some accounts are missing, confirm the role exists with the same name
   in every member account. Deploying with CloudFormation StackSets avoids drift.

## Escalate if
The trust policy, external ID and SCPs are all correct and AssumeRole still fails
for more than one hour. Include the CloudTrail event ID in the ticket.
