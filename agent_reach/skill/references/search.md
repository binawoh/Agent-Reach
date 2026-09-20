# 搜索工具

按 [SKILL.md 路由表](../SKILL.md#路由表) 选择能力，并遵守其中的费用限制。
内置搜索、外部搜索、平台通道是不同入口，不设所有任务通用的后端执行顺序。

## 搜索与验收

1. **先确定要找什么**：普通网页/刚发布的内容先用当前会话内置搜索；官方原文、技术文档、
   财报深入补充优先 Exa。最新官方公告兼具两类需求时，先找当期发布，再用官方正文核验。
   用户要小红书/B站等站内体验、评论或视频时，直接按平台 reference 调用专用通道；
   普通网页的转载可作线索，不能冒充原帖。已有具体 URL 时按 [网页阅读](web.md) 读取。
2. **确认可调用**：以当前工具列表、公开 schema、CLI help 和本机认证为准。
   内置搜索直接使用宿主提供的接口，不要求另外配置 OpenAI/Anthropic API key，
   不因缺少内置工具而私自开通付费 API。已有足够近期的免费/额度证据可复用，
   不必每次重复查价；费用未知则选已确认免费或已包含的能力。
3. **检查结果是否足够**：不把退出码 0 当作任务成功。核对主题、目标主体、时间范围、
   原始出处和具体 URL。搜索“今天”时确认日期与时区，区分发布时间和事件日期；
   旧政策、上期公告、缓存摘要不能作为当期事实。重要数字或法规需打开对应原文核验。
4. **按缺口补充**：无关/旧结果、缺少原文、摘要过短时，可细化日期、主体或官方域名，
   或切换到另一可用搜索通道。内置与 Exa 可互补；Tavily、Firecrawl Search、TinyFish
   Search 按当前可用性和费用边界补充，不必等前一个工具报错。相同查询重复后仍不足，
   不继续盲目重试；换查询、来源或说明暂未找到。
5. **证据够用就结束**：一般先取少量相关结果，再读取最有价值的原文。不得把首页 URL
   当作具体文章链接，也不要从标题猜 URL；重新定位原文后再引用。报告实际使用的来源、
   尚未核实的部分，不把一次小样本测试写成永久排名，也不因搜索漏收就断言信息不存在。

## 当前 Agent 的内置搜索

先检查宿主暴露的工具与说明：例如某些 Codex/OpenAI 会话有网页搜索与打开页面工具，
某些 Claude 会话有 WebSearch/WebFetch；名称和权限随环境变化，不能硬编码。
内置搜索不可用时用已配置且符合费用限制的外部后端，不因此阻塞整个任务。
外部检索结果与宿主搜索结果都要核对时效与原文，内置不代表必然最新。

## 可选 PowerShell 助手

若当前环境已有 `agent-search`，选好外部后端后再调用：

```powershell
agent-search -Query "query" -Limit 5 -Provider exa
agent-search -Query "query" -Limit 5 -Provider tinyfish
```

可指定 `-Provider exa|tavily|firecrawl|tinyfish`，输出 JSON 的 `provider` 表明实际后端。
助手无法发现或调用宿主内置工具，也不判断费用、时效和内容质量；这些由 agent 负责。
为兼容已有用法保留的 `auto` 只按 Exa → Tavily → Firecrawl → TinyFish 处理调用失败，
不是本 skill 的任务路由。通常明确指定后端；仅在允许涉及的全部后端且只需调用失败兜底时用 auto。
没有该命令时直接调用发现的后端，或参考仓库的 `agent_reach/scripts/agent-search.ps1`。
不要求把脚本放到某个固定目录。安装与换机按 [个人版本维护](personal-maintenance.md)。

## Tavily / Firecrawl / TinyFish

### Firecrawl CLI 准备

任务选中 Firecrawl 且符合费用限制后（包括通过助手调用），先完成以下检查。
不要为了一个内置搜索已完成的任务安装全部后端：

1. 用当前 shell 的命令发现机制检查 `firecrawl`，存在时运行 `firecrawl --version`。
   CLI 已可用就直接复用，不重复安装或为此升级。
2. 未安装时由 agent 先安装官方 CLI，再继续原任务：

   ```bash
   npm install -g firecrawl-cli
   firecrawl --version
   ```

   若缺少 Node.js/npm，先按当前系统准备运行环境。安装位置由环境决定；若安装成功但
   命令仍找不到，发现实际 npm 安装目录并修正当前进程 PATH 或使用实际入口，不反复安装。
3. **搜索或抓取前必须确认认证成功**：运行 `firecrawl --status`，复用现有本机配置或
   `FIRECRAWL_API_KEY`。另一台电脑即使装好了 CLI，也要独立检查认证状态。
   未认证时先完成认证，不能只提示缺少凭据就执行搜索。用 `firecrawl login --help`
   确认当前版本支持的方式；已有 API key 时在本机安全配置，没有现成凭据时由 agent
   启动浏览器登录，例如 `firecrawl login --method browser`。
   若需要用户本人登录或授权，明确告知并等待完成，再重新运行 `firecrawl --status`；
   确认已认证后才继续。等待用户登录不等于认证失败，不因此直接跳过 Firecrawl。
   安装成功或登录命令已启动都不代表认证完成；不打印密钥，不将其写入 skill 或 Git。
4. 核对免费套餐/剩余额度及超额计费行为；认证成功不等于免费，无法确认不产生额外费用时，
   按费用限制换通道，不通过调用试探是否扣费。满足条件后执行原来的搜索或抓取确认可用。
   安装或认证确实受阻时报告具体原因；自动选择工具时可继续其他后端，
   用户指定 Firecrawl 时如实说明阻塞，不把其他后端的结果冒充 Firecrawl。

安装命令来源：[Firecrawl 官方 CLI](https://github.com/firecrawl/cli#installation)。

### 凭据与调用

- Tavily 读取 `TAVILY_API_KEY`，先读进程环境，Windows 上再读当前用户环境变量。
- Firecrawl、TinyFish 复用各自 CLI 在本机保存的凭据，不把 key 写入技能或搜索脚本。
- 不要在日志或回答中打印密钥；新电脑单独配置凭据。

```powershell
agent-search -Query "query" -Limit 5 -Provider tavily
agent-search -Query "query" -Limit 5 -Provider firecrawl
tinyfish search query "query" --include-domains "example.com" --page 0
tinyfish doctor --pretty
```

TinyFish CLI 的 `results`（助手包装后为 `data.results`）按需要截取；CLI 默认返回约 10 条，
不足时可能更少，更多结果按当前 help 使用 `--page`。部分结果可能只有网站首页链接，
必须另行定位具体原文，不能视为可直接引用的文章。需要正文时按 [网页阅读](web.md)
使用免费 Fetch；禁止升级为 TinyFish Agent、Agent Batch 或 Browser。
新装的 MCP 工具要在 agent 重启后的新会话加载；当前会话没有工具时使用 CLI，不要重复安装。
doctor 标为 `unattended_safe: false` 的修复由用户执行。Windows 旧进程可从当前用户环境
重新载入 `TINYFISH_API_KEY`，不输出变量值。

以上是个人版的附加搜索路由，`agent-reach doctor` 不会把它们列作新增原生 channel；
用各工具自己的检查命令和实际搜索验证。

## Exa AI 搜索

用于查找官方原文、技术文档、示例和财报。先检查当前 MCP schema；需要 `objective`
时传入本次检索目标，不凭旧示例猜参数。以下示例符合当前公开工具契约：

```bash
mcporter call exa.web_search_exa query="query" objective="Find the original source for this query" numResults=5
mcporter call exa.web_search_exa query="library API code example" objective="Find official documentation and examples" numResults=5
```

> Exa MCP 的 `get_code_context_exa` 已弃用且默认不注册。代码问题也使用
> `web_search_exa`；需要精确搜索仓库内容时，改用 `dev.md` 中的 GitHub 搜索。

具体平台使用对应 reference。未列出的搜索服务只有在当前环境实际提供、符合任务与费用限制时才使用。
