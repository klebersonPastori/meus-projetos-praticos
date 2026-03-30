#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scanner de segurança e phishing de página única.

Fluxo de decisão:
  1. Detecção precoce de credential spoofing (@)
  2. Resolução DNS + bloqueio de IPs privados (RFC 1918)
  3. ← ALLOWLIST: domínios confiáveis saem aqui com apenas TLS + VT como evidência.
     Nenhum fetch, HTML, JS, cookies ou anti-phishing é executado para eles.
  4. Análise completa para domínios desconhecidos/suspeitos.
"""

from urllib.parse import urlparse, urljoin
import re
import socket
import time
import ipaddress

from .utils import (
    GREEN, RESET, BOLD, CYAN, YELLOW, RED, DIM,
    banner, green, info, warn, err, good,
    normalize_url, http_fetch, decode_body, get_ssl_info,
    analyze_security_headers, parse_set_cookies, find_mixed_content,
    extract_forms, extract_scripts, scan_js_code, fetch_external_scripts,
    compute_risk_score, check_domain_age, EXFILTRATION_PATTERNS,
    is_trusted_domain
)
from .antiphishing import analyze_phishing
from .virustotal import scan_url_virustotal

# ── RFC 1918 completo + loopback + link-local ─────────────────────────────────
# Cobre todos os ranges privados que um ataque de DNS Rebinding pode explorar.
_BLOCKED_NETWORKS = [
    ipaddress.ip_network('10.0.0.0/8'),      # Classe A / rede corporativa
    ipaddress.ip_network('172.16.0.0/12'),   # Classe B
    ipaddress.ip_network('192.168.0.0/16'),  # Classe C
    ipaddress.ip_network('127.0.0.0/8'),     # Loopback
    ipaddress.ip_network('169.254.0.0/16'),  # Link-local (RFC 3927)
]

def _is_corporate_lan(ip_obj: ipaddress.IPv4Address) -> bool:
    """Retorna True se o IP pertence à rede corporativa (10.0.0.0/8)."""
    return ip_obj in ipaddress.ip_network('10.0.0.0/8')

def _is_private_ip(ip_obj: ipaddress.IPv4Address) -> bool:
    """Retorna True se o IP pertence a qualquer faixa privada/reservada."""
    return any(ip_obj in net for net in _BLOCKED_NETWORKS)
# ─────────────────────────────────────────────────────────────────────────────


def _collect_tls(host: str, scheme: str, silent: bool):
    """
    Coleta informações TLS de forma leve.
    Usada tanto no caminho normal quanto no caminho rápido da Allowlist,
    onde serve apenas como evidência sem disparar análise de risco.
    Retorna dict com version/issuer/days_left ou None se não for HTTPS.
    """
    if scheme != "https":
        return None
    try:
        sslinfo = get_ssl_info(host, 443)
        if sslinfo["connected"]:
            if not silent:
                print(f"{GREEN}TLS:{RESET} {sslinfo.get('tls_version')} | Emissor: {sslinfo.get('issuer')}")
            return {
                "version":   sslinfo.get("tls_version"),
                "issuer":    sslinfo.get("issuer"),
                "days_left": sslinfo.get("cert_days_left"),
            }
    except Exception:
        pass
    return None


def _run_virustotal(url: str, vt_api_key: str, silent: bool):
    """
    Executa consulta ao VirusTotal e imprime resumo no terminal.
    Retorna o dict de resultado ou None se a chave não foi fornecida.
    Extraído como helper para ser chamado nos dois caminhos (allowlist e normal).
    """
    if not vt_api_key:
        return None
    if not silent:
        info("Consultando VirusTotal... Aguarde.")
    try:
        vt_result = scan_url_virustotal(url, vt_api_key)
        if not silent:
            if vt_result.get("status") == "ok":
                mal = vt_result.get("malicious", 0)
                sus = vt_result.get("suspicious", 0)
                tot = vt_result.get("total", 0)
                if mal > 0 or sus > 0:
                    warn(f"VirusTotal: {mal} malicioso(s) + {sus} suspeito(s) de {tot} engines.")
                else:
                    good(f"VirusTotal: 0 detecções em {tot} engines.")
            elif vt_result.get("status") == "queued":
                warn(f"VirusTotal: análise ainda em fila. {vt_result.get('error', '')}")
            else:
                warn(f"VirusTotal: {vt_result.get('error', 'Erro desconhecido')}")
        return vt_result
    except Exception as e:
        if not silent:
            warn(f"VirusTotal ignorado: {e}")
        return {"status": "error", "error": str(e)}


def scan_single_page(url: str, timeout=12, js_fetch_limit=10, silent=False,
                     vt_api_key: str = ""):

    url    = normalize_url(url)
    parsed = urlparse(url)
    host, scheme = parsed.hostname, parsed.scheme

    # Findings vazios — preenchidos apenas no caminho de análise completa.
    findings = {
        "domain_age_days": None,
        "http_only": False, "hsts_missing": False, "weak_csp": [],
        "sec_headers_missing": [], "cookies_weak": [], "mixed_content": [],
        "forms_insecure": [], "js_suspicious": [], "external_js_no_sri": [],
        "cert_invalid": False, "cert_expiring_soon": False,
        "notes": [], "redirect_note": None,
    }

    if not silent: info(f"Alvo: {url}")

    # ── 1. DETECÇÃO PRECOCE: CREDENTIAL SPOOFING via @ ───────────────────────
    # Verificação pré-conexão — a URL pode conter @ para enganar a leitura.
    # Ex: https://google.com.br@evil.run.app — o domínio REAL é evil.run.app.
    at_in_netloc = "@" in (urlparse(url).netloc or "")
    if at_in_netloc:
        real_host = (urlparse(url).hostname or "").lower()
        fake_part = urlparse(url).netloc.split("@")[0]
        if not silent:
            warn("CREDENTIAL SPOOFING DETECTADO!")
            warn(f"  Parte falsa (antes do @): {fake_part}")
            warn(f"  Domínio REAL da conexão:  {real_host}")

    # ── 2. RESOLUÇÃO DNS + BLOQUEIO DE IP PRIVADO ────────────────────────────
    dns_failed = False
    try:
        ip     = socket.gethostbyname(host)
        ip_obj = ipaddress.ip_address(ip)
        if not silent: good(f"Host: {host} -> IP: {ip}")

        if _is_private_ip(ip_obj):
            if _is_corporate_lan(ip_obj):
                if not silent: warn(f"IP de Rede Local detetado: {ip}. Varredura abortada.")
                return {
                    "url": url, "final_url": url,
                    "status": "LAN CORPORATIVA",
                    "headers_sec": {}, "cookies": [], "findings": findings,
                    "score": 0, "level": "INFO",
                    "action": "[LAN] ATIVO INTERNO. Analise ignorada.",
                    "response_time": 0, "tls_data": None, "virustotal": None,
                }
            else:
                # Faixa privada fora da corporativa — possível DNS Rebinding
                if not silent: err(f"IP Privado Externo detetado: {ip} (fora do escopo corporativo).")
                findings["notes"].append(
                    f"O domínio aponta para o IP privado {ip}, que não pertence à "
                    f"infraestrutura corporativa. Possível ataque de DNS Rebinding "
                    f"(RFC 1918 / RFC 3927)."
                )
                return {
                    "url": url, "final_url": url,
                    "status": "IP SUSPEITO",
                    "headers_sec": {}, "cookies": [], "findings": findings,
                    "score": 100, "level": "CRÍTICO",
                    "action": "[CRITICO] IP PRIVADO DESCONHECIDO. Possivel ataque de DNS Rebinding.",
                    "response_time": 0, "tls_data": None, "virustotal": None,
                }

    except Exception as e:
        dns_failed = True
        if not silent: warn(f"Falha DNS (site inexistente ou sem rede): {e}")

    # ── 3. ALLOWLIST: CAMINHO RÁPIDO ─────────────────────────────────────────
    # Domínios confiáveis não precisam de fetch, análise de HTML/JS/cookies
    # ou pipeline anti-phishing. Esses processamentos geram ruído em sites
    # legítimos e representam trabalho desnecessário para o analista.
    #
    # O que é coletado aqui:
    #   - TLS: evidência leve e útil (versão, emissor, validade do cert)
    #   - VirusTotal: confirmação externa de reputação — a única evidência
    #     que pode surpreender (ex: domínio confiável comprometido recentemente)
    if is_trusted_domain(host):
        if not silent: good(f"Domínio na Allowlist: {host}. Análise de conteúdo ignorada.")

        tls_data  = _collect_tls(host, scheme, silent)
        vt_result = _run_virustotal(url, vt_api_key, silent)

        findings["notes"].append(
            "Domínio presente na Allowlist interna. "
            "Análise de conteúdo ignorada — apenas TLS e evidência VT coletados."
        )

        return {
            "url": url, "final_url": url,
            "status": "ALLOWLIST",
            "headers_sec": {}, "cookies": [], "findings": findings,
            "score": 0, "level": "BAIXO",
            "action": "[OK] DOMINIO CONFIAVEL (ALLOWLIST). Risco mitigado por reputacao conhecida.",
            "response_time": 0,
            "tls_data":   tls_data,
            "virustotal": vt_result,
        }

    # ── 4. ANÁLISE COMPLETA (domínios fora da Allowlist) ─────────────────────

    # TLS / Cert — análise completa incluindo flags de risco
    tls_data = None
    if not dns_failed and scheme == "https":
        try:
            sslinfo = get_ssl_info(host, 443)
            if sslinfo["connected"]:
                tls_data = {
                    "version":   sslinfo.get("tls_version"),
                    "issuer":    sslinfo.get("issuer"),
                    "days_left": sslinfo.get("cert_days_left"),
                }
                if not silent:
                    print(f"{GREEN}TLS:{RESET} {sslinfo.get('tls_version')} | Emissor: {sslinfo.get('issuer')}")
                if not sslinfo.get("verified"):
                    findings["cert_invalid"] = True
                    if not silent: warn("Certificado inválido ou autoassinado.")
                if sslinfo.get("cert_days_left") is not None and sslinfo["cert_days_left"] <= 30:
                    findings["cert_expiring_soon"] = True
            else:
                findings["cert_invalid"] = True
        except Exception:
            findings["cert_invalid"] = True
    elif scheme != "https":
        findings["http_only"] = True
        if not silent: warn("HTTP puro detetado. Risco elevado de interceção.")

    # Fetch da página
    try:
        start_time = time.time()
        final_url, status, headers, body = http_fetch(url, method="GET", timeout=timeout)
        response_time = round((time.time() - start_time) * 1000)

        if not silent: print(f"{GREEN}Status:{RESET} HTTP {status} ({response_time}ms)")
        if final_url != url:
            findings["redirect_note"] = f"Redirecionamento: {url} -> {final_url}"

    except Exception as e:
        if not silent: err(f"Servidor inacessível ou bloqueado: {e}")

        # Mesmo offline, analisa a URL para detectar domínios suspeitos
        try:
            from .antiphishing import analyze_phishing as _ap
            pre         = _ap(initial_url=url, final_url=url, headers=None, html="")
            pre_score   = pre["score"]
            pre_reasons = pre["reasons"]

            if scheme != "https":
                pre_score = min(100, pre_score + 20)

            if pre_score >= 75:
                pre_level  = "CRÍTICO"
                pre_action = "[CRITICO] DOMINIO INACESSIVEL - Alto risco de phishing. Bloqueio recomendado."
            elif pre_score >= 40:
                pre_level  = "MÉDIO"
                pre_action = "[MEDIO] DOMINIO INACESSIVEL - URL com caracteristicas suspeitas. Monitorar."
            else:
                pre_level  = "INACESSÍVEL"
                pre_action = "[INFO] INACESSIVEL. Dominio offline, inexistente ou bloqueado."

            for r in pre_reasons:
                findings["notes"].append(f"[Pré-análise URL] {r}")

            if not silent and pre_reasons:
                warn(f"Score pré-conexão: {pre_score} | {', '.join(pre_reasons[:3])}")

        except Exception:
            pre_score  = 0
            pre_level  = "INACESSÍVEL"
            pre_action = "[INFO] INACESSIVEL. Dominio offline, inexistente ou bloqueado."

        return {
            "url": url, "final_url": url, "status": "OFFLINE / BLOCKED",
            "headers_sec": {}, "cookies": [], "findings": findings,
            "score": pre_score, "level": pre_level, "action": pre_action,
            "response_time": 0, "tls_data": None, "virustotal": None,
        }

    # Whois Domain Age
    findings["domain_age_days"] = check_domain_age(final_url)
    if not silent and findings["domain_age_days"] is not None:
        info(f"Idade do Domínio: {findings['domain_age_days']} dias")

    # Headers e Cookies
    sec_map, header_notes = analyze_security_headers(headers)
    for h, v in sec_map.items():
        if v is None: findings["sec_headers_missing"].append(h)

    if "Strict-Transport-Security" not in headers and scheme == "https":
        findings["hsts_missing"] = True
    findings["weak_csp"].extend(header_notes)

    cookies = parse_set_cookies(headers)
    for ck in cookies:
        flags = [f for f, cond in [("Secure", not ck["secure"]), ("HttpOnly", not ck["httponly"])] if cond]
        if flags: findings["cookies_weak"].append({"cookie": ck["name"], "issues": flags})

    # Análise de HTML
    html = decode_body(headers, body) if body else ""
    if html:
        html_lower = html.lower()

        # Página de bloqueio de proxy corporativo
        PROXY_SIGNATURES = [
            "forcepoint", "websense", "blockpage.cgi", "ws_block.cgi",
            "content blocked by your organization", "this category is blocked",
            "bluecoat", "symantec web gateway", "mcafee web gateway",
            "cisco umbrella", "zscaler",
        ]
        if any(sig in html_lower for sig in PROXY_SIGNATURES):
            if not silent: warn("Página de bloqueio de proxy corporativo detetada.")
            return {
                "url": url, "final_url": final_url,
                "status": f"PROXY BLOCK (HTTP {status})",
                "headers_sec": sec_map, "cookies": cookies, "findings": findings,
                "score": 0, "level": "INACESSÍVEL",
                "action": "[INFO] BLOQUEADO PELO PROXY. Assinatura de proxy corporativo identificada.",
                "response_time": response_time, "tls_data": tls_data, "virustotal": None,
            }

        findings["mixed_content"].extend(find_mixed_content(html, final_url))

        # Forms
        forms = extract_forms(html)
        for f in forms:
            issues     = []
            dst_action = f["action"].lower()
            if f["password"] and f["method"] == "GET":
                issues.append("Senha via GET.")
            if final_url.startswith("https://") and f["action"].startswith("http://"):
                issues.append("Downgrade HTTP.")
            for pat in EXFILTRATION_PATTERNS:
                if re.search(pat, dst_action):
                    issues.append(f"Exfiltração suspeita detetada no form action: {pat}")
            if issues:
                findings["forms_insecure"].append({"method": f["method"], "action": f["action"], "issues": issues})

        # Scripts inline e externos
        inline_js, external_js = extract_scripts(html, final_url)
        for code in inline_js:
            findings["js_suspicious"].extend(scan_js_code(code, final_url))
        for su, code in fetch_external_scripts(external_js, limit=js_fetch_limit, timeout=8).items():
            if code:
                findings["js_suspicious"].extend([f"{su}: {x}" for x in scan_js_code(code, final_url)])

    # Score de infraestrutura / headers
    score, level, action = compute_risk_score(findings)

    # Pipeline anti-phishing
    try:
        phishing = analyze_phishing(
            initial_url=url,
            final_url=final_url,
            headers=headers,
            html=html or ""
        )
        if phishing["reasons"]:
            combined_score = min(100, score + phishing["score"])
            if combined_score > score:
                score = combined_score
                if not silent:
                    info(f"Anti-phishing score: {phishing['score']} | Score combinado: {score}")
                for reason in phishing["reasons"]:
                    if reason not in findings["notes"]:
                        findings["notes"].append(f"[Anti-Phishing] {reason}")
                if score >= 75:
                    level  = "CRÍTICO"
                    action = "[CRITICO] BLOQUEIO RECOMENDADO. Forte indicativo de Phishing."
                elif score >= 40:
                    level  = "MÉDIO"
                    action = "[MEDIO] REQUER ANALISE MANUAL. Infraestrutura suspeita."
    except Exception as e:
        if not silent: warn(f"Pipeline anti-phishing ignorado: {e}")

    # VirusTotal — só chega aqui quem não está na Allowlist
    vt_result = _run_virustotal(url, vt_api_key, silent)

    return {
        "url": url, "final_url": final_url, "status": status,
        "headers_sec": sec_map, "cookies": cookies, "findings": findings,
        "score": score, "level": level, "action": action,
        "response_time": response_time,
        "tls_data":   tls_data,
        "virustotal": vt_result,
    }