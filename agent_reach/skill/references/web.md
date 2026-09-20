# 网页阅读

已知 URL 时先读取目标页面，不为读取而重复全网搜索。遵守 SKILL.md 的费用限制：
TinyFish 只用免费 Search / Fetch，禁止 Agent、Agent Batch、Browser 及对应 MCP/API。

## 选择读取工具

| 需要 | 选择 |
|-----|------|
| 核对一段事实、打开搜索结果 | 当前宿主内置网页读取，内容足够即可结束 |
| 完整正文、表格、Markdown 提取 | 已认证且确认免费额度可用的 Firecrawl |
| 指定 TinyFish、或补充另一种正文提取 | 免费 TinyFish Fetch |
| 替代读取路径 | 可用且符合费用限制的 Jina Reader、web-reader MCP 等 |
| 展开/翻页/点击后才出现目标内容 | 宿主已有且不额外收费的浏览器工具 |
| 平台帖子/视频/行情 | 回到 social、video、finance 等专用 reference |
| RSS | feedparser |

不要只看响应非空或文本长度：确认正文包含用户需要的段落、字段、表格和时间信息。
抓到菜单、登录页、验证码或缺少关键表格不算完成；搜索摘要也不等于已读取原文。
普通读取不完整时换另一免费读取器或宿主浏览器，无法补齐则说明缺失部分。
不得为了补齐、测试或自动重试调用 TinyFish 付费功能，即使账户里有赠送余额。

## Firecrawl

先按 [Firecrawl CLI 准备](search.md#firecrawl-cli-准备) 完成缺失 CLI 的安装、
本机认证和免费额度核验；现有 CLI 可用就直接复用。

```bash
firecrawl scrape "https://example.com/article" --format markdown --only-main-content
```

需要 JSON 时按当前 `firecrawl scrape --help` 添加 `--json`。Search 和 Scrape
参数不一定相同，不把一个子命令的参数直接套到另一个子命令。读取后检查关键内容，
超时或限流时按实际错误调整调用，不自动升级套餐。

## TinyFish Fetch（仅免费功能）

复用本机已认证且确认免费可用的 CLI/MCP：

```bash
tinyfish fetch content get --format markdown "https://example.com/article"
```

按当前版本的公开响应检查结果与错误。普通 Fetch 可能漏掉折叠区、表格或动态内容；
改用上述其他免费通道，不升级到 TinyFish Agent 或 Browser。安装和认证说明见
[搜索工具](search.md)，无需因为新装 MCP 尚未载入当前会话就重复安装。

## 宿主浏览器

当关键内容需要展开、翻页或点击时，检查当前 Agent 实际提供的浏览器工具及其说明，
遵循对应 skill 或工具协议做只读导航。不得假定每个 Agent 都有相同的工具名、CDP
端口或浏览器登录态；涉及平台登录时遵守相应平台的认证边界。
没有允许使用的浏览器能力，就寻找同一发布者的静态页面/PDF或报告无法读取的内容。

## 其他读取器

发现可用接口且符合费用限制后使用。例如 Jina Reader：

```bash
curl -s "https://r.jina.ai/https://example.com/article"
```

已有 web-reader MCP 时，按实际 schema 调用：

```bash
mcporter call web-reader.webReader url="https://example.com/article" return_format="text"
```

不要因工具名已配置就断言目标页面可读，以实际返回的目标内容为准。

## RSS (feedparser)

使用当前环境发现的 Python 解释器运行：

```python
import feedparser

for entry in feedparser.parse('FEED_URL').entries[:5]:
    print(f'{entry.title} — {entry.link}')
```
