# 个人定制版：同步上游与换机安装

本仓库的 `main` 是个人长期维护版本；上游为 `Panniantong/Agent-Reach`。
两个旧功能分支保留，不把其未合并代码自动并入本版本。

## 更新如何发生

GitHub Actions 的 **Sync upstream with personal customizations** 每 6 小时检查上游
`main`，也支持在 Actions 页面手动运行。Git 合并保留本仓库的提交；只有全量测试通过，
才推送合并结果到本仓库 `main`。发生冲突、测试失败或推送竞争时停止，不强推、不提 PR。
定时任务可能排队；公开仓库长期无活动时 GitHub 可能暂停定时任务，可在 Actions 页面重新启用。

每台电脑独立更新已安装版本；云端同步不会自动修改电脑：

```powershell
# 在克隆的仓库目录内运行；仓库可放在任意目录
./scripts/update-personal.ps1
```

此命令只从自己的 `origin/main` 快进拉取，随后用 pipx 安装当前源码并部署技能及搜索脚本。
有未提交改动或分支分叉时停止。不要用上游 ZIP、GitHub 的强制同步或 reset 覆盖个人 main。
更改上游工具版本应单独处理，不在每次更新时强制升级所有搜索工具。

## 新电脑安装

需要 Git、Python 3.10+、pipx、PowerShell 7；搜索 CLI 还需要 Node.js（TinyFish 当前需要 24+）。
先安装这些运行环境，再在选定的任意目录执行：

```powershell
git clone https://github.com/binawoh/Agent-Reach.git
cd Agent-Reach
./scripts/setup-personal.ps1

# 新电脑缺少搜索工具时安装；已有工具无需重复安装
npm install -g mcporter firecrawl-cli @tiny-fish/cli
# 新电脑尚未配置 Exa 时注册；已有配置应保留
mcporter config add exa https://mcp.exa.ai/mcp --scope home
```

安装器按脚本自身位置寻找仓库；按当前用户目录及 `CODEX_HOME` 找到技能目录。
同时更新存在的 `.agents`、`.claude`、`.cursor`、OpenCode 技能根目录，保留目录链接。
搜索脚本安装到当前用户的 `.local/bin`，不包含用户名或盘符。
特殊目录可直接使用 `python scripts/deploy_personal.py --skill-root PATH --bin-dir PATH`。
非 Windows 系统使用相同 PowerShell 7 脚本；Tavily 可通过进程环境变量传入。

## 凭据与验证

仓库只保存程序、文档和测试，不保存 Cookie、API key、浏览器数据或 MCP 私人配置。
Tavily 读取 `TAVILY_API_KEY`；Firecrawl、TinyFish 使用各自 CLI 的本机登录或配置。
新电脑需要单独登录或安全迁移凭据。安装程序不会读取或上传这些凭据。
TinyFish MCP 仍需在各台电脑的 agent 中注册，并在新会话加载。

搜索顺序为 **Exa → Tavily → Firecrawl → TinyFish**。安装成功不等于四个服务都已认证：

```powershell
agent-search -Query 'Hacker News' -Limit 3
agent-search -Query 'Hacker News' -Limit 3 -Provider tinyfish
tinyfish doctor --pretty
```

API key 只在本机配置，不放入命令示例、Git 提交或 Actions secrets。
