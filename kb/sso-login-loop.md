# SAML sign-in returns to the login page in a loop

## Symptoms
After authenticating with the identity provider, the browser returns to the Aegis
login page instead of the dashboard. No error is displayed.

## Common causes
1. The Assertion Consumer Service URL in the identity provider does not exactly
   match the one in our SSO settings, including the trailing path.
2. The NameID format is not set to emailAddress, so the assertion cannot be
   matched to a user.
3. The signing certificate in our settings has expired or was rotated at the
   identity provider.
4. Clock skew between the identity provider and our service invalidates the
   assertion window.

## How to fix
1. Compare the ACS URL character by character with the value in
   Settings > Authentication > SSO.
2. Set the NameID format to urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress.
3. Upload the current signing certificate from the identity provider.
4. Capture the SAML response with a browser extension and check the NotBefore and
   NotOnOrAfter timestamps against the current time.

## Escalate if
The assertion is valid and the certificate current, but the session still does
not establish. Include the decoded SAML response with secrets removed.
