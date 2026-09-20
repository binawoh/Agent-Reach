---
name: agent-reach
description: >
  搜索、调研和读取互联网内容时，按任务选择当前 Agent 的内置搜索、Exa 等外部搜索、
  平台专用通道、正文抓取或宿主浏览器工具。适用于网页/新闻/官方资料查询、URL 阅读、
  小红书/B站/Twitter/Reddit 等站内内容、视频字幕和 RSS。
  只负责获取与核验内容，不负责发帖、评论等写操作；已有专门平台 skill 时优先使用它。
metadata:
  homepage: https://github.com/binawoh/Agent-Reach
---

# Agent Reach — 互联网能力路由器

本 skill 负责选择和组合互联网工具，Exa 等只是其中的后端。先按任务选择能力，
再调用当前环境的公开接口；不把所有请求都交给同一个搜索引擎。

## 费用限制

只使用已确认免费或不会产生额外费用的能力；有 API key、余额或赠送额度不等于免费。
**TinyFish 仅允许免费范围内的 Search / Fetch；禁止调用 Agent、Agent Batch、Browser
或创建浏览器会话，包括 CLI、MCP、API 及其他 skill 的同等入口。** 不因 Fetch 失败、
已有赠送余额或用户泛称“用 TinyFish”就启用付费功能。无法确认费用或免费额度用尽时，
换已确认免费的通道；没有可用通道则说明缺口，不自动充值、升级或消费付费余额。

## 环境发现

本 skill 不绑定用户名、盘符、仓库目录或某一种 agent。先通过当前 skill 的实际位置、
当前会话暴露的内置搜索/网页读取/浏览器工具、已加载的 MCP 工具、命令发现
（如 `Get-Command` / `command -v`）及工具自身配置，确认可用能力和安装位置。
只发现当前任务需要的工具，不必先体检或配置全部后端；不得因宿主叫 Codex 或 Claude
就假定它有搜索权限。必要时可自行编写适配代码，遵守任务路由和凭据规则。
仓库附带的 `agent-search.ps1` 只是 PowerShell 参考实现；有合适的 MCP、CLI 或 API
可直接调用，不要求安装统一命令，也不因缺少固定目录而重新安装。
需要使用 Firecrawl CLI 时，未安装先安装，未认证先完成认证，验证通过后再搜索；具体见
[Firecrawl CLI 准备](references/search.md#firecrawl-cli-准备)。不要仅因缺少 CLI 就跳过该后端。

## 常驻规则（全程适用）

1. **动手前先体检**：多后端/登录态平台（小红书/Reddit/B站/Twitter/Facebook/Instagram/Boss直聘）先跑
   `agent-reach doctor --json`。`active_backend` 有值时按它选命令组；`active_backend: null`
   表示 Doctor 为避免触发浏览器 Cookie 读取或远端写入而没有做实时验证，不代表后端不存在。
   Doctor 结果是「某一时刻的快照」，通道/登录态可能已变化；执行只读命令前若怀疑失效，
   按对应 reference 的「体检与恢复」runbook 重新确认（如 career.md 的 Boss直聘 CDP 排查）。
2. **声明你在用什么**：开始干活前说一句「使用 agent-reach 的 X 平台 / Y 后端」。
3. **失败按 references 里的重试链处理**，不要瞎猜命令。
4. **按证据需要扩展**：全网调研先找原始资料；用户需要网友体验时再加入相关平台。
   证据足够即可结束，不为凑工具数量重复搜索。只返回旧资料、无关结果或首页链接时，
   即使命令成功，也要按 [搜索工具](references/search.md) 调整查询或换通道。
5. **个人版本维护**：沿用个人仓库每周上游同步；本机更新按
   [个人版本维护](references/personal-maintenance.md)。不在每次搜索后额外检查或安装更新。

## 路由表

| 用户意图 | 首选能力 | 详细文档 |
|---------|------|---------|
| 普通网页搜索、刚发布的新闻/公告 | 当前 Agent 内置搜索；缺失或结果不足时用外部搜索 | [search](references/search.md) |
| 官方原文、技术文档、财报深入补充 | Exa；必要时与内置搜索交叉核验 | [search](references/search.md) |
| 已知 URL、正文或表格 | 内置读取可满足时直接用；完整抓取优先 Firecrawl | [web](references/web.md) |
| 展开/翻页/交互后才能读到内容 | 宿主已有且不额外收费的浏览器工具 | [web](references/web.md) |
| 小红书/推特/B站/V2EX/Reddit/Facebook/Instagram 站内内容 | 对应平台通道 | [social](references/social.md) |
| 招聘/职位/LinkedIn/Boss直聘 | 对应平台通道 | [career](references/career.md) |
| 精确查 GitHub 仓库/代码 | GitHub 工具 | [dev](references/dev.md) |
| YouTube/B站/播客字幕 | 字幕或转录通道 | [video](references/video.md) |
| 雪球/股票行情 | 对应行情或站内通道 | [finance](references/finance.md) |
| RSS | feedparser | [web](references/web.md) |

用户指定工具时优先执行指定工具；遇到不可用或结果不足，说明原因再补充其他来源，
不得把备用结果冒充指定工具结果。Tavily 是外部搜索补充，Firecrawl Search 和 TinyFish
Search 也可按需使用；这些搜索入口不等于正文抓取或浏览器 Agent。

## 常用命令（先按上表选工具）

```bash
# 可选 PowerShell 外部搜索助手：明确指定任务所需后端
agent-search -Query "query" -Limit 5 -Provider exa

# 指定后端（也支持 exa、tavily、firecrawl）
agent-search -Query "query" -Limit 5 -Provider tinyfish

# 抓取正文（先按 search.md 完成 CLI 安装与认证）
firecrawl scrape "https://example.com/article" --format markdown --only-main-content

# GitHub 搜索
gh search repos "query" --sort stars --limit 10

# YouTube 字幕（注意：B站不要用 yt-dlp，失败重试链见 video.md）
yt-dlp --write-sub --write-auto-sub --skip-download -o "/tmp/%(id)s" "URL"

# V2EX 热门
curl -s "https://www.v2ex.com/api/topics/hot.json" -H "User-Agent: agent-reach/1.0"

# B站搜索（bili-cli，无需登录）
bili search "query" --type video -n 5
```

## 需登录态的平台（按 doctor 的 active_backend 选命令）

Twitter 注意：`agent-reach configure twitter-cookies` 保存的 Cookie 只供
`doctor` 检查配置是否齐全；`doctor` 不执行 `twitter status`，也不会设置当前
Shell。直接运行 `twitter` 前，必须在子进程环境中显式提供
`TWITTER_AUTH_TOKEN` 和 `TWITTER_CT0`，不得在日志或命令回显中暴露值。

小红书注意：Agent Reach 不替用户登录，也不读取浏览器 Cookie。OpenCLI 只用
用户已有且明确控制的 Chrome 会话；没有现成会话时不要自动登录，改用
Cookie-Editor 手工导出后配置 xiaohongshu-mcp / 存量工具。

Boss直聘配置触发：当用户说“帮我配 Boss直聘”时，先读取 `references/career.md`
的 Boss 章节，然后在获得安装授权后运行
`agent-reach install --env=local --system --channels=boss`。Agent 负责按系统启动
只绑定 `127.0.0.1:9222` 的专用 Chrome；**拉起后第一步是暂停并让用户肉眼确认**
窗口内是已登录状态（右上角有头像），未登录则让用户登录/扫码，用户确认后再运行
`boss --cdp-url http://localhost:9222 login --cdp` 和 `agent-reach doctor` 验收。
不要让用户自己研究端口参数。
专用 Chrome profile 必须长期复用，不要每次创建，也不要默认改用日常主 Chrome。

判断 CDP 浏览器登录态**不要信 `boss status`**（它只校验本地 session.enc，与
浏览器登录态互不代表），以 `agent-reach doctor` 的浏览器 cookie 探测（wt2）
为准，并配合用户肉眼确认。绝不用当前页 URL 判断登录态：
`security-check` / `zhipin-security` / `_security_check` 安全校验页是 Boss 反爬挑战，
与登录无关——已登录也会出现（带 CDP 调试端口的 Chrome 几乎必现）。看到它不要
当成“未登录”，先跑 `agent-reach doctor` 看浏览器 cookie，再决定是否需要用户登录。
搜索报 `AUTH_EXPIRED` 即浏览器未登录的 ground truth：直接走登录流程 + `login --cdp`，
不要往安全校验方向解释。

执行搜索时必须使用
`boss --browser-source existing-browser --cdp-url http://localhost:9222 search ...`；
遇到 `ENVIRONMENT_RISK` 立即停止，不刷新、不重新登录、不自动重试。

```bash
# Twitter 搜索（twitter-cli 首选；失败重试链见 social.md）
twitter search "query" -n 10

# Reddit（无零配置路径：OpenCLI 或 rdt-cli，必须登录态）
opencli reddit search "query" -f yaml   # 桌面
rdt search "query" --limit 10            # 存量/服务器

# 小红书（桌面首选 OpenCLI）
opencli xiaohongshu search "query" -f yaml

# Facebook / Instagram（桌面 OpenCLI，复用浏览器登录态）
opencli facebook search "query" -f yaml
opencli facebook groups -f yaml
opencli instagram search "query" -f yaml       # 搜用户
opencli instagram user USERNAME -f yaml        # 读指定用户最近帖子
```

## 环境检查

`agent-reach` 不在 PATH 时，发现实际包管理器、虚拟环境或入口路径后调用，
不要假定某个 conda 环境名。只使用内置搜索时不需要运行此检查。

```bash
# 检查可用 channel 与每个平台当前激活的后端
agent-reach doctor --json
```

## OpenCLI 适配器发现

路由表没有覆盖用户需要的平台或命令时，先用 `opencli list` 查已有适配器，再用
`opencli <平台> --help` 查看公开命令。发现适配器只证明命令存在，不证明登录态或
目标内容可用；仅在用户任务明确需要该平台时执行只读命令，并以实际非空内容验收。

## 工作区规则

临时输出使用当前系统临时目录或工作区指定的临时位置，结束后清理本次中间文件。
持久配置使用工具实际配置目录；用户要求交付的文件按其工作区规则保存。
Cookie、API key 和浏览器数据不得写入 skill、源码仓库、日志或回答。

## 详细文档

根据用户需求，阅读对应的详细文档：

- [搜索工具](references/search.md) — 内置/外部搜索、结果验收与按需补充
- [社交媒体](references/social.md) — 小红书, Twitter, B站, V2EX, Reddit, Facebook, Instagram（多后端/登录态命令组）
- [职场招聘](references/career.md) — LinkedIn, Boss直聘
- [开发工具](references/dev.md) — GitHub CLI
- [网页阅读](references/web.md) — 内置读取、Firecrawl、TinyFish Fetch、宿主浏览器、RSS
- [视频播客](references/video.md) — YouTube, B站, 小宇宙
- [金融行情](references/finance.md) — 雪球股票行情、搜索、热门内容

## 配置渠道

如果某个 channel 需要配置，读取个人仓库的安装指南：
https://raw.githubusercontent.com/binawoh/Agent-Reach/main/docs/install.md

用户只需提供 cookies，其他配置由 agent 完成。
