---
name: agent-reach
description: >
  搜索、调研和读取互联网内容时，按任务选择当前 Agent 的内置搜索、Exa 等外部搜索、
  平台专用通道、正文抓取或宿主浏览器工具。适用于网页/新闻/官方资料查询、URL 阅读、
  小红书/B站/Twitter/Reddit 等站内内容、视频字幕和 RSS。
  只负责获取与核验内容，不负责发帖、评论等写操作；已有专门平台 skill 时优先使用它。
  也适用于安装、查看状态、管理平台渠道和更新 Agent Reach。
metadata:
  homepage: https://github.com/binawoh/Agent-Reach
  version: "{{VERSION}}"
---

# Agent Reach

一个命令读所有平台：`agent-reach`。只读，默认输出一行 JSON。

动手前先说一句"用 agent-reach skill（X 渠道）"。本 skill 被调用后全程有效，以下规则一直适用。

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

## 路由表

普通搜索和最新消息先用宿主搜索，官方原文、技术文档和财报优先用 Exa。精确查 GitHub 源码时用 GitHub 搜索。需要补充时按任务选 Tavily、Firecrawl Search 或免费 TinyFish Search。已知 URL 用宿主读取、Firecrawl 或免费 TinyFish Fetch，交互页面用宿主浏览器，RSS 用 feedparser。平台任务优先用已有的专门 skill。用户指定工具时优先使用，并说明实际采用的替代来源。详见[搜索工具](references/search.md)、[网页与 RSS](references/web.md)和[个人版本维护](references/personal-maintenance.md)。

## 选路

- 公开内容先用你自带的搜索/读取工具（可加 `site:域名`）。正文、评论、字幕分别核对是否已拿到；够了就直接回答，不装渠道、不登录。
- 自带工具不可用、结果缺了用户要的部分、或用户要的是渠道声明的站内动作时，再用 Reach。不确定有哪些动作和参数先跑 `agent-reach channels`。
- 渠道已经加上（默认渠道或 `add` 过）时，搜索/阅读直接走该站工具；还没加的渠道，搜索/阅读先试免登录公开网页，结果里 `backend: public-web` 标明来源。`--backend public-web` 只查公开网页；`--backend <后端>` 指定站内工具。
- 平台名或链接只用来认出来源，不自动触发安装或登录。
- 摘要、页面壳、评论计数、字幕轨道列表不等于正文、评论或字幕本身，要分别说明。用户跳过登录时，已拿到的公开结果照样交付。

```bash
agent-reach channels                      # 每个渠道的动作和参数
agent-reach <渠道> <动作> [参数]          # 例：agent-reach xiaohongshu search "咖啡" --limit 5
agent-reach read <链接>                   # 按链接自动选渠道
```

## 结果与错误

- `ok: true` → 内容在 `items`，每条有 `title / url / author / published_at / text`，原始数据在 `raw`。
- `ok: false` → 看 `error.code`，照 `error.hint` 做：

| error.code | 怎么办 |
|---|---|
| `NEED_SETUP` | 缺依赖或密钥。按提示 `agent-reach add <渠道>`；要密钥时请用户本人提供，再 `agent-reach configure <key>` |
| `NEED_LOGIN` | 保留已有结果，告诉用户需要登录；`agent-reach login <渠道>` 打开浏览器，由用户本人登录，你绝不代登、不要密码 |
| `UPSTREAM_BROKEN` | 这个平台暂时有问题，`message` 是出错时的原话。用平台名告诉用户哪个平台暂时用不了、大概是什么原因，不说工具名；原话说明工具过时，才在用户同意后跑一次 `agent-reach update`；不循环重试 |
| `TIMEOUT` | 看失败阶段和渠道状态（`agent-reach doctor --text`）；不反复重试、不反复开窗 |
| `RATE_LIMITED` | 平台限流，Reach 已暂停该渠道；按 `retry_after_seconds` 等，不换后端 |
| `PLATFORM_BLOCKED` | 平台要求验证（验证码/风控）。停下，请用户在官方页面处理；不换账号、不换后端 |
| `BUSY` | 排队等了 2 分钟浏览器仍然满，或用户正开着登录窗口。过一会儿、或等用户说登好了再试；不关窗口、不切换配置 |
| `NOT_FOUND` | 内容不存在，核对链接或 ID |
| `BAD_INPUT` | 参数不对，跑 `agent-reach channels` 看用法 |

遇到 `PLATFORM_BLOCKED`、`RATE_LIMITED`、`NEED_LOGIN`、`BUSY` 就停止本次尝试，不换账号、后端或浏览器反复请求。网络失败或某台机器的失败不能说成"平台必须登录"。

## 登录与专用浏览器

所有浏览器渠道共用一个专用浏览器（优先 CloakBrowser，装不上时用本机 Chrome），默认无头不弹窗，闲置 10 分钟自动关闭，下次调用自动重开。可以并行调用（包括子代理同时查）：同一平台最多同时 2 条，所有平台合计 4 条，多出来的自动排队；同一平台的两次搜索之间至少隔 10 秒。

第一次用某个网站时，如果用户的 Chrome 已连接 OpenCLI 扩展，程序会把该站登录自动复制一次到专用浏览器，之后一直复用；只复制该站，不动原浏览器。登录失效或没有可复制的来源时，才请用户本人 `agent-reach login <渠道>`。刷新、选来源、退出等细节见 [会话与专用浏览器](references/sessions.md)：用户要登录、退出、换账号，或遇到 `NEED_LOGIN` 时读它。

## 平台注意

- 小红书 read 只返回文字描述，不要声称看懂了图片或视频。
- Boss 直聘搜索结果 `salary_encoded=true` 时绝不猜薪资数字；read 职位链接拿详情里的可读薪资。
- 各平台公开能做什么、Reach 补什么，见 [能力边界](references/capabilities.md)：用户问"能查什么/查得全吗"或要判断结果完整度时读它。

## 渠道

{{CHANNEL_TABLE}}

`default` 是默认安装的渠道，也可以去掉，去掉后更新不会加回来。`login` 列是认证入口，不是查公开内容的前提。

## 安装完成时

`agent-reach setup` 后，把 `result.installation_report.markdown` 原样展示给用户，不增删、不重排、不自己补问候或表格；报告由程序生成。

## 用户要管理 Agent Reach 时

| 用户说 | 你运行 |
|---|---|
| 加上某个平台 | `agent-reach add <渠道>`，依赖自动装好；只告诉用户他必须做的事（登录或提供密钥） |
| 去掉某个平台 | `agent-reach remove <渠道>` |
| 登录 / 登录过期 | `agent-reach login <渠道>`，由用户本人在打开的窗口里登录 |
| 退出登录 | `agent-reach logout <渠道>` |
| 看看状态 / 哪些能用 | `agent-reach doctor --text`；要实测跑 `agent-reach check <渠道> --text` |
| 升级 / 更新 | `agent-reach update` |
| 卸载 | 先 `agent-reach uninstall --dry-run` 给用户看，确认后 `agent-reach uninstall` |
| 让另一个 AI 也能用 | `agent-reach skill link <那个 AI 的 skill 目录>`；`agent-reach skill` 查看现在放在哪 |

故障排查、浏览器维护和卸载细节见 [维护说明](references/maintenance.md)：更新失败、浏览器起不来或要卸载时读它。

## 有新版本时

结果里出现 `meta.update` 就说明有新版本。每次对话只提一次，用用户的语言、大白话：

1. 告诉用户有新版本（`meta.update.latest`）。
2. 从 `meta.update.notes` 挑 1 到 3 个要点说清改了什么。
3. 问要不要更新；用户同意后才跑 `agent-reach update`。

## 红线

- 只读。发帖、评论、点赞、私信一律不做。
- 不替用户登录，不索要或输出密码、Cookie 等凭据。
- 普通查询不改依赖、不自动更新。
