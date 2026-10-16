# Issues found in society_dues.py (PES2UG24CS515)

Before: Pylint 5.81/10, Bandit 3 issues (1 Low, 2 Medium), Flake8 5 issues.
After: Pylint 10.00/10, Bandit 0 issues, Flake8 0 issues.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| SQL injection (B608) | Security (Medium) | 9 | `addDue` built the INSERT with an f-string, so a flat/month like `x'); DROP TABLE dues;--` could change the query | Used a parameterized query with `?` placeholders |
| Use of eval (B307 / W0123) | Security (Medium) | 21 | `penalty()` ran `eval(rule)` on whatever string was passed, so arbitrary code could run | Replaced with `ast.parse` + a small `safe_calc` that only allows numbers and + - * / |
| Hardcoded password (B105) | Security (Low) | 5 | `TREASURER_PASSWORD = "flat#101"` sitting in source code | Read it from the `TREASURER_PASSWORD` environment variable |
| Mutable default argument (W0102) | Bug | 8 | `history=[]` is shared across all calls so history from different calls got mixed | Default to `None` and create a new list inside the function |
| Broad exception (W0718) | Bug / Quality | 22 | `except Exception` hides every kind of error | Catch only `ValueError`, `SyntaxError`, `ZeroDivisionError` |
| Inconsistent return (R1710) | Bug | 12-16 | `collect()` returned the amount or fell off the end with no return | Added explicit `return None` |
| Comparison to None (E711 / C0121) | Style | 29 | `rows != None` | Changed to `rows is not None` |
| Function name not snake_case (C0103) | Style | 8 | `addDue` | Renamed to `add_due` and updated the call sites |
| Missing docstrings (C0114 / C0116) | Style | 1, 8, 12, 19, 27, 34 | No module or function docstrings | Added short docstrings |
| Line too long (E501 / C0301) | Style | 4, 13, 15 | Lines over 79 characters | Wrapped the long calls over multiple lines |
| Missing blank lines (E302) | Style | 12 | Only 0 blank lines before `def collect` | Added 2 blank lines |
| main() runs on import | Quality | 42 | `main()` was called at module level | Wrapped in `if __name__ == "__main__":` |
