# Connector fails with a certificate error behind a corporate proxy

## Symptoms
The collector logs "SSL: CERTIFICATE_VERIFY_FAILED" or "self signed certificate
in certificate chain". The same collector works from an unproxied network.

## Common causes
1. The corporate proxy performs TLS inspection and presents its own certificate,
   which the collector does not trust.
2. The proxy environment variables are not set, so the collector tries a direct
   connection that the firewall silently drops.
3. The proxy requires authentication that has not been configured.

## How to fix
1. Add the corporate root certificate to the collector's trust store by mounting
   it and setting AEGIS_CA_BUNDLE to its path.
2. Set HTTPS_PROXY and NO_PROXY on the collector. NO_PROXY should include
   internal addresses and the metadata endpoint 169.254.169.254.
3. If the proxy needs credentials, include them in the HTTPS_PROXY value or use
   the proxy_auth setting in the collector configuration file.
4. As a temporary alternative, ask the network team to add our API domain to the
   TLS inspection bypass list.

## Escalate if
The root certificate is mounted and trusted but verification still fails. Attach
the output of: openssl s_client -connect api.aegis.example.com:443
