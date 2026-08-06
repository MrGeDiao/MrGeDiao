#!/usr/bin/env python3
"""重绘 assets/svg/star-growth.svg：按 Signal Index 设计生成 shuorenhua 的 star 累计增长曲线。

用法：python3 scripts/gen-star-growth.py   （依赖已登录的 gh CLI 或 GH_TOKEN）
历史逐日累计存在 data/star-history.json，每次运行只读一次 stargazers_count 补上当天。
"""
import json
import math
import subprocess
from datetime import date
from pathlib import Path

REPO = "MrGeDiao/shuorenhua"
HISTORY = Path(__file__).resolve().parent.parent / "data" / "star-history.json"
OPEN_DATE = date(2026, 3, 22)  # 开源日
EVENTS = [(date(2026, 6, 18), "v1.9 · Eval Harness")]  # 曲线上的发版标注

# Signal Index tokens
PANEL, BORDER = "#F7F8F5", "#D7DCE2"
INK, MUTED = "#101318", "#929AA5"
GRID, BASELINE = "#E5E8EC", "#AEB5BF"
ACCENT = "#246BFD"

X0, X1, Y0, PLOT_H = 88, 1150, 340, 210  # 绘图区
SANS = "-apple-system, 'SF Pro Text', 'PingFang SC', 'Segoe UI', 'Microsoft YaHei', sans-serif"
MONO = "ui-monospace, 'SF Mono', 'JetBrains Mono', monospace"


def load_history():
    """读逐日累计存档，用当前 stargazers_count 补上今天这条，回写后返回。

    stargazers 列表端点（REST 和 GraphQL 都一样）对 Actions 自带的 GITHUB_TOKEN
    一律拒绝——它的作用域只覆盖本仓库，读不了 shuorenhua，匿名也不放行。
    仓库自身的 stargazers_count 权限低，自带 token 就能读，所以历史时间戳一次性
    存档，日常只增量追加当天总数。
    """
    data = json.loads(HISTORY.read_text(encoding="utf-8"))
    total = int(subprocess.run(
        ["gh", "api", f"repos/{REPO}", "--jq", ".stargazers_count"],
        stdout=subprocess.PIPE, text=True, check=True).stdout.strip())

    data["cumulative"][date.today().isoformat()] = total
    data["cumulative"] = dict(sorted(data["cumulative"].items()))
    HISTORY.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return {date.fromisoformat(d): v for d, v in data["cumulative"].items()}


def main():
    cum_at = load_history()
    today = date.today()
    span = (today - OPEN_DATE).days

    def xs(d): return X0 + (d - OPEN_DATE).days / span * (X1 - X0)

    total = cum_at[max(cum_at)]
    ymax = math.ceil(total * 1.06 / 20) * 20

    def ys(v): return Y0 - v * PLOT_H / ymax

    pts = [(xs(OPEN_DATE), ys(0))] + [(xs(d), ys(cum_at[d])) for d in sorted(cum_at)]
    line = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    area = line + f" L{X1},{Y0} L{X0},{Y0} Z"
    end_x, end_y = pts[-1]

    gridlines, ylabels = [], []
    for v in range(200, ymax, 200):
        y = ys(v)
        gridlines.append(f'<line x1="{X0}" y1="{y:.1f}" x2="{X1}" y2="{y:.1f}"/>')
        ylabels.append(f'<text x="{X0-10}" y="{y+4:.1f}">{v}</text>')

    xticks = [f'<text x="{X0}" y="365" text-anchor="start">{OPEN_DATE.month}月{OPEN_DATE.day}日</text>']
    m = OPEN_DATE.month % 12 + 1
    year = OPEN_DATE.year + (OPEN_DATE.month == 12)
    while date(year, m, 1) <= today:
        xticks.append(f'<text x="{xs(date(year, m, 1)):.1f}" y="365">{m}月</text>')
        year, m = (year + 1, 1) if m == 12 else (year, m + 1)

    events_svg = []
    for ev_date, label in EVENTS:
        cum_v = max((c for d, c in cum_at.items() if d <= ev_date), default=0)
        ex, ey = xs(ev_date), ys(cum_v)
        events_svg.append(
            f'<line x1="{ex:.1f}" y1="{ey+6:.1f}" x2="{ex:.1f}" y2="{Y0}" stroke="{BASELINE}" stroke-width="1" stroke-dasharray="2 5"/>\n'
            f'  <circle cx="{ex:.1f}" cy="{ey:.1f}" r="3.5" fill="{INK}" stroke="{PANEL}" stroke-width="2"/>\n'
            f'  <text x="{ex-10:.1f}" y="{ey-15:.1f}" font-family="{SANS}" font-size="12" fill="{MUTED}" text-anchor="end">{label}</text>')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="390" viewBox="0 0 1200 390" role="img" aria-label="说人话 star 增长曲线：开源 {span} 天，0 到 {total} stars，数据截至 {today}">
  <rect x="1" y="1" width="1198" height="388" fill="{PANEL}" stroke="{BORDER}" stroke-width="1.5"/>
  <rect x="1" y="1" width="1198" height="4" fill="{ACCENT}"/>

  <text x="40" y="37" font-family="{MONO}" font-size="11.5" letter-spacing="1" fill="{ACCENT}">SIGNAL GROWTH / GITHUB</text>
  <text x="40" y="73" font-family="{SANS}" font-size="25" font-weight="700" fill="{INK}">「说人话」star 增长</text>
  <text x="40" y="98" font-family="{MONO}" font-size="12.5" fill="{MUTED}">开源 {span} 天 · 0 → {total} · 数据截至 {today}</text>
  <text x="1150" y="75" font-family="{MONO}" font-size="43" font-weight="700" fill="{ACCENT}" text-anchor="end">{total}</text>
  <text x="1150" y="98" font-family="{MONO}" font-size="11.5" letter-spacing="1" fill="{MUTED}" text-anchor="end">STARGAZERS</text>
  <line x1="40" y1="112" x2="1160" y2="112" stroke="{BORDER}" stroke-width="1"/>

  <g stroke="{GRID}" stroke-width="1">
    {''.join(gridlines)}
    <line x1="{X0}" y1="{Y0}" x2="{X1}" y2="{Y0}" stroke="{BASELINE}" stroke-width="1.5"/>
  </g>
  <g font-family="{MONO}" font-size="11.5" fill="{MUTED}" text-anchor="end">
    {''.join(ylabels)}
  </g>
  <g font-family="{MONO}" font-size="11.5" fill="{MUTED}" text-anchor="middle">
    {''.join(xticks)}
  </g>

  <path d="{area}" fill="{ACCENT}" fill-opacity="0.06"/>
  <path d="{line}" fill="none" stroke="{ACCENT}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>

  {''.join(events_svg)}

  <circle cx="{end_x:.1f}" cy="{end_y:.1f}" r="4.5" fill="{ACCENT}" stroke="{PANEL}" stroke-width="2"/>
  <text x="{end_x-12:.1f}" y="{end_y-10:.1f}" font-family="{SANS}" font-size="14" font-weight="700" fill="{INK}" text-anchor="end">最新</text>
</svg>
'''
    out = Path(__file__).resolve().parent.parent / "assets" / "svg" / "star-growth.svg"
    out.write_text(svg, encoding="utf-8")
    print(f"written {out} — {total} stars, {span} days, ymax {ymax}")


if __name__ == "__main__":
    main()
