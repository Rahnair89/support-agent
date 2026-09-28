# Rotate an API token without downtime

## Symptoms
Not a fault. This describes the supported procedure for replacing an API token
that is about to expire or may have been exposed.

## Common causes
1. Scheduled rotation under the customer's own key management policy.
2. A token was committed to a repository or shared in a message and must be
   replaced.
3. An employee who created the token has left.

## How to fix
1. In Settings > API tokens, create a second token with the same scopes. Two
   active tokens are supported, which is what makes a zero downtime rotation
   possible.
2. Update every client to use the new token.
3. Watch Settings > API tokens > Last used for the old token. When it stops
   updating for 24 hours, nothing is still using it.
4. Revoke the old token.

If the token may have been exposed, revoke it first and accept the brief outage.
Availability is less important than a live credential in the wrong hands.

## Escalate if
Last used continues to update after every known client has been updated, and the
source cannot be identified from the audit log.
