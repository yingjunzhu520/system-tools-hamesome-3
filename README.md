# 第 3 周 系统开发工具基础 实验报告

> 课程：系统开发工具基础 · 中国海洋大学（985） · 计算机科学与技术
> 姓名：朱英俊 · 学号：24070030103 · 日期：2026 年 9 月 7 日

## 仓库目录

```
.
├── hamesome-report.cls         # 自定义 LaTeX 模板（基于 ctexart）
├── report.tex                  # LaTeX 实验报告源文件（本机 latexmk -xelatex 编译）
├── report.pdf                  # fpdf2 渲染的 PDF 预览（沙箱无 LaTeX 引擎）
├── commit_screenshot.png       # GitHub commit 记录截图
├── make_report_pdf.py          # fpdf2 渲染脚本
├── make_q_screenshots.py       # 终端风格截图渲染脚本
├── make_commit_png.py          # commit_screenshot 生成脚本
├── q09/                        # 第 9 题：打包构建 wheel
├── q10/                        # 第 10 题：智能体 TDD 修复循环
├── q11/                        # 第 11 题：协作材料重写
├── q12/                        # 第 12 题：PyTorch 线性回归
└── .git/                       # 本地仓库（分次增量提交）
```

## 本周四道实验题

| 题号 | 主题 | 主要工具 | 关键产物 |
|------|------|----------|----------|
| q09 | 打包与交付 | pyproject.toml / build / venv | `greetlab_*.whl` |
| q10 | 智能体编程 | pytest / 编程智能体 | `tests/`、`ai_log.md` |
| q11 | 不止于代码 | Markdown 协作规范 | `communication.md` |
| q12 | Python 与 PyTorch | torch / nn.Linear / SGD | `train.py` |

## 远程仓库

- **GitHub**：https://github.com/yingjunzhu520/system-tools-hamesome-3

认证方式：HTTPS（Git Credential Manager，令牌缓存于本机）。

## 本机编译真实 PDF

```bash
latexmk -xelatex report.tex   # 或 xelatex report.tex 编译两遍刷新交叉引用
```

## 沙箱环境说明

沙箱无 TeX 引擎，且为 Windows + Git Bash。本目录下：
- `report.tex` 是真实源文件，本机可立即编译。
- `report.pdf` 是 fpdf2 渲染的预览，覆盖 LaTeX 源的主要章节内容。
- `q09/q10/q11/q12` 子目录里有可运行脚本与运行输出。
- 终端截图（`q0X_img*.png`）由 `make_q_screenshots.py` 忠实渲染真实命令输出。
