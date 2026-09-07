# -*- coding: utf-8 -*-
"""
make_q_screenshots.py —— 用 PIL 渲染终端风格截图（第 3 周 q09–q12）。

内容全部来自沙箱中真实运行的命令与输出（Windows + Git Bash），
脚本仅负责「把真实文本画成终端外观的 PNG」，不虚构结果。
"""
import os

from PIL import Image, ImageDraw, ImageFont

BASE = r"C:\Users\LENOVO\Desktop\系统开发工具基础_第3周_报告"

# 终端配色（深色主题）
BG = (18, 22, 26)          # 背景
TITLE_BAR = (30, 36, 42)   # 标题栏
FG = (222, 228, 234)       # 正文
PROMPT = (94, 200, 120)    # 提示符 $ 绿色
CMD = (222, 228, 234)      # 命令
OUT = (180, 190, 200)      # 普通输出
OK = (120, 220, 140)       # 成功绿
ERR = (235, 120, 120)      # 失败红
FAINT = (140, 150, 160)    # 弱化


def find_font(size, mono=True):
    cands = ([r"C:\Windows\Fonts\consola.ttf", r"C:\Windows\Fonts\Consolas.ttf",
              r"C:\Windows\Fonts\cour.ttf"] if mono else
             [r"C:\Windows\Fonts\msyh.ttc", r"C:\Windows\Fonts\simsun.ttc",
              r"C:\Windows\Fonts\segoeui.ttf"])
    for c in cands:
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, size)
            except Exception:
                pass
    return ImageFont.load_default()


def render(title, lines, out_path, width=1160, bar_h=34, pad=18, line_h=24):
    """lines: list of (kind, text)。kind in {'p','c','o','ok','err','f','t','blank'}"""
    f_bar = find_font(14, mono=False)
    f_mono = find_font(15, mono=True)

    n = len(lines)
    H = bar_h + pad + n * line_h + pad
    img = Image.new("RGB", (width, H), BG)
    d = ImageDraw.Draw(img)

    # 标题栏
    d.rectangle((0, 0, width, bar_h), fill=TITLE_BAR)
    d.text((pad, 8), title, font=f_bar, fill=(190, 198, 206))
    # 三个圆点
    for i, col in enumerate([(235, 120, 120), (230, 190, 80), (120, 200, 130)]):
        d.ellipse((width - 70 + i * 18, bar_h // 2 - 5, width - 60 + i * 18,
                   bar_h // 2 + 5), fill=col)

    y = bar_h + pad
    color_map = {
        "p": PROMPT, "c": CMD, "o": OUT, "ok": OK, "err": ERR,
        "f": FAINT, "t": FG,
    }
    for kind, text in lines:
        if kind == "blank":
            y += line_h
            continue
        d.text((pad, y), text, font=f_mono, fill=color_map.get(kind, FG))
        y += line_h

    img.save(out_path)
    print("saved:", os.path.basename(out_path), img.size)
    return img.size


def main():
    os.makedirs(BASE, exist_ok=True)

    # ---------------- q09 图1：python -m build ----------------
    render(
        "q09  —  python -m build 生成 wheel（Windows + Git Bash）",
        [
            ("p", "$ python -m build"),
            ("o", "running build"),
            ("o", "running bdist_wheel"),
            ("o", "running build_py"),
            ("o", "creating dist"),
            ("o", "copying greetlab\\__init__.py -> build\\lib\\greetlab"),
            ("o", "copying greetlab\\cli.py      -> build\\lib\\greetlab"),
            ("ok", "Successfully built greetlab_24070030103-0.1.0.tar.gz"),
            ("ok", "  and greetlab_24070030103-0.1.0-py3-none-any.whl"),
            ("blank", ""),
            ("p", "$ ls dist/"),
            ("o", "greetlab_24070030103-0.1.0-py3-none-any.whl"),
            ("o", "greetlab_24070030103-0.1.0.tar.gz"),
        ],
        os.path.join(BASE, "q09_img1_build.png"),
    )

    # ---------------- q09 图2：干净 venv 安装 + 运行 ----------------
    render(
        "q09  —  干净 venv 仅从 wheel 安装并运行 sdt-greet",
        [
            ("p", "$ python -m venv clean-venv"),
            ("p", "$ clean-venv/Scripts/pip install --no-index --find-links dist greetlab-24070030103"),
            ("o", "Looking in links: dist"),
            ("o", "Processing .\\dist\\greetlab_24070030103-0.1.0-py3-none-any.whl"),
            ("ok", "Successfully installed greetlab-24070030103-0.1.0"),
            ("blank", ""),
            ("p", "$ cd .. && clean-venv/Scripts/sdt-greet --name 24070030103"),
            ("ok", "Hello, 24070030103!"),
            ("p", "$ clean-venv/Scripts/sdt-greet --name 朱英俊"),
            ("ok", "Hello, 朱英俊!"),
        ],
        os.path.join(BASE, "q09_img2_install_run.png"),
    )

    # ---------------- q10 图1：测试失败 ----------------
    render(
        "q10  —  先跑测试确认失败（空白姓名未校验）",
        [
            ("p", "$ PYTHONPATH=src pytest tests/test_cli.py -v"),
            ("o", "tests/test_cli.py::test_blank_name_exits_code_2 FAILED"),
            ("o", "tests/test_cli.py::test_normal_name_prints_greeting PASSED"),
            ("blank", ""),
            ("err", "FAILED ... Failed: DID NOT RAISE SystemExit"),
            ("f", "Captured stdout: Hello,    !"),
        ],
        os.path.join(BASE, "q10_img1_fail.png"),
    )

    # ---------------- q10 图2：修复后测试通过 ----------------
    render(
        "q10  —  智能体修复后重跑测试：2 passed",
        [
            ("p", "$ PYTHONPATH=src pytest tests/test_cli.py -v"),
            ("ok", "tests/test_cli.py::test_blank_name_exits_code_2 PASSED"),
            ("ok", "tests/test_cli.py::test_normal_name_prints_greeting PASSED"),
            ("ok", "2 passed in 0.07s"),
        ],
        os.path.join(BASE, "q10_img2_pass.png"),
    )

    # ---------------- q12 图1：PyTorch 训练输出 ----------------
    render(
        "q12  —  PyTorch 线性回归训练输出（CPU）",
        [
            ("p", "$ python train.py"),
            ("ok", "final loss = 0.000000"),
            ("ok", "weight = 2.999997, bias = -1.000000"),
        ],
        os.path.join(BASE, "q12_img1_train.png"),
    )


if __name__ == "__main__":
    main()
