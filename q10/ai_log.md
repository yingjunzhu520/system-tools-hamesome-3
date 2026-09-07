# ai_log.md（第 10 题：智能体修复循环记录）

- **目标**：`--name` 只含空白字符时 `main()` 须以 `SystemExit(2)` 结束，不输出问候语。
- **约束**：保留 argparse 结构，用 `p.error(...)` 退出；不改动 `print` 逻辑与正常路径。
- **测试命令**：`PYTHONPATH=src pytest tests/test_cli.py -v`
- **智能体改动**：`cli.py` 在 `parse_args()` 后新增 `if not a.name.strip(): p.error("--name 不能只含空白字符")`。
- **人工验证**：`git diff` 确认仅新增两行、无无关改动；重跑测试 `2 passed`。
