# 搜索工具

默认按 **Exa → Tavily → Firecrawl → TinyFish** 依次搜索；用户点名后端时直接使用它。
先发现当前可用的 MCP 工具、CLI 及已配置的凭据。后端不可用或调用失败才尝试下一个；
全部失败就如实报告。可自行写适配代码，但只能调用工具的公开接口，不能虚构成功结果。

若当前环境已有 `agent-search`，可以复用这个可选统一命令：

```powershell
agent-search -Query "query" -Limit 5
agent-search -Query "query" -Limit 5 -Provider tinyfish
```

可指定 `-Provider exa|tavily|firecrawl|tinyfish`；用户点名后端时直接指定它。
输出为 JSON，`provider` 表明实际后端。前一个后端调用失败才尝试下一个，全部失败则报告原因。
没有该命令时直接调用发现的后端，或参考仓库的 `agent_reach/scripts/agent-search.ps1`。
不要求把脚本放到某个固定目录。安装与换机按 [个人版本维护](personal-maintenance.md)。

## Tavily / Firecrawl / TinyFish

- Tavily 读取 `TAVILY_API_KEY`，先读进程环境，Windows 上再读当前用户环境变量。
- Firecrawl、TinyFish 复用各自 CLI 在本机保存的凭据，不把 key 写入技能或搜索脚本。
- 不要在日志或回答中打印密钥；新电脑单独配置凭据。

```powershell
agent-search -Query "query" -Limit 5 -Provider tavily
agent-search -Query "query" -Limit 5 -Provider firecrawl
tinyfish search query "query" --include-domains "example.com" --page 0
tinyfish doctor --pretty
```

TinyFish 的 `data.results` 按 `-Limit` 截取，单页默认最多 10 条；更多结果使用 CLI 的
`--page`（从 0 开始）。需要正文时按 [网页阅读](web.md) 使用 Fetch，动态交互再用 Agent。
新装的 MCP 工具要在 agent 重启后的新会话加载；当前会话没有工具时使用 CLI，不要重复安装。
doctor 标为 `unattended_safe: false` 的修复由用户执行。Windows 旧进程可从当前用户环境
重新载入 `TINYFISH_API_KEY`，不输出变量值。

以上是个人版的附加搜索路由，`agent-reach doctor` 不会把它们列作新增原生 channel；
用各工具自己的检查命令和实际搜索验证。

## Exa AI 搜索

高质量 AI 搜索引擎，适合查找技术文档、官方示例和相关网页。

```bash
mcporter call exa.web_search_exa query="query" numResults=5
mcporter call exa.web_search_exa query="library API code example" numResults=5
```

### 使用场景

| 场景 | 参数 |
|-----|------|
| 网页搜索 | `web_search_exa(query: "...", numResults: 5)` |
| 技术/代码资料 | `web_search_exa(query: "框架名 API 示例", numResults: 5)` |

> Exa MCP 的 `get_code_context_exa` 已弃用且默认不注册。代码问题也使用
> `web_search_exa`；需要精确搜索仓库内容时，改用 `dev.md` 中的 GitHub 搜索。

### 特点

- 擅长英文内容和技术文档
- 可通过查询词定位官方文档和代码示例
- 结果质量高

## 与其他搜索工具对比

| 工具 | 来源 | 适用场景 |
|-----|------|---------|
| Exa | agent-reach | 英文/技术/代码搜索 |
| Tavily | 本机环境变量认证 | Exa 失败后的网页搜索备用 |
| Firecrawl | 本机 CLI | 搜索与正文抓取 |
| TinyFish | 本机 CLI / MCP | 搜索、Fetch 正文、Agent 动态网页提取 |
| 智谱搜索 | my-mcp-tools | 中文搜索 |
| GitHub 搜索 | agent-reach (dev.md) | 仓库/代码搜索 |
