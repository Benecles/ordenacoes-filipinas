Vendored from `ordenacoes-filipinas-workshop-ceo/protocols/tools/` on 2026-11-10, including all three test suites. The rule tables are unchanged. `slop_lint.tables` accepts both package imports and direct script execution.

`lesson_check` projects authored HTML before calling these linters. Slop findings are review prompts (no density budget imposed); retired plain-bold/mark rules are warnings because COMPLAINTS #75 permits bold and reserves highlighting for readers. The approved Processo lesson also exceeds the eight-word colour-span cap, so span lengths are warnings. Other marks rules remain errors.

Run offline: `python3 -m unittest discover -s tools/lint -p "test_*.py"`.
