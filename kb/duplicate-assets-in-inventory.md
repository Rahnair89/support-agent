# The same asset appears more than once

## Symptoms
A single server or container appears as two or three entries in the inventory,
sometimes with different identifiers and different findings attached.

## Common causes
1. Two connectors report the same asset with identifiers that cannot be matched,
   for example a cloud provider ID and an endpoint agent ID.
2. The hostname changed between syncs, so the newer record did not match the
   older one.
3. An asset was rebuilt with the same name but a new identifier.
4. The deduplication key configured for the environment does not exist on all
   sources.

## How to fix
1. Open both records and compare the Identifiers section. If they share an
   instance ID or a MAC address, they should merge on the next sync.
2. Use Merge assets on the inventory page to link them manually.
3. In Settings > Inventory, check the deduplication key. Cloud instance ID is the
   most reliable in AWS environments; hostname is the least reliable.
4. Records for deleted assets age out after 30 days of no reporting.

## Escalate if
Two records share an instance ID but do not merge after a full sync.
