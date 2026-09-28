# Dashboard shows data from yesterday

## Symptoms
Widgets and reports show figures that are several hours out of date. The
connector status is Healthy.

## Common causes
1. A large estate takes longer to sync than the configured interval, so cycles
   queue behind one another.
2. The source system is rate limiting, which slows collection without failing it.
3. A scheduled maintenance window paused ingestion.
4. The dashboard is showing a cached view in the browser.

## How to fix
1. Check Settings > Integrations > [name] > Sync history for the duration of
   recent runs. If a run takes longer than the interval, increase the interval.
2. Look for 429 responses in the connector log.
3. Check the status page for a maintenance notice.
4. Reload the dashboard with a hard refresh to rule out a cached view.

## Escalate if
Sync history shows completed runs within the last hour but the dashboard still
shows older figures.
