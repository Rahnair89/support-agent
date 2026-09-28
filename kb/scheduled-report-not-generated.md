# A scheduled report did not arrive

## Symptoms
A weekly or monthly report configured under Reports does not appear in the
console or in the recipient's inbox.

## Common causes
1. The schedule uses a time zone different from the recipient's, so the report
   is not late, only expected at the wrong hour.
2. The report owner's account was disabled, which pauses the schedule.
3. The recipient's mail system rejected the message, often for size.
4. The report returned no rows and empty reports are suppressed by default.

## How to fix
1. Check the schedule's time zone in Reports > [name] > Schedule.
2. Confirm the owner's account is active. Transfer ownership if the owner has
   left the organisation.
3. Look in Reports > Delivery history for a bounce message.
4. Run the report manually. If it returns nothing, the filters are too narrow.
   Enable Send even when empty if the customer wants confirmation either way.

## Escalate if
Delivery history shows Sent but the recipient's mail system has no record of the
message.
