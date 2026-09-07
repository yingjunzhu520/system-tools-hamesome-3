# communication.md（第 11 题：协作材料重写）

## Issue（重写）

**标题**：`sdt-greet --name " "` 对空白姓名仍输出问候语并以 0 退出

**环境**：Windows（版本待确认）；greetlab-24070030103 v0.1.0；Python 版本待确认。

**复现命令**：`sdt-greet --name " "`

**期望结果**：以 `SystemExit(2)` 结束，不输出问候语。

**实际结果**：输出 `Hello, !`，退出码为 0。

## 提交信息（重写）

**标题**：fix: 空白姓名改为报错退出，而非输出问候语

**正文**：`--name` 传入纯空白时，`main()` 仍打印 `Hello, !` 并返回 0。新增 `if not a.name.strip(): p.error(...)` 校验，使该输入以 `SystemExit(2)` 结束，正常路径不受影响。

## 评审意见（重写）

**Blocking**：`cli.py` 缺少空白姓名校验，`--name " "` 会输出无意义的 `Hello, !`，且退出码 0 会让调用方误判成功。请在解析后新增 `a.name.strip()` 检查，空白时调用 `p.error(...)`（返回码 2），并补充对应测试。

**Nit**：可在 `--name` 的 `help` 文本中补充「不可为空或纯空白」说明。
