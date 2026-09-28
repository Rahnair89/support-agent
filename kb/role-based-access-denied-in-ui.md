# User sees "You do not have permission to view this page"

## Symptoms
A user can sign in but some pages are blocked, or actions such as suppressing a
finding are unavailable.

## Common causes
1. The user's role does not include the required permission. Viewer is read only;
   Analyst can triage; Administrator can change settings.
2. The user belongs to a group scoped to a subset of asset groups, and the page
   covers assets outside that scope.
3. Role changes made through SSO group mapping take effect only at the next
   sign-in.
4. Two group mappings conflict, and the more restrictive one applies.

## How to fix
1. Open Settings > Users, select the user, and compare their role with the
   permission matrix in our documentation.
2. Check the asset group scope on the user's group.
3. Ask the user to sign out and back in after any role change.
4. Where group mappings overlap, the most restrictive scope wins. Remove the user
   from the narrower group or widen its scope.

## Escalate if
The permission matrix says a role should allow an action and it remains blocked
after a fresh sign-in.
