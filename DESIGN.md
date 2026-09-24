# MrGeDiao Profile — Signal Index

## 1. Purpose

这是一个个人 GitHub 首页，先介绍人，再介绍项目。访客应在第一屏看懂：作者是大厂产品经理出身，现在自己写代码做 AI 工具，也做企业 AI 落地咨询。代表作是「说人话」；其他项目（含 paper-reading-zh）只在矩阵里占一行。

2026-09-24 内容改版：视觉系统不变，页面结构从「项目陈列」改为「人 → 代表作 → 其他在做的 → 咨询」。

## 2. Visual Direction

方向：**独立研究所 / Signal Index**。

页面像一份仍在更新的研究索引：骨白底、石墨字、电蓝信号、清楚的编号和字段。它不是实验室复古档案，也不是开发者终端；视觉更接近现代技术索引和研究计划表。

核心特征：

- 大号身份标题 + 8/4 不对称首屏
- 电蓝索引号、字段名和数据线
- 横向研究记录：`PROBLEM / APPROACH / PROOF / PLATFORMS`
- 私有项目矩阵：`PURPOSE / METHOD / BOUNDARY`
- 方角、细线、无阴影、无渐变
- 内容密度高，但段落短、列宽明确

## 3. Tokens

| Token | Value | Role |
| --- | --- | --- |
| `canvas` | `#F7F8F5` | 页面与 SVG 主画布 |
| `surface` | `#FFFFFF` | 局部研究记录底色 |
| `ink` | `#101318` | 标题、主文案 |
| `body` | `#66707C` | 正文、说明 |
| `muted` | `#929AA5` | 次级标签、坐标、日期 |
| `line` | `#D7DCE2` | 网格、表格和分隔线 |
| `signal` | `#246BFD` | 全页唯一强调色 |
| `signal-soft` | `#E8F0FF` | 极少量蓝色弱底，只用于标签 |

禁止新增第二强调色。图标本身可以保留技术品牌原色，但不得把它们扩散为页面 UI 色。

## 4. Typography

- Sans：`-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'PingFang SC', 'Segoe UI', sans-serif`
- Mono：`ui-monospace, 'SF Mono', 'JetBrains Mono', 'Cascadia Code', monospace`
- 身份标题：sans 72–82px / 760，紧字距
- 主定位：sans 30–34px / 700
- 分区标题：sans 22–26px / 700
- 正文：sans 15–18px / 400–500
- 字段、索引、项目名、数据：mono 11–18px
- 不使用衬线体，不靠全大写长句制造气势
- SVG 不会替 CJK 文本自动换行；写入前先用「字号 × 字数」粗估宽度，再按实际渲染检查列边界和相邻元素

## 5. Layout

### Hero

- 1200px viewBox 下按 8/4 分栏：左侧身份、一句定位和三栏（背景 / 现在 / 咨询），右侧是「现在在做」四项清单加联系邮箱块。
- 顶部是 `SIGNAL INDEX / PERSONAL EDITION` 元数据行。
- 底部三栏使用真实 Tabler 图标：user、code、briefcase。
- 右栏只放页面上真实存在、可核实的内容，不放虚设字段，也不复述主标题。

### About

- 「关于我」两段正文，下接双栏表格：左侧 skillicons + 工具行，右侧「做事方式」面板（写清需求 → 自己写代码 → 测试验收 → 上线维护）。

### Flagship

- 只放「说人话」一条横向研究记录，不是圆角卡片。
- 左侧大号 `01`，右侧依次为项目、问题、做法、验证和平台。
- README 正文继续提供链接与动态 shields，不能只把文字封在图片里。

### Data

- star 曲线由脚本生成，曲线、终点和数字都用电蓝。
- 不放静态活动快照（会过期，且 GitHub 页面自带贡献图）。
- 一张图里只用一种视觉编码：高度就是高度，不再叠加透明度或格数表达同一个量。

- skillicons 只列实际用到的技术，不新增“熟练度”“百分比”或技术栈评分。

### Other Work

- 四个私有项目 + paper-reading-zh 使用统一矩阵（`PURPOSE / METHOD / BOUNDARY`），不做浮动卡。
- 每个项目至少写清用途、方法和边界；信息来自仓库事实，不写发布宣言。
- 允许公开私有项目名和设计取舍，不公开 secret、主机地址和内部敏感路径。

### Consulting

- 四步横向面板：看业务流程 → 选一个小场景 → 带团队上手 → 复盘；编号 + Tabler 图标 + 两行说明。

## 6. Icons & Assets

- 通用线性图标使用 Tabler Icons（MIT），不自行画风格不一致的图标。
- 技术品牌图标使用 skillicons.dev / Simple Icons 等真实来源。
- 不使用动物、显微镜等纯装饰插画；方案图中的此类元素不是实现目标。

## 7. Motion & Depth

- 全页静态，无 SMIL。
- 默认无阴影；层级靠背景、线、间距和字号。
- 默认方角；只有外部 shields 保持其自身形状。

## 8. Responsive & QA

- SVG 统一 1200px viewBox，缩放到 GitHub 约 900px 内容宽度时正文仍可读。
- 关键正文不小于 14px；表格列不得出现文字互相覆盖。
- 视觉改动必须同时检查：选中稿、900px SVG 渲染、整页预览。
- QA 固定看五项：字体层级、列宽和节奏、颜色、图标来源、文案保真。

## 9. Avoid

- 朱砂、暖纸、印章、宋体、杂志封面语汇
- 深色终端、黑底代码卡、霓虹或发光
- 渐变、玻璃、阴影、圆角卡片堆
- 空泛口号、AI 宣传腔、为完整而凑出的指标
