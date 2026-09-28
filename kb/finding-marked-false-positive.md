# Customer disputes a finding marked as a false positive

## Symptoms
The customer's security team believes a finding closed as a false positive was
genuine, or that an open finding is not a real risk.

## Common causes
1. A compensating control was detected, such as a firewall rule or a WAF policy
   that blocks the exploit path, so the finding was down-ranked.
2. The asset is not reachable from the internet or from any identity that an
   attacker could plausibly obtain.
3. The source data was stale, so the assessment used an out of date configuration.
4. A suppression rule created earlier by the customer matched the finding.

## How to fix
1. Open the finding and read the Evidence tab. It lists every signal used, the
   confidence score, and the reasoning for the verdict.
2. Check Suppression rules in Settings for a rule that matches the asset or the
   finding type.
3. If a compensating control was assumed, confirm it is still in place. Controls
   removed after the last sync will not be reflected until the next one.
4. If the customer disagrees with the verdict, use Reopen on the finding. This
   records the disagreement and feeds the tuning process.

Never dismiss a dispute without showing the evidence trail. The customer is
entitled to see why the platform reached its conclusion.

## Escalate if
The evidence trail does not support the verdict, or the same finding type is
repeatedly misjudged for one customer.
