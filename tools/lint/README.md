Canonical home of the house prose linters (`slop_lint.py`, `slop_rules_en.py`, `marks_lint.py`) and their test suites (moved from workshop `protocols/tools/` on 2026-11-10; made canonical 2026-11-14). `slop_lint.tables` accepts both package imports and direct script execution.

`lesson_check` projects authored HTML before calling these linters. Slop findings are review prompts (no density budget imposed); retired plain-bold/mark rules are warnings because COMPLAINTS #75 permits bold and reserves highlighting for readers. The approved Processo lesson also exceeds the eight-word colour-span cap, so span lengths are warnings. Other marks rules remain errors.

Run offline: `python3 -m unittest discover -s tools/lint -p "test_*.py"`.
