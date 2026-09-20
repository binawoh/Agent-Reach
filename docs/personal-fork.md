# 个人定制版：同步上游与换机使用

本仓库的 `main` 是个人长期维护版本，按任务发现并选择宿主内置工具、Exa/Tavily 等外部
搜索、正文抓取和平台专用通道。具体规则以 [skill](../agent_reach/skill/SKILL.md) 为准。
只使用已确认免费或不额外收费的能力；TinyFish 仅允许免费 Search/Fetch，禁用
Agent、Agent Batch、Browser 及同等 MCP/API 入口，不消费赠送余额去测试付费功能。
两个旧功能分支保留，不把其未合并代码自动并入本版本。

## 上游同步

GitHub Actions 的 **Sync upstream with personal customizations** 每周一 09:23（新加坡／北京时间）检查上游
`Panniantong/Agent-Reach` 的 `main`，也支持在 Actions 页面手动运行。
Git 合并保留个人提交；只有全量测试通过，才推送合并结果到 **binawoh/Agent-Reach**。
发生冲突、测试失败或推送竞争时停止，不强推、不提 PR，完全不修改上游。
定时任务可能排队；公开仓库长期无活动时 GitHub 可能暂停定时任务，可在 Actions 页面重新启用。

云端同步不会自动修改各台电脑上的 skill。需要更新时，让当前 agent 按
[个人版本维护指引](../agent_reach/skill/references/personal-maintenance.md) 操作。

## 路径和调用方式由 agent 发现

这是一个 skill，不依赖固定的本机目录或安装脚本。可以告诉正在使用的 agent：

> 从 binawoh/Agent-Reach 的 main 安装或更新个人版 agent-reach skill。
> 请自行发现当前 skill 目录、已有源码、包管理器和可用 MCP/CLI，按当前环境完成适配并验证。
> 保留按任务路由、费用限制、本机凭据和目录链接，只修改个人仓库，不修改上游、不提 PR。

agent 应先检查当前加载的 skill、工具和配置，再选择安装位置及调用方式。
已有源码快进拉取个人 `main`，有本地改动或分叉时先处理；没有源码时可克隆到合适的位置。
另装的 `use-tinyfish` 等独立 skill 也按同一费用限制适配本机副本，移除付费升级示例；
安装或更新后检查一次，不能让独立入口绕过 TinyFish 仅免费 Search/Fetch 的限制。
技能内容来自 `agent_reach/skill/`，适配代码可由 agent 在运行时编写。
不要用上游 ZIP、强制同步或 reset 覆盖个人定制。

仓库中的 `agent_reach/scripts/agent-search.ps1` 是可选的 PowerShell 参考实现，
不要求放到某个固定目录或必须叫某个命令。也可以直接使用已加载 MCP、公开 CLI 或 API。
若选择该脚本，需要 PowerShell 7，并按各后端实际需要准备运行环境和认证。
该脚本只调用外部搜索，不发现宿主内置能力、不判断内容质量或费用；通常显式指定
`-Provider`。兼容旧用法的 `auto` 调用失败链不能替代 skill 的任务路由。

## 凭据与验证

仓库只保存程序、文档和测试，不保存 Cookie、API key、浏览器数据或 MCP 私人配置。
Tavily 可读取 `TAVILY_API_KEY`；Firecrawl、TinyFish 使用各自 CLI/MCP 的本机认证。
换电脑后单独登录或安全迁移凭据；不要把凭据放进 Git 或安装示例。

安装完成后在允许的免费范围内验证实际能力并报告后端。安装成功不等于所有后端都已认证，
认证成功也不等于免费；无法确认费用时用其他已确认免费的通道。
TinyFish 可用 `tinyfish doctor --pretty` 检查；新装的 MCP 工具需要新会话加载。
对当前环境不存在的目录或命令，先发现或适配，不要仅凭路径不同判定安装损坏。
