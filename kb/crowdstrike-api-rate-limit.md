# Endpoint connector fails with HTTP 429

## Symptoms
The endpoint integration flips between Healthy and Degraded. The connector log
shows repeated "429 Too Many Requests" responses and partial data in the
inventory.

## Common causes
1. Another tool is using the same API client credentials, so the two share one
   rate limit budget.
2. The sync interval is set lower than the vendor's published limit allows.
3. A full re-sync was triggered while an incremental sync was already running.
4. The vendor applies a tenant-wide limit that a large estate exceeds during the
   initial import.

## How to fix
1. Create a dedicated API client in the vendor console for Aegis rather than
   reusing an existing one.
2. Increase the sync interval in Settings > Integrations to 30 minutes or more
   during the initial import.
3. Wait for the in-progress sync to finish before starting another. The platform
   retries with exponential backoff automatically.
4. Ask the vendor to raise the rate limit for the tenant if the estate is large.

## Escalate if
429 responses continue for more than two hours with a dedicated client and a
30 minute interval.
