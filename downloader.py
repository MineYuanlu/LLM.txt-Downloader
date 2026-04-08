#!/usr/bin/env python3
"""
LLM.txt 本地化下载工具

用法：
    python llm_downloader.py

配置在 main 函数中修改：
- START_URL: 起始 llms.txt 地址
- TARGET_DIR: 本地保存根目录
- ALLOWED_DOMAINS: 跨站白名单（set）
- ALLOW_CROSS_DOMAIN: 是否允许下载白名单中的跨站资源
- ALLOW_SUBDOMAIN: 是否将子域名视为同站（例如 www.example.com 与 example.com）
"""

import os
import re
import requests
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse, urljoin
from pathlib import Path
from typing import Dict, Set, Optional, List, Tuple

# ------------------------------
# 配置区域（可根据需要修改）
# ------------------------------
START_URL = "https://www.shadcn-svelte.com/llms.txt"
# 本地存储根目录：脚本所在目录下的 llm 文件夹
TARGET_DIR = Path(__file__).parent / "data"
# 跨站下载白名单（仅当 ALLOW_CROSS_DOMAIN = True 时生效）
ALLOWED_DOMAINS = {
    "shadcn-svelte.com",
    "www.shadcn-svelte.com",
    # 可添加其他信任域名
}
# 是否允许跨站下载（True 时白名单内的域名资源会被下载）
ALLOW_CROSS_DOMAIN = True
# 是否将子域名视作同站（例如 www.example.com 和 example.com 视为同一站点）
ALLOW_SUBDOMAIN = True
# 允许下载的文件扩展名
ALLOWED_EXTENSIONS = {".txt", ".md"}
# 并发下载线程数
MAX_WORKERS = 8

# 请求头
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; LLMDownloader/1.0)"
}


class LLMDownloader:
    """下载 llms.txt 及其关联资源，并替换链接为相对路径"""

    def __init__(
        self,
        target_dir: Path,
        allowed_domains: Set[str],
        allow_cross_domain: bool = False,
        allow_subdomain: bool = True,
        allowed_extensions: Set[str] = ALLOWED_EXTENSIONS,
        max_workers: int = MAX_WORKERS,
    ):
        self.target_dir = target_dir.resolve()
        self.allowed_domains = allowed_domains
        self.allow_cross_domain = allow_cross_domain
        self.allow_subdomain = allow_subdomain
        self.allowed_extensions = allowed_extensions
        self.max_workers = max_workers
        self.visited_urls: Set[str] = set()
        self._lock = threading.Lock()  # 保护 visited_urls

        # 确保目标目录存在
        self.target_dir.mkdir(parents=True, exist_ok=True)

    def _normalize_domain(self, netloc: str) -> str:
        """提取注册域名部分（简单处理，去掉 www 前缀用于子域判断）"""
        if not self.allow_subdomain:
            return netloc
        # 简单去掉开头的 "www."
        if netloc.startswith("www."):
            return netloc[4:]
        return netloc

    def _is_same_site(self, url1: str, url2: str) -> bool:
        """判断两个 URL 是否属于同一站点（考虑子域设置）"""
        net1 = urlparse(url1).netloc
        net2 = urlparse(url2).netloc
        return self._normalize_domain(net1) == self._normalize_domain(net2)

    def _is_allowed_domain(self, netloc: str) -> bool:
        """检查域名是否在白名单中（或与起始站点相同）"""
        if self.allow_cross_domain:
            return netloc in self.allowed_domains
        return False

    def _is_allowed_extension(self, url: str) -> bool:
        """检查 URL 是否指向允许的文件类型（.txt/.md）"""
        path = urlparse(url).path.lower()
        return any(path.endswith(ext) for ext in self.allowed_extensions)

    def _should_download(self, url: str, base_url: str) -> bool:
        """判断是否应该下载该 URL 的资源"""
        parsed = urlparse(url)
        # 跳过非 http/https 协议
        if parsed.scheme not in ("http", "https"):
            return False
        # 只下载允许的文件类型
        if not self._is_allowed_extension(url):
            return False
        # 同站？
        if self._is_same_site(url, base_url):
            return True
        # 跨站但白名单允许？
        if self.allow_cross_domain and self._is_allowed_domain(parsed.netloc):
            return True
        return False

    def _local_path_for_url(self, url: str) -> Path:
        """根据 URL 生成本地存储路径（target_dir/域名/路径）"""
        parsed = urlparse(url)
        # 域名作为第一级目录
        domain = parsed.netloc
        # 路径部分，去掉开头的 '/'
        path = parsed.path.lstrip("/")
        if not path:
            path = "index.html"  # 默认首页名
        # 拼接
        local_path = self.target_dir / domain / path
        # 规范化并确保不逃逸出 target_dir
        local_path = local_path.resolve()
        if not str(local_path).startswith(str(self.target_dir)):
            raise ValueError(f"路径逃逸检测：{url} 试图访问 {local_path}")
        return local_path

    def _url_to_relative_link(self, target_url: str, current_file_path: Path) -> str:
        """
        将目标 URL 转换为相对于当前文件的本地链接路径（保留查询参数和锚点）
        """
        parsed = urlparse(target_url)
        # 目标本地文件路径
        target_local_path = self._local_path_for_url(target_url)
        # 计算相对路径
        current_dir = current_file_path.parent
        rel_path = os.path.relpath(target_local_path, current_dir)
        # 统一使用 Unix 风格分隔符
        rel_path = rel_path.replace(os.sep, "/")
        # 重新附上查询参数和锚点
        if parsed.query:
            rel_path += "?" + parsed.query
        if parsed.fragment:
            rel_path += "#" + parsed.fragment
        return rel_path

    def _extract_links(self, content: str, base_url: str) -> List[Tuple[str, str]]:
        """
        从内容中提取所有链接，返回 (原始匹配文本, 链接URL) 列表
        支持 Markdown 链接、自动链接和 HTML <a> 标签
        """
        links = []

        # 1. Markdown 内联链接: [text](url)
        pattern_md = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
        for match in pattern_md.finditer(content):
            text, url = match.groups()
            full_url = urljoin(base_url, url)
            links.append((match.group(0), full_url))

        # 2. Markdown 自动链接: <url>
        pattern_auto = re.compile(r"<((https?://[^>]+))>")
        for match in pattern_auto.finditer(content):
            url = match.group(1)
            full_url = urljoin(base_url, url)
            links.append((match.group(0), full_url))

        # 3. HTML <a href="...">
        pattern_html = re.compile(r'href=["\']([^"\']+)["\']', re.IGNORECASE)
        for match in pattern_html.finditer(content):
            url = match.group(1)
            full_url = urljoin(base_url, url)
            links.append((match.group(0), full_url))

        # 去重（同一原始文本可能匹配多次）
        seen = set()
        unique_links = []
        for orig, url in links:
            if orig not in seen:
                seen.add(orig)
                unique_links.append((orig, url))
        return unique_links

    def _fetch_and_save(self, url: str) -> Optional[Tuple[str, Path]]:
        """
        下载单个 URL 并保存到本地。
        使用 requests.get 而非共享 Session，避免线程安全问题。
        返回 (内容, 本地路径) 或 None。
        """
        print(f"下载: {url}")
        try:
            resp = requests.get(url, headers=HEADERS, timeout=30)
            resp.raise_for_status()
            content = resp.text
        except Exception as e:
            print(f"  错误: {e}")
            return None

        local_path = self._local_path_for_url(url)
        local_path.parent.mkdir(parents=True, exist_ok=True)
        with open(local_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  保存至: {local_path.relative_to(self.target_dir)}")
        return content, local_path

    def _build_replacement(self, orig_text: str, rel_link: str) -> str:
        """根据原始链接格式构造替换文本"""
        if orig_text.startswith("["):
            # Markdown 链接: [text](url) -> [text](rel_link)
            return f"[{orig_text.split('](', 1)[0][1:]}]({rel_link})"
        elif orig_text.startswith("<") and orig_text.endswith(">"):
            # 自动链接: <url> -> <rel_link>
            return f"<{rel_link}>"
        elif orig_text.startswith("href="):
            # HTML href: href="url" -> href="rel_link"
            quote = orig_text[5]  # " 或 '
            return f"href={quote}{rel_link}{quote}"
        return rel_link

    def _replace_links_in_file(
        self, url: str, content: str, local_path: Path
    ) -> None:
        """替换文件中的链接为本地相对路径，并重新保存文件"""
        links = self._extract_links(content, url)
        replacements = {}

        for orig_text, link_url in links:
            parsed_link = urlparse(link_url)
            if parsed_link.scheme not in ("http", "https"):
                continue
            if self._is_same_site(link_url, url) or (
                self.allow_cross_domain
                and self._is_allowed_domain(parsed_link.netloc)
            ):
                rel_link = self._url_to_relative_link(link_url, local_path)
                replacements[orig_text] = self._build_replacement(
                    orig_text, rel_link
                )

        if replacements:
            for orig, new in replacements.items():
                content = content.replace(orig, new)
            with open(local_path, "w", encoding="utf-8") as f:
                f.write(content)

    def download(self, start_url: str) -> None:
        """
        BFS 爬取 + 多线程并发下载。

        第一阶段：按层级（BFS）发现链接，每层内并发下载。
        visited_urls 由主线程在提交任务前原子标记，避免多重引用竞争。
        使用 requests.get 替代共享 Session，确保线程安全。

        第二阶段：所有文件下载完毕后，统一替换链接为本地相对路径。
        """
        print(f"目标根目录: {self.target_dir}")
        print(f"起始 URL: {start_url}")
        print(f"允许扩展名: {self.allowed_extensions}")
        print(f"并发线程数: {self.max_workers}")

        # url -> (content, local_path)，记录所有成功下载的文件
        downloaded: Dict[str, Tuple[str, Path]] = {}
        to_process = [start_url]

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            while to_process:
                # 主线程过滤已访问 URL，原子标记防止重复提交
                batch = []
                for url in to_process:
                    with self._lock:
                        if url not in self.visited_urls:
                            self.visited_urls.add(url)
                            batch.append(url)

                if not batch:
                    break

                # 并发下载当前批次
                future_to_url = {
                    executor.submit(self._fetch_and_save, url): url
                    for url in batch
                }

                # 收集下载结果，提取下一层链接
                next_level: List[str] = []
                for future in as_completed(future_to_url):
                    url = future_to_url[future]
                    try:
                        result = future.result()
                    except Exception as e:
                        print(f"  异常: {url}: {e}")
                        continue
                    if result:
                        content, local_path = result
                        downloaded[url] = (content, local_path)
                        # 提取子链接，加入下一层待处理
                        links = self._extract_links(content, url)
                        for _, link_url in links:
                            if self._should_download(link_url, url):
                                next_level.append(link_url)

                to_process = next_level

        # 第二阶段：替换所有已下载文件中的链接为本地相对路径
        print("替换链接...")
        for url, (content, local_path) in downloaded.items():
            self._replace_links_in_file(url, content, local_path)

        print(f"全部完成。共下载 {len(downloaded)} 个文件。")


def main():
    downloader = LLMDownloader(
        target_dir=TARGET_DIR,
        allowed_domains=ALLOWED_DOMAINS,
        allow_cross_domain=ALLOW_CROSS_DOMAIN,
        allow_subdomain=ALLOW_SUBDOMAIN,
    )
    downloader.download(START_URL)


if __name__ == "__main__":
    main()
