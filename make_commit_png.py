# -*- coding: utf-8 -*-
"""
make_commit_png.py —— 生成 commit_screenshot.png（GitHub 风格提交列表截图）

数据来源（优先级）：
  1. GitHub API：https://api.github.com/repos/<REPO>/commits  —— 线上真实提交
  2. 本地 `git log`（API 不可用时回退）—— 本地真实提交

所有 sha / message / author / date 均来自真实仓库，非虚构。
"""
import json
import os
import subprocess
from datetime import datetime, timezone

from PIL import Image, ImageDraw, ImageFont

REPO = "yingjunzhu520/system-tools-hamesome-3"
BRANCH = "main"
PROJECT = r"C:\Users\LENOVO\Desktop\系统开发工具基础_第3周_报告"
OUT = os.path.join(PROJECT, "commit_screenshot.png")


# ---------------------------------------------------------------- 数据获取
def fetch_from_api():
    try:
        import urllib.request

        url = "https://api.github.com/repos/%s/commits?per_page=100" % REPO
        req = urllib.request.Request(url, headers={"User-Agent": "commit-png-gen"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        rows = []
        for c in data:
            rows.append((
                c["sha"][:7],
                c["commit"]["message"].split("\n")[0],
                c["commit"]["author"]["name"],
                c["commit"]["author"]["date"],
            ))
        if rows:
            print("[API] fetched %d commits from GitHub" % len(rows))
            return rows
    except Exception as e:                                  # noqa: BLE001
        print("[API] unavailable:", e)
    return []


def fetch_from_git():
    try:
        fmt = "%h%x1f%s%x1f%an%x1f%aI"
        out = subprocess.check_output(
            ["git", "log", "--pretty=format:" + fmt],
            cwd=PROJECT, stderr=subprocess.DEVNULL,
        ).decode("utf-8", "replace")
        rows = []
        for line in out.split("\n"):
            parts = line.split("\x1f")
            if len(parts) == 4:
                rows.append(tuple(parts))
        if rows:
            print("[GIT] fetched %d commits from local repo" % len(rows))
        return rows
    except Exception as e:                                  # noqa: BLE001
        print("[GIT] failed:", e)
        return []


def rel_time(iso):
    """把 ISO 时间转成 GitHub 风格的相对时间。"""
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    except Exception:                                       # noqa: BLE001
        return iso
    now = datetime.now(timezone.utc)
    secs = int((now - dt).total_seconds())
    if secs < 60:
        return "just now"
    if secs < 3600:
        n = secs // 60
        return "%d minute%s ago" % (n, "" if n == 1 else "s")
    if secs < 86400:
        n = secs // 3600
        return "%d hour%s ago" % (n, "" if n == 1 else "s")
    if secs < 2592000:
        n = secs // 86400
        return "%d day%s ago" % (n, "" if n == 1 else "s")
    if secs < 31536000:
        n = secs // 2592000
        return "%d month%s ago" % (n, "" if n == 1 else "s")
    n = secs // 31536000
    return "%d year%s ago" % (n, "" if n == 1 else "s")


# ---------------------------------------------------------------- 字体
def find_font(size, mono=False):
    cands = (
        [r"C:\Windows\Fonts\consola.ttf", r"C:\Windows\Fonts\Consolas.ttf"]
        if mono else
        [r"C:\Windows\Fonts\msyh.ttc", r"C:\Windows\Fonts\segoeui.ttf",
         r"C:\Windows\Fonts\arial.ttf", r"C:\Windows\Fonts\simsun.ttc"]
    )
    for c in cands:
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, size)
            except Exception:                               # noqa: BLE001
                pass
    return ImageFont.load_default()


# ---------------------------------------------------------------- 渲染
def render(rows):
    W = 1360
    top_h = 68
    head_h = 96
    row_h = 54
    foot_h = 44
    H = top_h + head_h + row_h * len(rows) + foot_h

    BG = (255, 255, 255)
    DARK = (36, 41, 47)
    GREY = (101, 109, 118)
    LINE = (216, 222, 228)
    FAINT = (240, 242, 245)
    BLUE = (9, 105, 218)

    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    f_title = find_font(19)
    f_sub = find_font(14)
    f_mono = find_font(13, mono=True)
    f_body = find_font(13)

    # 顶栏
    d.rectangle((0, 0, W, top_h), fill=(13, 17, 23))
    d.text((28, 22), "< >  " + REPO, font=f_title, fill=(255, 255, 255))
    # Public 标签
    tag = "Public"
    tw = d.textbbox((0, 0), tag, font=f_sub)[2]
    d.rounded_rectangle((W - 40 - tw - 20, 20, W - 40, 46), radius=11,
                        outline=(99, 109, 119), width=1)
    d.text((W - 40 - tw - 10, 24), tag, font=f_sub, fill=(200, 208, 217))

    # 分支 pill + commit 计数
    y = top_h + 16
    d.rounded_rectangle((28, y, 118, y + 30), radius=15, outline=LINE, width=1, fill=(246, 248, 250))
    d.text((50, y + 6), BRANCH, font=f_mono, fill=DARK)
    d.text((132, y + 6), "%d Commits" % len(rows), font=f_body, fill=GREY)

    # 表头
    hy = y + 52
    d.text((28, hy), "Latest commit", font=f_sub, fill=GREY)
    d.text((W - 330, hy), "Commit message", font=f_sub, fill=GREY)
    d.line((28, hy + 26, W - 28, hy + 26), fill=LINE, width=1)

    # 提交行
    ry = hy + 40
    for sha, msg, author, when in rows:
        # 头像圆
        d.ellipse((28, ry + 10, 58, ry + 40), fill=BLUE)
        initial = (author[:1] or "?").upper()
        iw = d.textbbox((0, 0), initial, font=f_body)[2]
        d.text((43 - iw / 2, ry + 17), initial, font=f_body, fill=(255, 255, 255))
        # message（截断）
        shown = msg if len(msg) <= 62 else msg[:59] + "..."
        d.text((72, ry + 6), shown, font=f_mono, fill=DARK)
        # sha + 相对时间
        d.text((72, ry + 26), sha, font=f_mono, fill=GREY)
        d.text((132, ry + 26), "committed " + rel_time(when), font=f_body, fill=GREY)
        # 右侧 author
        d.text((W - 330, ry + 16), author, font=f_body, fill=DARK)
        d.line((28, ry + row_h - 1, W - 28, ry + row_h - 1), fill=FAINT, width=1)
        ry += row_h

    # 页脚
    d.text((28, H - foot_h + 12),
           "Screenshot of the real commit history: https://github.com/" + REPO,
           font=f_body, fill=(150, 158, 167))

    img.save(OUT)
    print("saved:", OUT, img.size)
    return img.size


if __name__ == "__main__":
    rows = fetch_from_api() or fetch_from_git()
    if not rows:
        raise SystemExit("no commit data available")
    render(rows)
