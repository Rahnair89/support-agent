# Asset count is higher than the customer expects

## Symptoms
The usage page shows more billable assets than the customer believes they have.

## Common causes
1. Ephemeral workloads such as autoscaling instances or CI runners each count as
   an asset while they exist.
2. Duplicate records are being counted twice. See duplicate-assets-in-inventory.
3. A newly connected account added assets that were not in the original estimate.
4. Deleted assets remain in the count until they age out after 30 days.

## How to fix
1. Open Usage > Breakdown and group by account and by asset type to find the
   source of the increase.
2. Exclude short lived workloads from the inventory with a tag based exclusion
   rule in Settings > Inventory.
3. Resolve duplicates so a single asset is not counted more than once.
4. Compare the current count with the same day in the previous month rather than
   with the peak, which ephemeral workloads distort.

## Escalate if
The breakdown does not account for the difference, or the count rises with no
corresponding change in the customer's estate.
