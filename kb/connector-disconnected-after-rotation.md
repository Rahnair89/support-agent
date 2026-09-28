# Integration stops working after a credential rotation

## Symptoms
An integration that has been healthy for weeks moves to Disconnected. The error
is "401 Unauthorized" or "invalid_client". Nothing else changed.

## Common causes
1. The API key or client secret was rotated in the source system but not updated
   in Aegis.
2. The new credential was created with fewer scopes than the old one.
3. The credential has an expiry date that has passed.
4. The service account used to create the credential was disabled.

## How to fix
1. Generate a new credential in the source system and update it in
   Settings > Integrations > [name] > Update credentials.
2. Compare the scopes on the new credential with the list in our integration
   documentation. Read scopes are required for inventory, and write scopes for
   response actions.
3. Check the credential's expiry and set a calendar reminder before the next one.
4. Confirm the service account that owns the credential is still active.

## Escalate if
A freshly created credential with the documented scopes is rejected immediately.
