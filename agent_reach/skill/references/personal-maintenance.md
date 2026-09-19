# 个人版本维护

个人源码为 `binawoh/Agent-Reach` 的 `main`；保留 Exa、Tavily、Firecrawl、TinyFish 搜索路由。
仓库位置、skill 安装目录、运行环境和调用脚本均由执行任务的 agent 自行发现，不固定路径。

更新或换机时：

1. 根据当前 skill 的加载位置、agent 配置、命令发现及包管理器信息确认实际安装方式。
   若找到源码仓库，检查 Git remote 和工作区状态；若没有，在合适的位置克隆个人仓库。
2. 只从个人 `main` 获取更新；已有克隆使用快进拉取，遇到本地改动或分叉先处理，不覆盖。
   上游 `Panniantong/Agent-Reach` 只读；不向其推送，也不提交 PR。
3. 按当前 agent 的实际技能加载方式更新 `SKILL.md` 和配套 references，保留目录链接及无关文件。
   需要更新 Agent Reach CLI 时，先识别现有包管理方式，再从个人源码安装。适配代码可现场编写。
4. 发现可用搜索后端并执行真实搜索验证。PowerShell 参考脚本可复用，也可直接使用 MCP/CLI/API；
   不要求安装特定入口命令。新装 MCP 在新会话加载，不反复安装。
   需要 Firecrawl CLI 但尚未安装时，先按 [准备流程](search.md#firecrawl-cli-准备) 安装并验证。

上游由个人仓库工作流定期合并并测试。不要直接安装上游 ZIP 或强制同步覆盖个人提交。
后续定制修改个人源码并同步实际使用的 skill；发生冲突或测试失败时先处理失败。
Cookie、API key 和浏览器数据只在本机配置，不进入源码仓库；新电脑单独认证或安全迁移。
更多说明见 [个人版本说明](https://github.com/binawoh/Agent-Reach/blob/main/docs/personal-fork.md)。
