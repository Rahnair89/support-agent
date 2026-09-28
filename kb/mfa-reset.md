# Reset multi-factor authentication for a user

## Symptoms
A user has lost their phone or replaced their device and can no longer complete
the second factor at sign-in.

## Common causes
1. The device holding the authenticator app was lost, wiped or replaced.
2. The authenticator app was reinstalled without exporting the accounts.
3. Time drift on the device makes the generated codes invalid.

## How to fix
1. An administrator opens Settings > Users, selects the user, and chooses
   Reset MFA. The user is prompted to enrol a new device at their next sign-in.
2. The user should verify that automatic time synchronisation is enabled on the
   new device before enrolling. Codes fail if the clock drifts by more than
   about 30 seconds.
3. If the customer uses SSO, MFA is enforced by their identity provider and must
   be reset there instead. Aegis does not manage the second factor in that case.

## Escalate if
Reset MFA is greyed out for an administrator, or the user still cannot enrol
after a reset.
