# Reflection (PES2UG24CS515)

**1. Which issues were easiest and hardest to fix?**
Easiest were the style ones (docstrings, snake_case, blank lines, `is not None`) since the tools tell you exactly what to change. Hardest was `eval` in `penalty()`. You can't just delete it because the program needs to calculate the rule like `"50 * 2"`, so I had to write a small safe evaluator using `ast`.

**2. Did the tools give any false positives?**
Not really, but the Bandit hardcoded password one (B105) is only Low severity and in this program it's a demo value, so it's more of a warning than a real leak. I still moved it to an environment variable because secrets in source code get committed to git. Also Pylint and Flake8 report the same thing sometimes (like `!= None` and line length) so the counts overlap.

**3. How would you use static analysis in a real workflow?**
Run flake8 and pylint as a pre-commit hook or in the CI pipeline so a PR fails if the score drops, and run bandit in CI too for security checks. That way problems are caught before code review and not by the reviewers.

**4. What improvements did you see after the fixes?**
Pylint went from 5.81 to 10.00, Bandit from 3 issues to 0, and Flake8 from 5 to 0. The code is also safer (no SQL injection or eval), easier to read because of docstrings and naming, and the history bug can't happen anymore. The program output is still the same (2500, 100, ['A-102']).
