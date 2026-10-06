Classify the customer's message into exactly one category.
Output only the category word, lowercase, with no punctuation or explanation.

Categories:
how_to  - asking how to do or configure something
bug     - something is broken, erroring, or not behaving as documented
account - login, access, permissions, billing, or user management
urgent  - ONLY an active security incident, suspected data exposure, or a
          complete outage affecting all users

Important: a single failing integration, a permission error, an AccessDenied
message, a rate limit, or one user unable to log in are NOT urgent. Those are
"bug" or "account". Reserve "urgent" for incidents, not errors.
