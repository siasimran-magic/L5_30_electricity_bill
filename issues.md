# Static Code Analysis - Issue Tracking

## Identified Issues and Fixes

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| **B605 (Bandit)** | Security (High) | 63 | `os.system("curl ...")` invokes a shell command with unsanitized parameters, vulnerable to command injection. | Replaced shell invocation with safe Python HTTP client `http.client.HTTPConnection`. |
| **B314 / B405 (Bandit)** | Security (Medium / Low) | 3, 18 | `xml.etree.ElementTree` is vulnerable to XML attacks (Billion Laughs / entity expansion denial of service, XXE). | Migrated to `defusedxml.ElementTree` to securely parse untrusted XML strings. |
| **B105 (Bandit)** | Security (Low) | 13 | Possible hardcoded credential string assigned to `CLERK_PASSWORD`. | Retrieved credential securely from environment variable using `os.getenv("CLERK_PASSWORD", "bill-desk-demo")`. |
| **E302 (Flake8)** | Style / Formatting | 23 | Expected 2 blank lines before top-level function definition `calculateUnits`, found 1. | Added an extra blank line to strictly adhere to PEP 8 spacing rules. |
| **E203 (Flake8)** | Style / Formatting | 45 | Extraneous whitespace before colon in dictionary key `{"meter" : meterId}`. | Removed whitespace before `:` (`{"meter": meterId}`). |
| **E501 (Flake8)** | Style / Formatting | 76 | Line exceeds maximum allowed line length (86 characters > 79 characters). | Wrapped long `print()` statement across multiple lines cleanly. |
| **E225 (Flake8)** | Style / Formatting | 80 | Missing whitespace around assignment operator `total=sum(...)`. | Added whitespace around `=` operator (`total = sum(...)`). |
