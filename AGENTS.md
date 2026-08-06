# AGENTS.md — MrGeDiao/MrGeDiao

GitHub 个人首页仓库：`README.md` + `assets/svg/` 定制资源。当前视觉系统是 2026-07-13 定稿的「Signal Index / 独立研究所」。

## 设计系统（改动必须遵守）

设计系统单源在 `DESIGN.md`：tokens、字体、布局、图标来源、动效规则和 Avoid 清单都以它为准。改视觉前先读 `DESIGN.md`，本文件不重复维护设计值。

## 页面结构

banner → 自述两段 → 公开作品（两条研究记录 + shields）→ star 增长曲线 → 工具箱与 AI 工作流 → 私有研究项目矩阵 → 近 30 天活动与统计 → Email

## 维护点

- `assets/svg/star-growth.svg` 由 `.github/workflows/refresh-star-growth.yml` 每天 09:23（北京时间）自动重绘，星数有变化才提交（github-actions[bot] 名义），无需任何 secret。逐日累计存在 `data/star-history.json`，脚本每次只读一次 shuorenhua 的 `stargazers_count` 补上当天再重绘，SVG 和 JSON 一起提交。不要改回按 starredAt 拉 stargazers 列表：那个端点 REST 和 GraphQL 都拒绝 Actions 自带的 GITHUB_TOKEN（作用域只覆盖本仓库），匿名也不放行。本地手动刷新同样是 `python3 scripts/gen-star-growth.py`（依赖已登录的 gh CLI）。
- `assets/svg/recent-activity.svg` 是近 30 天静态快照。更新：`python3 scripts/gen-recent-activity.py`（依赖已登录的 gh CLI），脚本会拉贡献日历与提交涉及的仓库数并重绘活动信号和统计。
- shields 徽章实时，无需维护；paper-reading-zh 的 release 徽章必须带 `include_prereleases`，去掉会显示 invalid。
- skillicons.dev 使用 `theme=light`，不要改回默认主题。
- SVG 里 CJK 没有自动布局；修改中文标题或字段后要同步检查列宽、换行和 x 坐标。
- 改完 SVG 至少渲染一遍：`rsvg-convert -w 900 -b '#ffffff'`，再用整页 Chrome / 浏览器预览检查缩放后的可读性。
- `assets/svg/banner-top.svg`、两张公开项目卡和 `assets/svg/lab-notes.svg` 是同一套网格，改列宽时要一起核对。

## 文案

- 中文为主，过「说人话」标准：具体、直接、有作者判断，不写宣传腔、价值拔高或空总结。
- 第一屏说清作者是谁、做什么、关注哪些问题；公开项目说清问题、做法、验证和平台。
- paper-reading-zh 的覆盖平台固定为 Codex、Claude Code、Claude Project、ChatGPT Project 四个，不能漏 Claude Project。
- 私有项目可以公开用途、实现方法、设计取舍和明确边界；不要公开凭证、主机地址、内部敏感路径或没有核验的数据。
- 不写公司、任职和业务指标等简历级细节；联系邮箱：zcoeus@protonmail.com。

## 协作约定

- 以仓库所有者名义提交，commit message 用中文、`docs:` 前缀、不加 AI 署名。
- 涉及视觉的改动先出渲染预览给作者确认再 push；纯数据刷新可直接提交。
