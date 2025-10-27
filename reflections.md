1. Which issues were the easiest to fix, and which were the hardest? Why?

Easiest: The flake8 formatting issues (like E302 for blank lines or W291 for trailing whitespace) and the unused import were the easiest.

Hardest: The use-of-global issue is hard because the fix isn't a simple change but a larger architectural refactor, like converting the script into a class.

2. Did the static analysis tools report any false positives? If so, describe one example.

No, in this specific lab, all the reports from pylint, bandit, and flake8 were accurate and pointed to legitimate issues.

3. How would you integrate static analysis tools into your actual software development workflow?

I would integrate them at two key points:

Local Development: First, by integrating the linters directly into the code editor (like VS Code) to provide real-time feedback with squiggly lines. Second, I would use pre-commit hooks. This would automatically run tools like flake8 and bandit every time I try to make a commit, preventing bad code from even entering the repository.

Continuous Integration (CI): I would add a "Lint & Test" stage to the CI pipeline. This step would run all the static analysis tools. If any high-severity issues are found, the build would fail, which blocks the pull request from being merged. This enforces a consistent quality standard for the entire team.

4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?

The improvements were:

Robustness: The code is far more resilient. It no longer crashes if you try to get a non-existent item (get_qty) or if the inventory.json file is missing (load_data). It also correctly catches only the specific KeyError in remove_item and properly closes files using the with statement, preventing resource leaks.

Security: A critical vulnerability (eval()) was completely removed, making the script much safer.

Readability: The code is much easier to read. All functions now follow the standard snake_case naming convention, and the entire file adheres to flake8 formatting rules for spacing, line length, and indentation.

Correctness: We fixed a major, hidden bug by correcting the mutable default arg in add_item, which now correctly creates a new log list for each call.
