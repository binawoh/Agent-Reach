# 个人定制版：同步上游与换机使用

本仓库的 `main` 是个人长期维护版本，保留 **Exa → Tavily → Firecrawl → TinyFish**
搜索路由。两个旧功能分支保留，不把其未合并代码自动并入本版本。

## 上游同步

GitHub Actions 的 **Sync upstream with personal customizations** 每 6 小时检查上游
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
> 保留四个搜索后端、本机凭据和目录链接，只修改个人仓库，不修改上游、不提 PR。

agent 应先检查当前加载的 skill、工具和配置，再选择安装位置及调用方式。
已有源码快进拉取个人 `main`，有本地改动或分叉时先处理；没有源码时可克隆到合适的位置。
技能内容来自 `agent_reach/skill/`，适配代码可由 agent 在运行时编写。
不要用上游 ZIP、强制同步或 reset 覆盖个人定制。

仓库中的 `agent_reach/scripts/agent-search.ps1` 是可选的 PowerShell 参考实现，
不要求放到某个固定目录或必须叫某个命令。也可以直接使用已加载 MCP、公开 CLI 或 API。
若选择该脚本，需要 PowerShell 7，并按各后端实际需要准备运行环境和认证。

## 凭据与验证

仓库只保存程序、文档和测试，不保存 Cookie、API key、浏览器数据或 MCP 私人配置。
Tavily 可读取 `TAVILY_API_KEY`；Firecrawl、TinyFish 使用各自 CLI/MCP 的本机认证。
换电脑后单独登录或安全迁移凭据；不要把凭据放进 Git 或安装示例。

安装完成后必须执行真实搜索，报告实际使用的后端。安装成功不等于所有后端都已认证。
TinyFish 可用 `tinyfish doctor --pretty` 检查；新装的 MCP 工具需要新会话加载。
对当前环境不存在的目录或命令，先发现或适配，不要仅凭路径不同判定安装损坏。
