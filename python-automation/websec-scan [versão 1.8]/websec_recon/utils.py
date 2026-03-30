#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilidades: estilo terminal, HTTP, TLS, parsing e heurísticas de segurança.
"""

import re
import ssl
import json
import socket
from datetime import datetime
from urllib.parse import urlparse, urljoin
import urllib.request
import urllib.error

def _try_import_whois():
    """Tenta importar whois em runtime — captura instalações feitas no mesmo boot."""
    try:
        import whois as _w
        return True, _w
    except ImportError:
        return False, None

WHOIS_AVAILABLE, _whois_module = _try_import_whois()

# ==========================
# Paleta de Cores Corporativa 
# ==========================
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

BLUE = "\033[94m"        
LIGHT_BLUE = "\033[96m"  
YELLOW = "\033[93m"      
RED = "\033[91m"         

GREEN = LIGHT_BLUE
CYAN = LIGHT_BLUE

UA = "WebSecRecon/1.0 (+security research; educational) Python-urllib"

import sys
import time
import os
import platform

# Controla se a sequência de boot já foi exibida nesta sessão
_BOOT_SHOWN = False

def _boot_sequence():
    """Sequência de inicialização visual — exibida apenas uma vez por sessão."""
    global _BOOT_SHOWN
    if _BOOT_SHOWN:
        return
    _BOOT_SHOWN = True

    import socket as _socket

    print(f"\n{BLUE}{'-' * 68}{RESET}")

    py_ver   = platform.python_version()
    os_name  = platform.system()
    hostname = _socket.gethostname()
    now      = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")

    print(f"{DIM}  HOST{RESET}  {BOLD}{hostname}{RESET}   "
          f"{DIM}OS{RESET} {os_name}   "
          f"{DIM}Python{RESET} {py_ver}   "
          f"{DIM}CSIRT Edition v1.8{RESET}")
    print(f"{DIM}  {'-' * 64}{RESET}\n")

    # Checagem de módulos — sem \r para evitar crash em terminais não-raw
    modules = [
        ("Whois / Domain Age",        WHOIS_AVAILABLE),
        ("TLS / Certificate Engine",  True),
        ("HTTP Engine",               True),
        ("Pattern Matching",          True),
        ("Network Layer",             True),
    ]

    for label, available in modules:
        time.sleep(0.08)
        if available:
            icon = f"{LIGHT_BLUE}[ + ]{RESET}"
            txt  = f"{LIGHT_BLUE}OK{RESET}"
        else:
            icon = f"{YELLOW}[ ! ]{RESET}"
            txt  = f"{YELLOW}AUSENTE{RESET}"
        print(f"  {icon}  {label:<32} {txt}")

    if not WHOIS_AVAILABLE:
        print(f"\n  {YELLOW}[!]{RESET} {DIM}python-whois ausente — "
              f"análise de idade de domínio desativada.{RESET}")

    print(f"\n{BLUE}{'-' * 68}{RESET}")
    print(f"  {DIM}{now}{RESET}  "
          f"{BOLD}Sistema pronto.{RESET}  "
          f"{DIM}Aguardando URL...{RESET}")
    print(f"{BLUE}{'-' * 68}{RESET}\n")
    time.sleep(0.2)


def banner():
    art = f"""\n{BLUE}{BOLD}
______________ _____       ______ _____                    ________                         
___  __ \__  /____(_)_________  /____(_)_____________ _    __  ___/___________ _______      
__  /_/ /_  __ \_  /__  ___/_  __ \_  /__  __ \_  __ `/    _____ \_  ___/  __ `/_  __ \     
_  ____/_  / / /  / _(__  )_  / / /  / _  / / /  /_/ /     ____/ // /__ / /_/ /_  / / /     
/_/     /_/ /_//_/  /____/ /_/ /_//_/  /_/ /_/_\__, /      /____/ \___/ \__,_/ /_/ /_/      
                                              /____/                                                                                                                                                      
{RESET}
{DIM}    -------------------------------------------------------------{RESET}
{DIM}            WebSec Scanner  ·  CSIRT Edition  ·  v1.8{RESET}
{DIM}    -------------------------------------------------------------{RESET}
"""
    print(art)
    _boot_sequence()

# Indicadores visuais limpos
def green(msg): print(f"{LIGHT_BLUE}{msg}{RESET}")
def info(msg): print(f"{LIGHT_BLUE}[i]{RESET} {msg}")
def good(msg): print(f"{BLUE}[+]{RESET} {msg}")
def warn(msg): print(f"{YELLOW}[!]{RESET} {msg}")
def err(msg): print(f"{RED}[x]{RESET} {msg}")

def normalize_url(u: str) -> str:
    u = (u or "").strip()
    if not u:
        return u
    p = urlparse(u)
    if not p.scheme:
        u = "https://" + u
    return u

def build_opener():
    handlers = [urllib.request.HTTPRedirectHandler()]
    opener = urllib.request.build_opener(*handlers)
    opener.addheaders = [("User-Agent", UA), ("Accept", "*/*")]
    return opener

def http_fetch(url, method="GET", timeout=12):
    opener = build_opener()
    req = urllib.request.Request(url, method=method)
    try:
        resp = opener.open(req, timeout=timeout)
        final_url = resp.geturl()
        headers = resp.headers
        status = getattr(resp, "status", 200)
        body = resp.read() if method != "HEAD" else b""
        return final_url, status, headers, body
    except urllib.error.HTTPError as e:
        return url, e.code, e.headers, e.read() if e.fp else b""
    except urllib.error.URLError as e:
        raise e

def decode_body(headers, body_bytes):
    ctype = headers.get("Content-Type", "") if headers else ""
    charset = "utf-8"
    m = re.search(r"charset=([A-Za-z0-9_\-]+)", ctype, re.I)
    if m:
        charset = m.group(1).strip()
    try:
        return body_bytes.decode(charset, errors="ignore")
    except:
        return body_bytes.decode("utf-8", errors="ignore")

# ==========================
# TLS / Certificado
# ==========================

def get_ssl_info(host, port=443, timeout=8):
    info = {
        "connected": False, "verified": False, "tls_version": None,
        "cipher": None, "cert": None, "cert_valid_until": None,
        "cert_days_left": None, "issuer": None, "subject": None,
        "sans": [], "error": None,
    }

    def parse_cert(cert_dict):
        if not cert_dict:
            return
        info["cert"] = True
        not_after = cert_dict.get("notAfter")
        if not_after:
            try:
                dt = datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
                info["cert_valid_until"] = dt
                info["cert_days_left"] = (dt - datetime.utcnow()).days
            except Exception:
                pass

        def flatten_name(name_tuple):
            parts = [f"{k}={v}" for rdn in name_tuple for (k, v) in rdn]
            return ", ".join(parts) if parts else None

        info["issuer"]  = flatten_name(cert_dict.get("issuer", ()))
        info["subject"] = flatten_name(cert_dict.get("subject", ()))
        sans = cert_dict.get("subjectAltName", [])
        info["sans"] = [v for (k, v) in sans if k.lower() == "dns"]

    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((host, port), timeout=timeout) as sock:
            with ctx.wrap_socket(sock, server_hostname=host) as ssock:
                info["connected"] = True
                info["verified"] = True
                info["tls_version"] = ssock.version()
                info["cipher"] = ssock.cipher()[0] if ssock.cipher() else None
                parse_cert(ssock.getpeercert())
                return info
    except Exception as e_verified:
        info["error"] = str(e_verified)

    try:
        ctx = ssl._create_unverified_context()
        with socket.create_connection((host, port), timeout=timeout) as sock:
            with ctx.wrap_socket(sock, server_hostname=host) as ssock:
                info["connected"] = True
                info["tls_version"] = ssock.version()
                info["cipher"] = ssock.cipher()[0] if ssock.cipher() else None
                parse_cert(ssock.getpeercert())
                return info
    except Exception as e_unverified:
        info["error"] = info["error"] or str(e_unverified)

    return info

# ==========================
# Checks de Segurança & Phishing
# ==========================

SEC_HEADERS = [
    "Strict-Transport-Security", "Content-Security-Policy",
    "X-Content-Type-Options", "X-Frame-Options", "Referrer-Policy",
    "Permissions-Policy", "Cross-Origin-Opener-Policy",
    "Cross-Origin-Embedder-Policy", "Cross-Origin-Resource-Policy",
]

SUSPICIOUS_JS_PATTERNS = [
    r"\beval\s*\(", r"\bnew\s+Function\s*\(", r"\batob\s*\(",
    r"\bdocument\.write\s*\(", r"_0x[a-f0-9]{4,}", r"(payload|cmd|token|key)=",
    r"\bsendBeacon\s*\(", r"\bXMLHttpRequest\s*\(", r"\bfetch\s*\(\s*['\"]http",
    r"\bsetTimeout\s*\(\s*['\"].+['\"],\s*\d+\s*\)",
]

EXFILTRATION_PATTERNS = [
    r"api\.telegram\.org", r"discord\.com/api/webhooks", r"formspree\.io",
    r"([0-9]{1,3}\.){3}[0-9]{1,3}" 
]

BASE64_LONG = re.compile(r"\b[A-Za-z0-9+/]{60,}={0,2}\b")

# ==========================
# Allowlist Corporativa (Domínios Seguros)
# ==========================

# Subdomínios legítimos, mas frequentemente abusados para hospedar Phishing
DANGEROUS_SUBDOMAINS = {
    "sites.google.com",
    "script.google.com",
    "drive.google.com",
    "forms.microsoft.com",
    "sway.office.com",
    "sway.cloud.microsoft"
}

TRUSTED_DOMAINS = [
    # 1. Ecossistema Corporativo (exemplo)
    "hyundai.com",
    "hyundai.com.br",
    "hyundai.co.kr",
    "hyundai.eu",
    "hyundai-autoever.com",
    "hyundai-autoever.com.br",
    "hyundai-autoever.eu",

    # 2. Big Techs e Serviços Confiáveis
    "google.com",
    "google.com.br",
    "youtube.com",
    "microsoft.com",
    "apple.com",
    "amazon.com",
    "github.com",
    "linkedin.com",
    "mozilla.org",           

    # 3. Provedores de Identidade (SSO/MFA)
    "okta.com",
    "auth0.com",
    "pingidentity.com",
    "microsoftonline.com",

    # 4. CDNs e Analytics Comuns
    "adobedtm.com",
    "cloudflare.com",
    "akamaihd.net",
    "cdnjs.cloudflare.com",
    "cdn.jsdelivr.net",
    "unpkg.com",

    # 5. SDKs de terceiros legítimos — evitam falsos positivos de JS suspeito
    "geocomply.com",          
    "cookielaw.org",          
    "onetrust.com",           
    "googletagmanager.com",   
    "google-analytics.com",   
    "doubleclick.net",        
    "hotjar.com",             
    "clarity.ms",             
    "segment.com",            
    "amplitude.com",          
    "cdn.tailwindcss.com",    
    "jsdelivr.net",           

    # 6. Sites de apostas regulados no Brasil (evita MÉDIO em sites legítimos)
    "betano.bet.br",
    "bet365.com",
    "sportingbet.com.br",
    "pixbet.com",
    "blaze.com",
    "estrela.bet.br",

    # 7. E-commerce brasileiro legítimo com headers fracos (evita MÉDIO em sites conhecidos)
    "olx.com.br",
    "mercadolivre.com.br",
    "mercadopago.com.br",
    "shopee.com.br",
    "americanas.com.br",
    "submarino.com.br",
    "magazineluiza.com.br",

    # 8. Portais de midia/conteudo brasileiros legitimos
    # Headers fracos e JS de publicidade (eval/atob/doubleclick) sao normais nesses dominios
    "uol.com.br",
    "jsuol.com.br",
    "tab.uol.com.br",
    "globo.com",
    "g1.globo.com",
    "r7.com",
    "terra.com.br",
    "ig.com.br",
    "folha.uol.com.br",
    "estadao.com.br",
    "abril.com.br",

    # 9. Segurança, Cloud e Desenvolvimento
    "aws.amazon.com",         
    "python.org",             
    "linuxmint.com",          
    "owasp.org",              
    "virustotal.com",         
    "stackoverflow.com",      

    # 10. Comunicação, Colaboração e ITSM Corporativo
    "zoom.us",
    "webex.com",
    "slack.com",
    "atlassian.net",
    "servicenow.com",
    "zendesk.com",

    # 11. Fornecedores de Cibersegurança e Infraestrutura de Rede
    "cisco.com",
    "paloaltonetworks.com",
    "fortinet.com",
    "crowdstrike.com",
    "kaspersky.com"
]

def is_trusted_domain(domain):
    """
    Verifica se o domínio faz parte da Allowlist principal,
    mas bloqueia subdomínios conhecidos por hospedar phishing.
    Também perdoa automaticamente domínios governamentais brasileiros (.gov.br).
    """
    if not domain: 
        return False
    
    domain = domain.lower()

    # 1. Se for um subdomínio perigoso, falha a allowlist imediatamente
    if domain in DANGEROUS_SUBDOMAINS:
        return False
    
    # 2. Regra universal para sites do governo brasileiro
    if domain.endswith(".gov.br"):
        return True
        
    # 3. Verifica a Allowlist
    for trusted in TRUSTED_DOMAINS:
        if domain == trusted or domain.endswith("." + trusted):
            return True
            
    return False

def check_domain_age(url):
    """Retorna a idade do domínio em dias. Requer python-whois."""
    global WHOIS_AVAILABLE, _whois_module

    # Tenta importar novamente caso tenha sido instalado após o início
    if not WHOIS_AVAILABLE:
        WHOIS_AVAILABLE, _whois_module = _try_import_whois()

    if not WHOIS_AVAILABLE or _whois_module is None:
        return None

    try:
        hostname = urlparse(url).netloc.lower().split(":")[0]

        TWO_LEVEL_TLDS = {
            "com.br", "org.br", "gov.br", "net.br", "edu.br",
            "co.uk", "org.uk", "gov.uk", "me.uk",
            "com.ar", "com.au", "co.au", "com.mx",
        }
        parts = hostname.split(".")
        if len(parts) >= 3 and ".".join(parts[-2:]) in TWO_LEVEL_TLDS:
            domain = ".".join(parts[-3:])
        elif len(parts) >= 2:
            domain = ".".join(parts[-2:])
        else:
            domain = hostname

        w = _whois_module.whois(domain)
        creation_date = w.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        if creation_date:
            return (datetime.now() - creation_date).days
    except Exception:
        return None
    return None

def analyze_security_headers(headers):
    results = {h: headers.get(h) for h in SEC_HEADERS}
    notes = []
    if not results["Strict-Transport-Security"]:
        notes.append("HSTS ausente.")
    csp = results["Content-Security-Policy"]
    if not csp:
        notes.append("CSP ausente (risco de XSS/Exfiltração).")
    else:
        if "unsafe-inline" in csp or "unsafe-eval" in csp:
            notes.append("CSP fraca (unsafe-inline/eval).")
    if headers.get("X-Content-Type-Options", "").lower() != "nosniff":
        notes.append("X-Content-Type-Options ausente/incorreto.")
    return results, notes

def parse_set_cookies(headers):
    cookies_raw = headers.get_all("Set-Cookie") or []
    parsed = []
    for ck in cookies_raw:
        flags = {"name": None, "secure": False, "httponly": False, "samesite": None, "host_prefix": False}
        parts = [p.strip() for p in ck.split(";")]
        if parts:
            name_val = parts[0]
            if "=" in name_val:
                flags["name"] = name_val.split("=", 1)[0]
                if flags["name"].startswith("__Host-"):
                    flags["host_prefix"] = True
        for p in parts[1:]:
            k = p.lower()
            if k == "secure": flags["secure"] = True
            elif k == "httponly": flags["httponly"] = True
            elif k.startswith("samesite"):
                kv = p.split("=", 1)
                if len(kv) == 2: flags["samesite"] = kv[1].strip()
        parsed.append(flags)
    return parsed

def find_mixed_content(html, base_url):
    issues = []
    if not html or not str(base_url).startswith("https://"): return issues
    for m in re.finditer(r"""(?:src|href)\s*=\s*['"](http://[^'"]+)['"]""", html, re.I):
        issues.append(f"Recurso inseguro: {m.group(1)}")
    return list(dict.fromkeys(issues))

def extract_forms(html):
    forms = []
    if not html: return forms
    for m in re.finditer(r"<form\b([^>]*)>(.*?)</form>", html, re.I | re.S):
        attrs, body = m.group(1) or "", m.group(2) or ""
        method = (re.search(r"""method\s*=\s*["']?([A-Za-z]+)""", attrs, re.I) or [None, "GET"])[1].upper()
        action = (re.search(r"""action\s*=\s*["']([^"']+)["']""", attrs, re.I) or [None, ""])[1].strip()
        
        forms.append({
            "method": method,
            "action": action,
            "password": bool(re.search(r"""type\s*=\s*['"]password['"]""", body, re.I)),
            "email": bool(re.search(r"""type\s*=\s*['"]email['"]""", body, re.I))
        })
    return forms

def extract_scripts(html, base_url):
    inline, external = [], []
    if not html: return inline, external
    for m in re.finditer(r"""<script[^>]+src=['"]([^'"]+)['"][^>]*>""", html, re.I):
        src = (m.group(1) or "").strip()
        if not src.lower().startswith("http"): src = urljoin(base_url, src)
        external.append(src)
    for m in re.finditer(r"""<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>""", html, re.I | re.S):
        code = (m.group(1) or "").strip()
        if code: inline.append(code)
    return inline, external

def scan_js_code(snippet, page_origin):
    issues = []
    for pat in SUSPICIOUS_JS_PATTERNS:
        if re.search(pat, snippet, re.I): issues.append(f"JS suspeito: /{pat}/")
    
    if BASE64_LONG.search(snippet) and "atob" in snippet:
        issues.append("Possível payload base64 longo com atob().")
        
    for m in re.finditer(r"""(?:fetch|sendBeacon|XMLHttpRequest)\s*\(\s*(['"])(https?://[^'"]+)\1""", snippet, re.I):
        url = m.group(2)
        if urlparse(url).netloc and urlparse(url).netloc != urlparse(page_origin).netloc:
            issues.append(f"Exfiltração/Request externo: {url}")
            
    if re.search(r"(password|senha|pwd|pass).*\.value", snippet, re.I):
        if not re.search(r"(crypto|hash|sha|bcrypt|pbkdf2|encrypt)", snippet, re.I):
            issues.append("[CRITICO] Script manipula valor de campo de senha sem evidência de hash/criptografia no frontend.")    
            
    return issues

def fetch_external_scripts(urls, limit=10, timeout=8):
    fetched, opener = {}, build_opener()
    for u in list(dict.fromkeys(urls))[:limit]:
        try:
            resp = opener.open(urllib.request.Request(u, method="GET"), timeout=timeout)
            fetched[u] = decode_body(resp.headers, resp.read())
        except: fetched[u] = None
    return fetched

def compute_risk_score(findings):
    raw_score = 0

    # Infraestrutura base
    if findings.get("http_only"):     raw_score += 20
    if findings.get("cert_invalid"):  raw_score += 40
    if findings.get("hsts_missing"):  raw_score += 5

    # Headers de segurança ausentes
    # Pesos calibrados: headers críticos (HSTS, CSP, X-Content-Type) têm peso alto.
    # Headers avançados (COEP, COOP, CORP, Permissions-Policy) têm peso reduzido —
    # são raros mesmo em sites legítimos e geravam falsos positivos em portais de mídia.
    HEADER_WEIGHTS = {
        "Strict-Transport-Security":    8,   # crítico — sem ele HTTPS é bypass
        "Content-Security-Policy":      8,   # crítico — XSS/exfiltração
        "X-Content-Type-Options":       6,   # importante — MIME sniffing
        "X-Frame-Options":              4,   # médio — clickjacking
        "Referrer-Policy":              3,   # baixo — vazamento de URL
        "Permissions-Policy":           1,   # raro mesmo em sites legítimos
        "Cross-Origin-Opener-Policy":   1,   # raro mesmo em sites legítimos
        "Cross-Origin-Embedder-Policy": 1,   # raro mesmo em sites legítimos
        "Cross-Origin-Resource-Policy": 1,   # raro mesmo em sites legítimos
    }
    missing_headers = findings.get("sec_headers_missing", [])
    headers_score = sum(HEADER_WEIGHTS.get(h, 1) for h in missing_headers)
    raw_score += min(30, headers_score)  # teto reduzido de 43 para 30pts

    # Formulários inseguros com exfiltração confirmada
    raw_score += 20 * len([f for f in findings.get("forms_insecure", []) if "Exfiltração" in str(f)])

    # JS suspeito — escala calibrada para evitar falsos positivos em portais legítimos.
    # Scripts de publicidade (doubleclick, adnxs, prebid, tagmanager) usam eval/atob/
    # document.write legitimamente. O filtro abaixo descarta itens que sejam apenas
    # padrões genéricos originados de domínios de ads conhecidos.
    AD_DOMAINS = {
        "doubleclick.net", "adnxs.com", "googlesyndication.com",
        "googletagmanager.com", "google-analytics.com", "googletagservices.com",
        "amazon-adsystem.com", "taboola.com", "outbrain.com",
        "rubiconproject.com", "openx.net", "pubmatic.com", "criteo.com",
        "hotjar.com", "clarity.ms", "segment.com", "amplitude.com",
    }
    js_items = findings.get("js_suspicious", [])
    js_score = 0
    for i, item in enumerate(js_items):
        item_str = str(item)
        # Verifica se o item vem de um domínio de publicidade conhecido
        is_ad_domain = any(ad in item_str for ad in AD_DOMAINS)

        if "[CRITICO]" in item_str or "Exfiltração/Request externo" in item_str:
            # Exfiltração para domínio de ads é legítima — não penaliza
            if is_ad_domain:
                js_score += 2
            else:
                js_score += 15
        elif is_ad_domain:
            # Padrão genérico (eval, atob, fetch) em script de publicidade — peso mínimo
            js_score += 1
        elif i < 3:
            js_score += 6   # reduzido de 8 para 6
        else:
            js_score += 1   # reduzido de 2 para 1
    raw_score += min(35, js_score)  # teto reduzido de 40 para 35

    # Idade do domínio
    domain_age = findings.get("domain_age_days")
    if domain_age is not None:
        if domain_age < 15:   raw_score += 60
        elif domain_age < 30: raw_score += 40
        elif domain_age < 90: raw_score += 20

    score = min(100, raw_score)

    if score >= 75:
        level, action = "CRÍTICO", "[CRITICO] BLOQUEIO RECOMENDADO. Forte indicativo de Phishing."
    elif score >= 40:
        level, action = "MÉDIO", "[MEDIO] REQUER ANALISE MANUAL. Infraestrutura suspeita."
    else:
        level, action = "BAIXO", "[OK] RISCO ACEITAVEL. Dominio sem anomalias graves detectadas."

    return score, level, action