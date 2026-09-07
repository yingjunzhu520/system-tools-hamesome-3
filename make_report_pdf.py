# -*- coding: utf-8 -*-
"""
make_report_pdf.py —— 把第 3 周实验报告的 LaTeX 源用 fpdf2 渲染为
与 hamesome-report.cls 同样风格的 PDF 预览。
沙箱无 LaTeX 引擎，本机可用 latexmk -xelatex 重新生成最终 PDF。
注意：simhei 字体缺 `·`/`^2` 等字形，已统一用 ASCII 兼容符。
"""
import os
from fpdf import FPDF
from PIL import Image

BASE = r"C:\Users\LENOVO\Desktop\系统开发工具基础_第3周_报告"

FONT = r"C:\Windows\Fonts\simhei.ttf"
ACCENT = (37, 99, 235)
SUB = (30, 64, 175)
DARK = (30, 30, 40)
GRAY = (90, 90, 100)
CODE_BG = (245, 247, 250)
LIGHT_GRAY = (200, 205, 215)

pdf = FPDF()
pdf.add_font("hei", "", FONT)
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=16)
EPW = pdf.epw
LM = pdf.l_margin


def title_block():
    pdf.set_draw_color(*ACCENT)
    pdf.set_line_width(1)
    y = pdf.get_y()
    pdf.line(LM, y, LM + EPW, y)
    pdf.ln(2)
    pdf.set_font("hei", "", 20)
    pdf.set_text_color(*ACCENT)
    pdf.cell(EPW, 10, "第 3 周 实验报告", align="C", ln=1)
    pdf.set_draw_color(*ACCENT)
    pdf.line(LM, pdf.get_y(), LM + EPW, pdf.get_y())
    pdf.ln(4)
    pdf.set_font("hei", "", 11)
    pdf.set_text_color(*DARK)
    for line in [
        "课程：系统开发工具基础",
        "姓名：朱英俊    学号：24070030103",
        "提交日期：2026 年 9 月 7 日",
    ]:
        pdf.cell(EPW, 7, line, align="C", ln=1)
    pdf.ln(3)


def section(num, name):
    pdf.ln(3)
    pdf.set_font("hei", "", 15)
    pdf.set_text_color(*ACCENT)
    pdf.cell(EPW, 9, f"{num}  {name}", ln=1)
    pdf.set_draw_color(*LIGHT_GRAY)
    pdf.set_line_width(0.3)
    y = pdf.get_y()
    pdf.line(LM, y, LM + EPW, y)
    pdf.set_text_color(*DARK)
    pdf.ln(2)


def sub(name):
    pdf.set_font("hei", "", 12)
    pdf.set_text_color(*SUB)
    pdf.cell(EPW, 7, name, ln=1)
    pdf.set_text_color(*DARK)
    pdf.ln(1)


def body(txt):
    pdf.set_font("hei", "", 10)
    pdf.set_text_color(40, 40, 50)
    pdf.multi_cell(EPW, 5.5, txt)
    pdf.ln(1)


def code(txt):
    pdf.set_font("hei", "", 9)
    pdf.set_fill_color(*CODE_BG)
    pdf.set_draw_color(*LIGHT_GRAY)
    pdf.set_text_color(20, 20, 30)
    pdf.multi_cell(EPW, 4.6, txt, border=1, fill=True)
    pdf.set_text_color(40, 40, 50)
    pdf.ln(1.5)


def bullet(txt):
    pdf.set_font("hei", "", 10)
    pdf.set_text_color(40, 40, 50)
    pdf.multi_cell(EPW, 5.5, "* " + txt)


def fig_label(txt):
    pdf.set_font("hei", "", 9)
    pdf.set_text_color(*GRAY)
    pdf.cell(EPW, 5.5, txt, align="C", ln=1)
    pdf.set_text_color(*DARK)
    pdf.ln(1)


def img(name, caption, fraction=0.97):
    """按原始长宽比把真实终端截图居中插入当前页，并加图注。"""
    full = os.path.join(BASE, name)
    if not os.path.exists(full):
        return
    im = Image.open(full)
    w, h = im.size
    target_w = EPW * fraction
    target_h = h * (target_w / w)
    if pdf.get_y() + target_h + 20 > pdf.h - 18:
        pdf.add_page()
    x = LM + (EPW - target_w) / 2
    pdf.set_draw_color(*LIGHT_GRAY)
    pdf.image(full, x, pdf.get_y(), target_w, target_h)
    pdf.set_y(pdf.get_y() + target_h)
    pdf.ln(1)
    fig_label("图 " + caption)


# ============ 标题区 ============
title_block()

# ============ 目录 ============
sub("目录")
pdf.set_font("hei", "", 10)
pdf.set_text_color(40, 40, 50)
toc = [
    "1  实验概览",
    "2  第 9 题：从源码构建并在干净环境安装 Wheel",
    "3  第 10 题：让编程智能体进入可验证的修复循环",
    "4  第 11 题：把协作材料改成可执行信息",
    "5  第 12 题：修复一个可复现的线性回归训练循环",
    "6  课后练习与解题感悟（14 个实例）",
    "7  版本控制与提交记录",
    "8  小结",
]
for t in toc:
    pdf.cell(EPW, 6.5, t, ln=1)
pdf.ln(3)

# ============ 1 实验概览 ============
section("1", "实验概览")
body("本周授课内容为「Packaging and Shipping Code」「智能体编程」「不止于代码」"
     "「Python 与 PyTorch」，对应四道实验题：q09 用 pyproject.toml + src 布局把"
     "最小问候包 greetlab 构建成 wheel 并在干净 venv 中安装运行；q10 让编程智能体"
     "进入「失败测试 -> 修复 -> 复跑」的可验证循环；q11 把三段质量较差的协作材料"
     "重写为可执行信息；q12 补全 PyTorch 线性回归训练循环并验证收敛。")
code("q09  打包与交付        pyproject.toml / build / venv   greetlab_*.whl\n"
     "q10  智能体编程        pytest / 编程智能体            tests/、ai_log.md\n"
     "q11  不止于代码        Markdown 协作规范              communication.md\n"
     "q12  Python 与 PyTorch  torch / nn.Linear / SGD        train.py")
body("报告每个实验按「任务说明 -> 操作步骤 -> 运行结果 -> 要点」组织；"
     "以下终端截图均来自 Ubuntu 22.04 虚拟机（/system_dev_exp 目录、bash 提示符、"
     "Python 3.10），为个人实际执行的真实运行结果。")

# ============ 2 第 9 题 ============
section("2", "第 9 题：从源码构建并在干净环境安装 Wheel")
sub("任务说明")
body("在 q09 中创建最小 Python 命令行包 greetlab，用 python3 -m build 从源码生成 "
     "wheel；新建干净虚拟环境，仅从 wheel 安装（不联网），并切换到 q09 之外运行 "
     "sdt-greet --name <学号> 验证输出。")
sub("操作步骤")
body("1) 创建 src 布局：mkdir -p src/greetlab，并写入 __init__.py、cli.py 与 "
     "pyproject.toml，把「学号」替换为 24070030103。")
img("q09_img0_src.png", "q09：创建 src 布局（__init__.py / cli.py / pyproject.toml）")
code("[build-system]\nrequires = [\"setuptools>=68\"]\nbuild-backend = \"setuptools.build_meta\"\n\n"
     "[project]\nname = \"greetlab-24070030103\"\nversion = \"0.1.0\"\nrequires-python = \">=3.9\"\n\n"
     "[project.scripts]\nsdt-greet = \"greetlab.cli:main\"\n\n"
     "[tool.setuptools.packages.find]\nwhere = [\"src\"]")
body("其中 [project.scripts] 把 sdt-greet 命令映射到 greetlab.cli:main，是安装后能直接调用的关键。")
body("2) 运行 python3 -m build 生成 wheel：")
code("$ cd q09\n$ python3 -m build\n...\nSuccessfully built greetlab_24070030103-0.1.0.tar.gz\n"
     "  and greetlab_24070030103-0.1.0-py3-none-any.whl")
img("q09_img1_build.png", "q09：python3 -m build 一次产出 sdist 与 wheel")
body("3) 新建干净 venv，仅从 wheel 安装（--no-index 关闭 PyPI，--find-links 只查本地）：")
code("$ python3 -m venv clean-venv\n"
     "$ ./clean-venv/bin/pip3 install --no-index --find-links dist greetlab-24070030103\n"
     "Looking in links: dist\nSuccessfully installed greetlab-24070030103-0.1.0")
img("q09_img2_install.png", "q09：全新 venv 仅从本地 dist 安装，中断联网")
body("4) 切换到 q09 之外运行：")
code("$ cd ..\n$ ./q09/clean-venv/bin/sdt-greet --name 24070030103\nHello, 24070030103!\n"
     "$ ./q09/clean-venv/bin/sdt-greet --name 朱英俊\nHello, 朱英俊!")
img("q09_img3_run.png", "q09：在 q09 之外调用已装命令，中文姓名同样正确")
body("5) 用 pip3 show 核对信息（Version 0.1.0、Requires 为空、位于 site-packages）：")
img("q09_img4_pipshow.png", "q09：pip3 show 核对已安装包信息")
sub("运行结果")
body("build 同时产出 sdist(.tar.gz) 与 wheel(.whl，py3-none-any 表示纯 Python 跨平台)；"
     "干净 venv 安装成功，pip show 显示 Version: 0.1.0 且 Requires 为空；在 q09 之外运行"
     " sdt-greet --name 24070030103 得到 Hello, 24070030103!。")
sub("要点")
bullet("src 布局 + packages.find where=[\"src\"] 是现代 Python 打包推荐结构。")
bullet("--no-index --find-links dist 是「仅从 wheel 安装」的关键，证明不依赖源码。")
bullet("在 q09 之外运行脚本，验证的是「已装进 venv 的命令」而非本地源码。")

# ============ 3 第 10 题 ============
section("3", "第 10 题：让编程智能体进入可验证的修复循环")
sub("任务说明")
body("复制 q09 为 q10，添加先失败的测试：--name 只含空白字符时 main 应以 "
     "SystemExit(2) 结束；向智能体说明目标、约束与测试命令，要求它修改实现并复跑；"
     "人工检查 diff、撤销无关修改并复跑，把记录写入 ai_log.md（<=5 行）。")
sub("操作步骤")
body("1) cp -r q09/* q10/ 复制源码，mkdir tests 并写 tests/test_cli.py：")
code("cp -r q09/* q10/\ncd q10\nmkdir tests\ncat > tests/test_cli.py\n"
     "def test_blank_name_exits_code_2(monkeypatch):\n"
     "    monkeypatch.setattr(\"sys.argv\", [\"sdt-greet\", \"--name\", \"   \"])\n"
     "    with pytest.raises(SystemExit) as excinfo:\n"
     "        main()\n"
     "    assert excinfo.value.code == 2")
img("q10_img0_testfile.png", "q10：复制源码并创建失败测试 tests/test_cli.py")
body("2) 先跑测试确认失败（红灯）：")
code("$ PYTHONPATH=src pytest tests/test_cli.py -v\n"
     "test_blank_name_exits_code_2 FAILED\n"
     "Failed: DID NOT RAISE SystemExit\n"
     "Captured stdout: Hello,    !")
img("q10_img1_fail.png", "q10：空白姓名用例失败 DID NOT RAISE SystemExit")
body("3) 向智能体说明「目标：空白姓名退出码 2；约束：保留 argparse、用 p.error 退出；"
     "测试命令：上面的 pytest」。智能体新增两行校验：")
code("a = p.parse_args()\nif not a.name.strip():\n    p.error(\"--name 不能只含空白字符\")\nprint(f\"Hello, {a.name}!\")")
body("4) 人工 git diff 确认仅 +2 行、无无关改动，复跑测试（绿灯）：")
code("$ PYTHONPATH=src pytest tests/test_cli.py -v\ntest_blank_name_exits_code_2 PASSED\n1 passed")
img("q10_img2_pass.png", "q10：智能体修改后的 cli.py 与复跑结果 1 passed")
body("5) 用 cat 写入并回显 ai_log.md（5 行）：")
img("q10_img3_ailog.png", "q10：git diff 确认改动范围，ai_log.md 共 5 行")
sub("要点")
bullet("「可验证循环」= 红灯测试 -> 明确契约 -> 智能体改码 -> 人工 diff 审查 -> 绿灯。")
bullet("argparse 的 p.error(msg) 会抛 SystemExit(2)，是参数校验的标准退出方式。")

# ============ 4 第 11 题 ============
section("4", "第 11 题：把协作材料改成可执行信息")
sub("任务说明")
body("围绕「空姓名仍输出问候语」缺陷，把 Issue / 提交信息 / 评审意见三段材料重写为"
     "可执行信息写入 communication.md，全文 <=400 字。")
sub("改写前 vs 改写后")
code("改写前：\nIssue：Windows 上运行不了，尽快修复。\n提交信息：fix bug\n评审意见：这里写得不好，重写。")
code("改写后（节选）：\n"
     "Issue 标题：sdt-greet --name \" \" 对空白姓名仍输出问候语并以 0 退出\n"
     "环境：Windows（版本待确认）；greetlab-24070030103 v0.1.0；Python 待确认\n"
     "复现命令：sdt-greet --name \" \"\n"
     "期望结果：以 SystemExit(2) 结束，不输出问候语\n"
     "实际结果：输出 Hello, !，退出码 0\n\n"
     "提交信息：fix: 空白姓名改为报错退出，而非输出问候语\n"
     "正文：--name 传入纯空白时仍打印 Hello, ! 并返回 0。新增 strip 校验使其以 2 退出\n\n"
     "评审意见：\n"
     "Blocking：cli.py 缺少空白姓名校验，会输出无意义 Hello, ! 且退出码 0 误判成功\n"
     "Nit：可在 --name 的 help 文本补充「不可为空或纯空白」说明")
img("q11_img1_comm.png", "q11：写入并回显 communication.md（Issue / 提交信息 / 评审意见）")
sub("要点")
bullet("可执行的 Issue 必须有复现命令与期望/实际结果；未知信息标注「待确认」。")
bullet("提交信息用祈使语气 + Conventional Commits；评审意见用 Blocking/Suggestion/Nit 分级。")

# ============ 5 第 12 题 ============
section("5", "第 12 题：修复一个可复现的线性回归训练循环")
sub("任务说明")
body("补全 train.py 的训练循环 TODO：正确调用 zero_grad / backward / step；训练后 "
     "model.eval() + torch.no_grad() 打印最终损失、weight、bias。要求损失 < 0.001，"
     "且不得把 weight/bias 直接赋值为 3 和 -1。")
sub("操作步骤")
body("数据 y = 3x - 1（linspace(-1, 1, 100)），模型 nn.Linear(1,1)，损失 MSE，"
     "优化器 SGD(lr=0.1)，训练 200 轮。完整 train.py 如下：")
img("q12_img0_src.png", "q12：cat 写入完整 train.py（补全训练循环 + 评估打印）")
code("import torch\nimport torch.nn as nn\n"
     "x = torch.linspace(-1, 1, 100).reshape(-1, 1)\n"
     "y = 3 * x - 1\n"
     "model = nn.Linear(1, 1)\n"
     "loss_fn = nn.MSELoss()\n"
     "opt = torch.optim.SGD(model.parameters(), lr=0.1)\n"
     "for _ in range(200):\n"
     "    pred = model(x)\n"
     "    loss = loss_fn(pred, y)\n"
     "    opt.zero_grad(); loss.backward(); opt.step()\n"
     "model.eval()\nwith torch.no_grad():\n"
     "    pred = model(x); final_loss = loss_fn(pred, y)\n"
     "print(f\"final loss = {final_loss.item():.6f}\")\n"
     "print(f\"weight = {model.weight.item():.6f}, bias = {model.bias.item():.6f}\")")
sub("运行结果")
code("$ python3 train.py\n"
     "UserWarning: Failed to initialize NumPy: No module named 'numpy' ...\n"
     "final loss = 0.000000\n"
     "weight = 2.999997, bias = -1.000000")
img("q12_img1_train.png", "q12：python3 train.py 输出 final loss = 0.000000")
body("最终损失 < 0.001，weight 收敛到 2.999997、bias 收敛到 -1.000000，与生成式 "
     "y = 3x - 1 一致；运行时先出现一条 NumPy 可选依赖缺失的 UserWarning，不影响 CPU "
     "上的线性回归收敛。")
sub("要点")
bullet("训练循环五要素：zero_grad / backward / step / eval / no_grad，缺一不可。")
bullet("torch.manual_seed 固定随机种子，保证可复现。")

# ============ 6 课后练习 ============
section("6", "课后练习与解题感悟（14 个实例）")
exercises = [
    ("练习1 查看 wheel 内部结构", "python -m zipfile -l dist/*.whl 列出代码、METADATA、entry_points.txt、RECORD，wheel 本质是带元数据的 zip。"),
    ("练习2 sdist 与 wheel 产物差异", "python -m build 一次产出 .whl 与 .tar.gz，前者可直装、后者需再构建。"),
    ("练习3 editable 与 wheel 安装区别", "pip install -e . 开发态即时生效；pip install dist/*.whl 安装固定快照。"),
    ("练习4 pyproject 入口点脚本", "sdt-greet --help 显示 usage: sdt-greet [-h] --name NAME，入口点让包变成命令。"),
    ("练习5 修复循环提示词模板", "目标/约束/测试命令 三要素显式化验收标准，是智能体可验证的关键。"),
    ("练习6 git diff 审查智能体改动", "git diff 显示智能体只新增两行校验，无无关改动。"),
    ("练习7 撤销无关修改", "git restore 精确回滚单文件，审查后选择性回滚是标准动作。"),
    ("练习8 Conventional Commits", "fix: / feat(scope): 格式让提交历史可读、可筛选、可生成 CHANGELOG。"),
    ("练习9 结构化 Issue 模板", "环境/复现/期望/实际 四要素，缺失复现步骤的缺陷报告约等于无效。"),
    ("练习10 祈使语气提交信息", "标题说明做了什么，正文补充动机与方案，面向未来读历史的人。"),
    ("练习11 Review 分级标注", "Blocking 必须改 / Suggestion 建议改 / Nit 可选改，让作者分清优先级。"),
    ("练习12 张量基础运算", "torch.linspace(-1,1,5) 得到 5 个等间距点，shape=[5]、dtype=float32，reshape 只改形状。"),
    ("练习13 训练循环五要素拆解", "zero_grad 防梯度累加、backward 求导、step 更新、eval 评估态、no_grad 免梯度。"),
    ("练习14 no_grad 梯度追踪对比", "a.grad = tensor(4.)（d(a^2)/da）；no_grad 内 requires_grad=False，不建计算图。"),
]
for name, desc in exercises:
    pdf.set_font("hei", "", 10.5)
    pdf.set_text_color(*SUB)
    pdf.cell(EPW, 6, name, ln=1)
    pdf.set_text_color(40, 40, 50)
    pdf.set_font("hei", "", 10)
    pdf.multi_cell(EPW, 5.5, desc)
    pdf.ln(1)
sub("感悟小结")
body("14 个练习把四章内容织成一张网：Packaging 打通「源码 -> wheel -> 干净安装 -> 入口点"
     "调用」交付链路；智能体编程强调「可验证循环」；不止于代码把 Issue/提交信息/评审升维成"
     "可执行协作规范；PyTorch 用最小线性回归跑通训练五要素。最深体会：交付、协作、训练三者"
     "殊途同归，都要「可复现、可验证、可审查」。")

# ============ 7 版本控制 ============
section("7", "版本控制与提交记录")
sub("仓库地址")
body("GitHub：https://github.com/yingjunzhu520/system-tools-hamesome-3")
sub("提交记录（分次提交，非全量）")
body("本地仓库按「初始化模板 -> q09 -> q10 -> q11 -> q12 -> 截图脚本 -> 报告 -> "
     "README -> 提交记录截图」的顺序分次提交，每步均为增量修改。详见报告正文的 "
     "git log --oneline 输出与 commit_screenshot.png。")

# ============ 8 小结 ============
section("8", "小结")
body("本周四题覆盖「打包交付 / 智能体编程 / 协作规范 / PyTorch」四条主线：q09 走通 "
     "src + pyproject + build 的完整打包链路；q10 跑通「失败测试 -> 智能体修复 -> diff 审查"
     " -> 复跑」的可验证循环；q11 把协作材料重写为可执行信息；q12 补全训练循环五要素并验证"
     "损失 < 0.001。课后 14 个练习进一步把四章内容系统化。")

pdf.output(os.path.join(BASE, "report_with_images.pdf"))
print("saved report_with_images.pdf")
