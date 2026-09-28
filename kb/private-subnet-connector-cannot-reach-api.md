# Collector in a private subnet cannot reach the platform API

## Symptoms
The collector container starts, then logs "connection timed out" when contacting
api.aegis.example.com. The collector never registers, so it does not appear in
the console.

## Common causes
1. The subnet has no route to the internet: no NAT gateway, or a route table that
   does not point 0.0.0.0/0 at one.
2. The security group has no outbound rule allowing TCP 443.
3. A network ACL blocks the return traffic. Unlike security groups, NACLs are
   stateless and need rules in both directions.
4. DNS resolution fails because the VPC has DNS resolution or DNS hostnames
   disabled.

## How to fix
1. Check the subnet's route table for a 0.0.0.0/0 entry pointing at a NAT gateway
   in a public subnet.
2. Confirm the collector's security group allows outbound TCP 443 to 0.0.0.0/0.
3. Review the NACL on the subnet. Ephemeral ports 1024-65535 must be allowed
   inbound for responses.
4. From inside the container, run: getent hosts api.aegis.example.com
   If that fails, the problem is DNS, not routing.
5. VPC Reachability Analyzer will name the exact component that blocks the path.

## Escalate if
Reachability Analyzer reports the path as reachable but the connection still
times out.
