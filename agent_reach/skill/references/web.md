# 网页阅读

通用网页、RSS。

## 通用网页 (Jina Reader)

```bash
# 读取任意网页内容
curl -s "https://r.jina.ai/URL"

# 示例
curl -s "https://r.jina.ai/https://example.com/article"
```

**适用场景**: 大多数网页可以直接用 Jina Reader 读取。

## Web Reader (MCP)

```bash
# 读取网页内容 (Markdown 格式)
mcporter call web-reader.webReader url="https://example.com"

# 保留图片
mcporter call web-reader.webReader url="https://example.com" retain_images=true

# 纯文本格式
mcporter call web-reader.webReader url="https://example.com" return_format="text"
```

**适用场景**: 需要更精确控制输出格式时使用。

## TinyFish Fetch / Agent

用户指定 TinyFish，或普通阅读器无法取得正文时，使用已认证的 CLI：

```powershell
tinyfish fetch content get --format markdown "https://example.com/article"
# 需要动态交互或结构化提取时再升级为 Agent
tinyfish agent run --url "https://news.ycombinator.com/" "Read the current rank-1 story. Return JSON with title, article_url, discussion_url, points and comments. Do not vote or post."
```

Agent 成功的最终事件为 `type=COMPLETE`、`status=COMPLETED`，结果在 `resultJson`。
登录页、验证码和空结果不算读取成功，应如实说明。认证与安装见 [搜索工具](search.md)。

## RSS (feedparser)

```python
python3 -c "
import feedparser
for e in feedparser.parse('FEED_URL').entries[:5]:
    print(f'{e.title} — {e.link}')
"
```

**适用场景**: 订阅博客、新闻源、播客等 RSS feed。

## 选择指南

| 场景 | 推荐工具 |
|-----|---------|
| 通用网页 | Jina Reader (`curl r.jina.ai`) |
| 需要图片/格式控制 | web-reader MCP |
| 指定 TinyFish / 普通阅读器正文不完整 | TinyFish Fetch |
| 动态交互与结构化提取 | TinyFish Agent |
| RSS 订阅 | feedparser |
