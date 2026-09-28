# Large CSV export times out

## Symptoms
An export of findings or assets fails after several minutes with "Export failed"
or produces a truncated file.

## Common causes
1. The export exceeds the synchronous limit of 50,000 rows.
2. The browser tab was closed before the export finished.
3. The filter selected covers every asset in a large estate.
4. A slow connection drops the download partway through.

## How to fix
1. For more than 50,000 rows, use Schedule export instead of Download. Scheduled
   exports run in the background and email a link when ready.
2. Narrow the filter, for example by account or by severity, and export in parts.
3. Use the API for automated extraction. The findings endpoint pages results and
   is designed for large volumes.
4. Keep the tab open until a synchronous download completes.

## Escalate if
A scheduled export fails twice for the same filter.
