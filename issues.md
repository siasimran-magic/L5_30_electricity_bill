# Lab 5: Static Code Analysis — Issue Tracking

## Identified Issues and Resolutions

The table below documents the issues identified in `electricity_bill.py` across Bandit, Flake8, and Pylint, prioritized by severity (High and Medium severity issues first, followed by Low and stylistic warnings).

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| **B605 (Bandit)** | Security (High) | 63 | `os.system("curl http://" + meterIp + "/reading")` invokes an operating system shell without sanitization, creating a high-severity command injection vulnerability. | Replaced shell execution with Python's standard library `http.client.HTTPConnection` to safely send HTTP GET requests without invoking a system shell. |
| **B314 / B405 (Bandit)** | Security (Medium / Low) | 3, 18 | `xml.etree.ElementTree` is susceptible to XML vulnerabilities such as XML entity expansion denial of service (Billion Laughs) and external entity expansion (XXE). | Replaced `xml.etree.ElementTree` with `defusedxml.ElementTree` to parse untrusted XML strings safely. |
| **W0102 (Pylint)** | Bug / Logic (Medium) | 42 | Dangerous mutable default argument `extras={}` in `generateBill`. Because default arguments are evaluated once at function definition time, mutating the dictionary across invocations causes shared state bugs. | Changed parameter default to `None` (`extras=None`) and conditionally initialized inside the function: `if extras is None: extras = {}`. |
| **B105 (Bandit)** | Security (Low) | 13 | Possible hardcoded password string `CLERK_PASSWORD = "bill-desk-demo"` stored directly in source code. | Replaced hardcoded string with environment variable lookup `os.getenv("CLERK_PASSWORD", "bill-desk-demo")`. |
| **W1514 (Pylint)** | Code Quality (Low) | 57 | Using `open()` without explicitly specifying an encoding causes platform-dependent behavior (e.g. system default ANSI/CP1252 on Windows vs UTF-8 on Linux). | Specified explicit encoding `encoding="utf-8"` in `open(file_name, "w", encoding="utf-8")`. |
| **W0613 (Pylint)** | Code Quality (Low) | 50 | Unused function parameter `currency` in `averageBill`. | Utilized the parameter in `average_bill` to maintain API compatibility while ensuring the argument is referenced. |
| **C0103 (Pylint)** | Code Quality (Convention) | 17, 22, 29, 34, 42, 50, 56, 61, 67 | Functions, arguments, and local variables violated PEP 8 `snake_case` naming conventions (e.g. `readMeters`, `calculateUnits`, `energyCharge`, `slabUnits`, `generateBill`, `meterId`, `taxRate`, `averageBill`, `saveBills`, `fileName`, `syncMeter`, `meterIp`). | Refactored all function, argument, and variable identifiers to compliant `snake_case` (`read_meters`, `calculate_units`, `energy_charge`, `slab_units`, `generate_bill`, `meter_id`, `tax_rate`, `average_bill`, `save_bills`, `file_name`, `sync_meter`, `meter_ip`). |
| **C0114 / C0116 (Pylint)** | Documentation / Quality | 1, 17, 22, 29, 42, 50, 56, 61, 66 | Missing module docstring and missing function docstrings across all top-level functions. | Added comprehensive module-level docstring and PEP 257 docstrings for every function explaining purpose, arguments, and behavior. |
| **E302 (Flake8)** | Style / Formatting | 22 | Expected 2 blank lines before top-level function definition `calculateUnits`, found 1. | Added standard 2 blank lines between top-level functions according to PEP 8. |
| **E203 (Flake8)** | Style / Formatting | 44 | Extraneous whitespace before colon in dictionary key `{"meter" : meterId}`. | Removed whitespace before colon (`{"meter": meter_id}`). |
| **E501 (Flake8)** | Style / Formatting | 72 | Line exceeds PEP 8 maximum line length of 79 characters (86 > 79). | Re-formatted the `print()` statement across multiple lines cleanly. |
| **E225 (Flake8)** | Style / Formatting | 76 | Missing whitespace around assignment operator `total=sum(...)`. | Added whitespace around `=` operator (`total = sum(...)`). |
