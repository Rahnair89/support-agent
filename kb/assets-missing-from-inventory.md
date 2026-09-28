# Expected assets are missing from the inventory

## Symptoms
The customer knows a workload exists but cannot find it in the asset inventory,
while other assets from the same account are present.

## Common causes
1. The asset is in a region or account that is not included in the connector
   configuration.
2. The connector's role lacks the read permission for that specific service, for
   example ECS or EKS.
3. For Kubernetes, the cluster's access entries do not grant the connector role
   permission to list resources inside the cluster.
4. The asset was created after the last sync and the next one has not run.
5. An inventory filter or saved view is hiding it.

## How to fix
1. Confirm the account and region are both in scope for the connector.
2. Compare the role's policy with the permission list in our documentation. A
   missing read action shows in CloudTrail as AccessDenied for that service only.
3. For EKS, confirm the connector role has an access entry on the cluster.
4. Trigger a manual sync and wait for it to complete.
5. Clear all filters in the inventory view before concluding an asset is absent.

## Escalate if
The account, region and permissions are all correct and a completed sync still
does not return the asset.
