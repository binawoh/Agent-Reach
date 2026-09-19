# 个人版本维护

本机使用 `binawoh/Agent-Reach` 的个人 `main`；保留 Exa、Tavily、Firecrawl、TinyFish 搜索路由。
更新时读取当前用户目录的 `.agent-reach/personal-install.json`，其中 `source` 指向本机仓库。
在该目录运行 `./scripts/update-personal.ps1`；若记录不存在，先定位已有克隆或按
[换机安装说明](https://github.com/binawoh/Agent-Reach/blob/main/docs/personal-fork.md) 安装。

上游由仓库工作流定期合并并测试。不要直接安装上游 ZIP 或用强制同步覆盖个人提交。
发生合并冲突或测试失败时保留当前已安装版本，先处理具体失败。
后续定制修改源码仓库，再提交到自己的 main 并部署；不只修改技能安装目录，不提 PR。
Cookie、API key 和浏览器数据只在本机配置，不进入源码仓库。
