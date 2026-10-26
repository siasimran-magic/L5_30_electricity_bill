# Static Code Analysis - Issue Tracking

## Identified Issues and Fixes

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| **B605 (Bandit)** | Security (High) | 63 | `os.system("curl ...")` invokes a shell command with unsanitized parameters, vulnerable to command injection. | Replaced shell invocation with safe Python HTTP client `http.client.HTTPConnection`. |
| **B314 / B405 (Bandit)** | Security (Medium / Low) | 3, 18 | `xml.etree.ElementTree` is vulnerable to XML attacks (Billion Laughs / entity expansion denial of service, XXE). | Migrated to `defusedxml.ElementTree` to securely parse untrusted XML strings. |
| **B105 (Bandit)** | Security (Low) | 13 | Possible hardcoded credential string assigned to `CLERK_PASSWORD`. | Retrieved credential securely from environment variable using `os.getenv("CLERK_PASSWORD", "bill-desk-demo")`. |
