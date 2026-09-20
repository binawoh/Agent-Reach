# 个人版本维护

个人源码为 `binawoh/Agent-Reach` 的 `main`；保留按任务选择内置工具、外部搜索和平台通道的路由。
同步后仍须保留 SKILL.md 的费用限制：TinyFish 仅免费 Search/Fetch，禁用 Agent/Batch/Browser。
仓库位置、skill 安装目录、运行环境和调用脚本均由执行任务的 agent 自行发现，不固定路径。

更新或换机时：

1. 根据当前 skill 的加载位置、agent 配置、命令发现及包管理器信息确认实际安装方式。
   若找到源码仓库，检查 Git remote 和工作区状态；若没有，在合适的位置克隆个人仓库。
2. 只从个人 `main` 获取更新；已有克隆使用快进拉取，遇到本地改动或分叉先处理，不覆盖。
   上游 `Panniantong/Agent-Reach` 只读；不向其推送，也不提交 PR。
3. 按当前 agent 的实际技能加载方式更新 `SKILL.md` 和配套 references，保留目录链接及无关文件。
   需要更新 Agent Reach CLI 时，先识别现有包管理方式，再从个人源码安装。适配代码可现场编写。
   若另装了 `use-tinyfish`，用本仓库的 [免费版技能模板](tinyfish-free-only.md) 更新其本机
   `SKILL.md`，保留目录链接及其他文件；未安装则无需新增。其他独立 TinyFish skill 也须移除
   升级 Agent/Batch/Browser 的指引和示例。不改包管理器缓存或第三方上游；重装后重新检查，
   避免恢复付费回退。模板保存在个人仓库，换机时直接复用，不依赖旧电脑路径。
4. 发现当前会话的内置搜索/读取/浏览器能力及任务需要的外部后端，在允许的免费范围内验证。
   不为验收启用付费功能。PowerShell 参考脚本可复用，也可直接使用 MCP/CLI/API；
   不要求安装特定入口命令。新装 MCP 在新会话加载，不反复安装。
   使用 Firecrawl 前按 [准备流程](search.md#firecrawl-cli-准备) 检查：未安装先安装，
   未认证先完成本机认证，验证通过后再搜索；不能沿用另一台电脑的认证成功结论。

上游由个人仓库工作流定期合并并测试。不要直接安装上游 ZIP 或强制同步覆盖个人提交。
后续定制修改个人源码并同步实际使用的 skill；发生冲突或测试失败时先处理失败。
Cookie、API key 和浏览器数据只在本机配置，不进入源码仓库；新电脑单独认证或安全迁移。
更多说明见 [个人版本说明](https://github.com/binawoh/Agent-Reach/blob/main/docs/personal-fork.md)。
