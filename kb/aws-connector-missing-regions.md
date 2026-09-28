# Assets appear from only some AWS regions

## Symptoms
The inventory shows EC2 instances and security groups from us-east-1 but nothing
from eu-west-1 or ap-south-1, even though the connector status is healthy.

## Common causes
1. The region list on the connector was left at the default, which is the home
   region only.
2. The regions are not enabled on the AWS account. Newer regions are opt-in.
3. An SCP restricts activity to an approved set of regions, so read calls in
   other regions are denied.
4. The scan for the additional regions has not completed its first run.

## How to fix
1. Open Settings > Integrations > AWS > Edit and select every region the customer
   uses. Save and trigger a manual sync.
2. In the AWS console, go to Account > AWS Regions and confirm the regions show
   as Enabled.
3. Review SCPs for a Deny with a aws:RequestedRegion condition.
4. A first sync across many regions can take up to 45 minutes. Check the sync
   history before investigating further.

## Escalate if
Regions are enabled, selected and unrestricted, but a full sync cycle completes
with no assets from them.
