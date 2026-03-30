#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de consulta à API v3 do VirusTotal.
Envia a URL para análise e retorna o resultado consolidado.

Fluxo:
  1. POST /urls           → obtém analysis_id
  2. GET  /analyses/{id}  → aguarda conclusão (polling)
  3. Retorna dict com total de engines, detecções e lista de AVs que flagaram

Dependência: apenas urllib (stdlib) — sem requests.
"""

import json
import time
import base64
import urllib.request
import urllib.error
import urllib.parse

# Tempo máximo de espera pelo relatório (segundos)
VT_POLL_TIMEOUT   = 180
VT_POLL_INTERVAL  = 16

# FIX #5: tempo de espera ao receber HTTP 429 (rate limit da API free tier).
# O plano gratuito do VT permite 4 req/min — scans com crawler ativo podem
# atingir esse limite. Aguardamos 15s antes de retentar automaticamente.
VT_RATE_LIMIT_WAIT   = 15
VT_RATE_LIMIT_RETRIES = 2

# URL base da API v3
VT_API_BASE = "https://www.virustotal.com/api/v3"


def _vt_request(endpoint: str, method: str = "GET",
                data: bytes = None, api_key: str = "") -> dict:
    """
    Faz uma requisição autenticada à API do VirusTotal.

    FIX #5: trata HTTP 429 (Too Many Requests) com retries automáticos
    antes de propagar o erro — evita falha silenciosa em scans intensivos.
    """
    url = f"{VT_API_BASE}{endpoint}"
    headers = {
        "x-apikey": api_key,
        "Accept": "application/json",
    }
    if data:
        headers["Content-Type"] = "application/x-www-form-urlencoded"

    req = urllib.request.Request(url, data=data, headers=headers, method=method)

    for attempt in range(1 + VT_RATE_LIMIT_RETRIES):
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < VT_RATE_LIMIT_RETRIES:
                # Rate limit atingido — aguarda e retenta
                time.sleep(VT_RATE_LIMIT_WAIT)
                continue
            body = e.read().decode("utf-8", errors="ignore")
            return {"error": f"HTTP {e.code}: {body[:300]}"}
        except Exception as ex:
            return {"error": str(ex)}

    # Esgotou as retentativas de rate limit
    return {"error": "HTTP 429: Rate limit atingido após retentativas. Tente novamente em instantes."}


def scan_url_virustotal(url: str, api_key: str) -> dict:
    if not api_key:
        return {"status": "error", "error": "Chave de API do VirusTotal não configurada."}

    # Calcula o ID da URL conforme documentação do VT (base64 sem padding)
    url_id = base64.urlsafe_b64encode(url.encode()).decode().rstrip("=")
    permalink = f"https://www.virustotal.com/gui/url/{url_id}"

    # ── 1. TENTA BUSCAR RELATÓRIO EXISTENTE (Fluxo Rápido / Instantâneo) ─────
    existing_report = _vt_request(f"/urls/{url_id}", method="GET", api_key=api_key)

    if "error" not in existing_report and "data" in existing_report:
        # Relatório encontrado! Puxa os dados direto, sem polling.
        attrs = existing_report.get("data", {}).get("attributes", {})
        stats = attrs.get("last_analysis_stats", {})
        results = attrs.get("last_analysis_results", {})
        
    else:
        # ── 2. SE NÃO EXISTIR, SUBMETE E AGUARDA (Fluxo Lento / Polling) ───────
        post_data = urllib.parse.urlencode({"url": url}).encode("utf-8")
        submit    = _vt_request("/urls", method="POST", data=post_data, api_key=api_key)

        if "error" in submit:
            return {"status": "error", "error": submit["error"]}

        analysis_id = (submit.get("data", {}) or {}).get("id", "")
        if not analysis_id:
            return {"status": "error", "error": "VirusTotal não retornou ID de análise."}

        # Polling: aguarda conclusão
        deadline   = time.time() + VT_POLL_TIMEOUT
        result_obj = {}

        while time.time() < deadline:
            result_obj = _vt_request(f"/analyses/{analysis_id}", api_key=api_key)

            if "error" in result_obj:
                return {"status": "error", "error": result_obj["error"]}

            analysis_status = result_obj.get("data", {}).get("attributes", {}).get("status", "")
            if analysis_status == "completed":
                break

            time.sleep(VT_POLL_INTERVAL)
        else:
            return {"status": "queued",
                    "error": "VirusTotal ainda não concluiu a análise. Tente novamente em instantes."}

        # Extrai os dados do novo scan
        attrs   = result_obj.get("data", {}).get("attributes", {})
        stats   = attrs.get("stats", {})
        results = attrs.get("results", {})


    # ── 3. PROCESSA O RESULTADO FINAL (Comum aos dois fluxos) ────────────────
    malicious  = stats.get("malicious", 0)
    suspicious = stats.get("suspicious", 0)
    harmless   = stats.get("harmless", 0)
    undetected = stats.get("undetected", 0)
    total      = malicious + suspicious + harmless + undetected

    # Lista apenas engines com detecção positiva (malicious ou suspicious)
    detections = []
    for engine_name, engine_data in (results or {}).items():
        category = engine_data.get("category", "")
        if category in ("malicious", "suspicious"):
            detections.append({
                "engine":   engine_name,
                "category": category,
                "result":   engine_data.get("result", ""),
            })

    # Ordena: malicious primeiro, depois suspicious; ambos em ordem alfabética
    detections.sort(key=lambda x: (0 if x["category"] == "malicious" else 1, x["engine"].lower()))

    return {
        "status":     "ok",
        "total":      total,
        "malicious":  malicious,
        "suspicious": suspicious,
        "harmless":   harmless,
        "undetected": undetected,
        "detections": detections,
        "permalink":  permalink,
        "error":      None,
    }