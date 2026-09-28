# User account is locked after failed sign-in attempts

## Symptoms
The user sees "Your account is temporarily locked. Try again later." Correct
credentials are still rejected.

## Common causes
1. Ten consecutive failed sign-in attempts within 15 minutes triggers an
   automatic lock that clears after 30 minutes.
2. A saved password in a browser or script is retrying an old credential in the
   background.
3. An administrator suspended the account.

## How to fix
1. Wait 30 minutes, or ask an administrator to open Settings > Users, select the
   user, and choose Unlock.
2. Ask the user to clear the saved password from their browser and any script or
   mobile client that may still be retrying it. This is the usual reason an
   account locks again immediately after being unlocked.
3. Check the account status on the same page. Suspended is a manual action and is
   different from locked.

## Escalate if
The account locks again within minutes of an unlock and the audit log shows no
failed attempts.
