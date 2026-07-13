#!/usr/bin/env python3
"""Generate assets/svg/recent-activity.svg from the owner's last 30 days on GitHub.

Usage: python3 scripts/gen-recent-activity.py  (requires an authenticated gh CLI)
"""

import json
import subprocess
from datetime import date, datetime, time, timedelta, timezone
from html import escape
from pathlib import Path


LOGIN = "MrGeDiao"
DAYS = 30

# Signal Index tokens
PANEL = "#F7F8F5"
INK, BODY, MUTED = "#101318", "#66707C", "#929AA5"
BORDER, GRID, ACCENT = "#D7DCE2", "#E5E8EC", "#246BFD"
SANS = "-apple-system, 'SF Pro Text', 'PingFang SC', 'Segoe UI', 'Microsoft YaHei', sans-serif"
MONO = "ui-monospace, 'SF Mono', 'JetBrains Mono', monospace"


def iso_utc(day: date) -> str:
    return datetime.combine(day, time.min, timezone.utc).isoformat().replace("+00:00", "Z")


def fetch_activity(start: date, end: date) -> dict:
    query = """
    query($login: String!, $from: DateTime!, $to: DateTime!) {
      user(login: $login) {
        contributionsCollection(from: $from, to: $to) {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays { date contributionCount }
            }
          }
          commitContributionsByRepository(maxRepositories: 100) {
            repository { name isPrivate }
            contributions { totalCount }
          }
        }
      }
    }
    """
    result = subprocess.run(
        [
            "gh", "api", "graphql",
            "-f", f"query={query}",
            "-F", f"login={LOGIN}",
            "-F", f"from={iso_utc(start)}",
            "-F", f"to={iso_utc(end + timedelta(days=1))}",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    payload = json.loads(result.stdout)
    return payload["data"]["user"]["contributionsCollection"]


def main() -> None:
    today = date.today()
    start = today - timedelta(days=DAYS - 1)
    collection = fetch_activity(start, today)
    calendar = collection["contributionCalendar"]

    counts = {
        date.fromisoformat(day["date"]): day["contributionCount"]
        for week in calendar["weeks"]
        for day in week["contributionDays"]
    }
    days = [(start + timedelta(days=index), counts.get(start + timedelta(days=index), 0)) for index in range(DAYS)]
    total = sum(count for _, count in days)
    active_days = sum(count > 0 for _, count in days)
    repositories = sum(item["contributions"]["totalCount"] > 0 for item in collection["commitContributionsByRepository"])
    peak = max((count for _, count in days), default=0)

    x0, step, bar_w = 84, 22, 11
    base_y, max_h = 180, 80
    chart_x1 = x0 + (DAYS - 1) * step + bar_w
    bars, labels = [], []
    for index, (day, count) in enumerate(days):
        x = x0 + index * step
        if count > 0:
            h = max(6.0, count / max(peak, 1) * max_h)
            bars.append(
                f'<rect x="{x}" y="{base_y - h:.1f}" width="{bar_w}" height="{h:.1f}" fill="{ACCENT}">'
                f"<title>{escape(day.isoformat())}: {count} contributions</title></rect>"
            )
        else:
            bars.append(
                f'<rect x="{x}" y="{base_y - 2}" width="{bar_w}" height="2" fill="{GRID}">'
                f"<title>{escape(day.isoformat())}: 0 contributions</title></rect>"
            )
        if index in {0, 6, 12, 18, 24, DAYS - 1}:
            labels.append(
                f'<text x="{x + bar_w / 2:.1f}" y="202" text-anchor="middle">{day.day}</text>'
            )

    stats = [
        ("Contributions", total, "M3 12h4l3 8l4 -16l3 8h4"),
        ("Active Days", active_days, "M4 5m0 2a2 2 0 0 1 2 -2h12a2 2 0 0 1 2 2v12a2 2 0 0 1 -2 2h-12a2 2 0 0 1 -2 -2z M16 3v4 M8 3v4 M4 11h16"),
        ("Repositories", repositories, "M4 4m0 2a2 2 0 0 1 2 -2h12a2 2 0 0 1 2 2v12a2 2 0 0 1 -2 2h-12a2 2 0 0 1 -2 -2z M8 9h8 M8 13h6"),
    ]
    stats_svg = []
    for index, (label, value, path) in enumerate(stats):
        y = 93 + index * 58
        stats_svg.append(
            f'<g transform="translate(850 {y - 18})" fill="none" stroke="{ACCENT}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
            f'<path d="{path}"/></g>'
            f'<text x="890" y="{y}" font-family="{SANS}" font-size="15" fill="{BODY}">{label}</text>'
            f'<text x="1130" y="{y}" font-family="{MONO}" font-size="24" font-weight="700" fill="{INK}" text-anchor="end">{value}</text>'
            f'<line x1="840" y1="{y + 18}" x2="1130" y2="{y + 18}" stroke="{BORDER}"/>'
        )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="280" viewBox="0 0 1200 280" role="img" aria-label="最近 {DAYS} 天 GitHub 活动：{total} 次贡献，{active_days} 个活跃日，涉及 {repositories} 个仓库，数据截至 {today}">
  <rect x="1" y="1" width="1198" height="278" fill="{PANEL}" stroke="{BORDER}" stroke-width="1.5"/>
  <rect x="1" y="1" width="1198" height="4" fill="{ACCENT}"/>

  <text x="40" y="39" font-family="{SANS}" font-size="24" font-weight="700" fill="{INK}">最近提交</text>
  <text x="165" y="38" font-family="{MONO}" font-size="11.5" letter-spacing="1" fill="{MUTED}">RECENT ACTIVITY / LAST {DAYS} DAYS</text>
  <text x="1130" y="38" font-family="{MONO}" font-size="11.5" fill="{MUTED}" text-anchor="end">数据截至 {today}</text>
  <line x1="40" y1="55" x2="1160" y2="55" stroke="{BORDER}"/>
  <line x1="800" y1="72" x2="800" y2="236" stroke="{BORDER}"/>

  <text x="40" y="92" font-family="{MONO}" font-size="11" letter-spacing=".8" fill="{ACCENT}">CONTRIBUTION SIGNAL</text>
  <line x1="{x0}" y1="{base_y - max_h}" x2="{chart_x1}" y2="{base_y - max_h}" stroke="{GRID}"/>
  <text x="{x0 - 8}" y="{base_y - max_h + 4}" font-family="{MONO}" font-size="10.5" fill="{MUTED}" text-anchor="end">{peak}</text>
  <g>{''.join(bars)}</g>
  <line x1="{x0}" y1="{base_y}" x2="{chart_x1}" y2="{base_y}" stroke="#AEB5BF" stroke-width="1.5"/>
  <g font-family="{MONO}" font-size="10.5" fill="{MUTED}">{''.join(labels)}</g>
  <text x="40" y="232" font-family="{MONO}" font-size="11" fill="{MUTED}">{start} → {today} · 柱高 = 当日贡献数</text>

  <text x="840" y="78" font-family="{MONO}" font-size="11" letter-spacing=".8" fill="{ACCENT}">PERIOD SUMMARY</text>
  <!-- Icons: Tabler Icons, MIT License -->
  {''.join(stats_svg)}
</svg>
'''
    output = Path(__file__).resolve().parent.parent / "assets" / "svg" / "recent-activity.svg"
    output.write_text(svg, encoding="utf-8")
    print(f"written {output} — {total} contributions, {active_days} active days, {repositories} repositories")


if __name__ == "__main__":
    main()
