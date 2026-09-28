# Our severity differs from the scanner's CVSS score

## Symptoms
A vulnerability the customer's scanner rates Critical appears as Medium or Low in
Aegis, or the reverse.

## Common causes
1. CVSS describes how bad a vulnerability is in the abstract. Our ranking also
   considers whether it can be reached and whether it is already blocked.
2. The asset is not reachable from an untrusted network, so the practical risk is
   lower than the CVSS score suggests.
3. A control already in place blocks the exploit path.
4. The vulnerability is on a public exploitation list, so our ranking is higher
   than CVSS alone would give.

## How to fix
1. Open the finding and read the Ranking factors panel. It shows reachability,
   exploitation status and detected controls, with the contribution of each.
2. Explain the difference in terms of the specific asset rather than in general
   terms. The same CVE on two servers can legitimately rank differently.
3. If the customer requires CVSS ordering for a compliance report, the CVSS score
   is available as a sortable column and in the API.

## Escalate if
The ranking factors describe a control or a network position that the customer
can demonstrate does not exist.
