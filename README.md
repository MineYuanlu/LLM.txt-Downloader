# LLM Data Downloader

自动抓取 `llms.txt` 及其关联资源，保存为本地文件，并将链接替换为相对路径。

## 功能

- 从起始 `llms.txt` 出发，BFS 递归下载所有关联的 `.txt` / `.md` 文件
- 多线程并发下载（默认 8 线程）
- 下载完成后将文件内链接替换为本地相对路径
- 支持跨站白名单、子域名同站判断

## 使用

```bash
pip install requests
python downloader.py
```

下载结果保存在 `data/` 目录下，按域名分级存放。

## 配置

编辑 `downloader.py` 顶部的配置区域：

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `START_URL` | 起始 llms.txt 地址 | shadcn-svelte.com |
| `TARGET_DIR` | 本地保存根目录 | `./data` |
| `ALLOWED_DOMAINS` | 跨站下载白名单 | shadcn-svelte.com |
| `ALLOW_CROSS_DOMAIN` | 是否允许跨站下载 | `True` |
| `ALLOW_SUBDOMAIN` | 子域名视为同站 | `True` |
| `MAX_WORKERS` | 并发线程数 | `8` |

## 分支说明

| 分支 | 说明 |
|------|------|
| `master` | 源码，`/data` 已在 `.gitignore` 中忽略 |
| `data` | 自动生成，包含下载的数据文件，保留完整历史 |

## 自动化

GitHub Actions 工作流（`.github/workflows/download-data.yml`）自动维护 `data` 分支：

- **触发**：master 推送 / 每日定时 / 手动触发
- **策略**：拉取 `data` 分支 → merge master → 运行脚本 → 有变化则提交，无变化跳过
- **要求**：仓库 Settings → Actions → General → Workflow permissions 设为 **Read and write**
