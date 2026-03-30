#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Crawler com escopo controlado: mesmo domínio, profundidade, limite de páginas.
Rate limiting incluído para não disparar alertas de DoS no alvo.
"""

import time
from collections import deque
from urllib.parse import urlparse, urljoin
import re

from .utils import http_fetch, decode_body, info

# Intervalo mínimo entre requests do crawler (segundos)
CRAWL_DELAY = 1.5

def extract_links(html: str, base_url: str):
    urls = set()
    if not html: return urls
    for match in re.finditer(r"""href\s*=\s*['"]([^'"]+)['"]""", html, re.I):
        link = match.group(1).strip()
        if not link or link.startswith("#") or link.lower().startswith("mailto:") or link.lower().startswith("javascript:"):
            continue
        if not (link.startswith("http://") or link.startswith("https://")):
            link = urljoin(base_url, link)
        urls.add(link)
    return urls

def crawl(start_url: str, max_depth=2, max_pages=15, verbose=True):
    parsed_root = urlparse(start_url)
    domain = parsed_root.netloc
    queue, visited, found = deque([(start_url, 0)]), set(), []
    last_request_time = 0.0

    while queue and len(found) < max_pages:
        url, depth = queue.popleft()
        if url in visited or depth > max_depth: continue

        # Rate limiting — aguarda o intervalo mínimo entre requests
        elapsed = time.time() - last_request_time
        if elapsed < CRAWL_DELAY:
            time.sleep(CRAWL_DELAY - elapsed)

        visited.add(url)
        found.append(url)

        if verbose: print(f"[Crawler] Visitando: {url}")

        try:
            final_url, status, headers, body = http_fetch(url, method="GET", timeout=12)
            last_request_time = time.time()
            html = decode_body(headers, body)
        except Exception:
            last_request_time = time.time()
            continue

        for l in extract_links(html, final_url):
            if urlparse(l).netloc == domain and l not in visited:
                queue.append((l, depth + 1))

    if verbose:
        info(f"Crawler finalizado. Páginas coletadas: {len(found)} (limite {max_pages}, prof. {max_depth})")

    return found