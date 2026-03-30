#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Heurísticas corporativas Anti-Phishing.
100% standard library. Sem WHOIS por padrão (usa TLS notBefore como proxy).
"""

import re
import unicodedata  # FIX #3: adicionado para normalização NFKC
from urllib.parse import urlparse

from .utils import get_ssl_info

SUSPICIOUS_TLDS = {
    # TLDs históricos de phishing
    "zip", "mov", "top", "xyz", "click", "country",
    "gq", "ml", "cf", "tk", "work", "rest",
    "cam", "loan", "men", "stream", "bid", "win",
    "party", "faith", "date",
    # TLDs modernos frequentemente abusados no Brasil
    "online", "site", "store", "shop", "digital",
    "live", "cloud", "network", "solutions",
    "info", "biz",
    # Nota: .app não incluído — é TLD legítimo da Apple/Google
    # A detecção de run.app é feita via FREE_HOSTING_PLATFORMS
}

URL_SHORTENERS = {
    "bit.ly","tinyurl.com","goo.gl","ow.ly","t.co","is.gd","buff.ly","cutt.ly","short.ly","adf.ly"
}

PHISHING_KEYWORDS_URL = {
    # Credenciais e acesso
    "login", "signin", "sign-in", "logon", "sso", "oauth", "auth",
    "password", "passwd", "reset", "recover", "unlock", "reactivate",
    "verify", "validate", "confirm", "update", "secure",
    "token", "2fa", "mfa", "otp", "totp",

    # Sistemas corporativos comuns
    "outlook", "office365", "office-365", "sharepoint", "onedrive",
    "teams", "webmail", "intranet", "vpn", "citrix", "rdp",
    "sap", "erp", "workday", "servicenow", "jira", "confluence",

    # Banking corporativo / financeiro
    "account", "banking", "invoice", "payment", "payroll", "wire",
    "transferencia", "transferência", "boleto", "cobranca", "cobrança",
    "fatura", "extrato", "financeiro", "tesouraria",
    "banco", "bank", "bradesco", "itau", "santander", "bb", "caixa",
    "pix", "ted", "doc",

    # Engenharia social corporativa
    "rh", "recursos-humanos", "beneficios", "benefícios", "folha",
    "admissao", "admissão", "demissao", "demissão", "ferias", "férias",
    "holerite", "contracheque", "vale",
    "acesso-negado", "conta-bloqueada", "suspended", "blocked",
    "urgente", "urgente", "atencao", "atenção", "importante",
    "suporte", "helpdesk", "ti-corporativo", "servicedesk",

    # Autenticação / identidade digital gov
    "autenticador", "autenticacao", "autenticação",
    "acesso-gov", "gov-digital", "identidade-digital",
    "certificado-digital", "assinatura-digital",

    # Fiscal / tributário
    "documentos-fiscais", "documentofiscal", "nfe", "nfce",
    "nota-fiscal", "sped", "ecf", "defis",
    "regularizar", "regularizacao", "regularização",
    "debitos", "débitos", "divida", "dívida", "pendencia",
    "parcelamento", "simples-nacional", "mei",

    # Receita / INSS / Gov BR
    "receita-federal", "meu-inss", "e-social",
    "cnis", "sigepe", "conecta-gov", "acesso-gov",
    "serv-gov", "servicos-gov", "portal-gov",
}

PHISHING_KEYWORDS_HTML = {
    # Credenciais
    "senha", "password", "token", "otp", "2fa", "mfa",
    "usuario", "usuário", "username", "login", "acesso",

    # Dados pessoais / corporativos
    "cpf", "cnpj", "matricula", "matrícula",
    "cartao", "cartão", "cvv", "validade",
    "pix", "boleto", "fatura",

    # Engenharia social
    "conta bloqueada", "acesso suspenso", "verificar identidade",
    "atualizar cadastro", "confirmar dados", "prazo", "vencimento",
    "clique aqui", "acesse agora", "urgente", "importante",
    "segurança", "security", "autenticação", "autenticacao",

    # Sistemas corporativos
    "outlook", "office", "sharepoint", "teams", "vpn",
    "sap", "workday", "benefícios", "holerite",
}

# Plataformas de hosting gratuito frequentemente abusadas para phishing.
FREE_HOSTING_PLATFORMS = {
    "run.app",            # Google Cloud Run
    "web.app",            # Firebase Hosting
    "firebaseapp.com",    # Firebase
    "pages.dev",          # Cloudflare Pages
    "netlify.app",        # Netlify
    "vercel.app",         # Vercel
    "github.io",          # GitHub Pages
    "glitch.me",          # Glitch
    "replit.app",         # Replit
    "onrender.com",       # Render
    "pythonanywhere.com", # PythonAnywhere
    "000webhostapp.com",  # 000webhost
    "infinityfreeapp.com",# InfinityFree
}

# Marcas e sistemas corporativos comuns em lookalike/spoofing
BRANDS = {
    # Microsoft (mais visada em phishing corporativo)
    "microsoft", "outlook", "office", "office365", "sharepoint",
    "onedrive", "teams", "azure", "microsoftonline",

    # Google Workspace
    "google", "gmail", "workspace", "drive",

    # Identidade e acesso
    "okta", "auth0", "onelogin", "pingidentity", "duo",

    # Comunicação
    "slack", "zoom", "webex", "whatsapp", "telegram",

    # Bancos corporativos BR
    "itau", "bradesco", "santander", "bancodobrasil", "caixa",
    "nubank", "inter", "sicoob", "sicredi",

    # Bancos internacionais
    "paypal", "citibank", "hsbc", "jpmorgan",

    # Plataformas corporativas
    "sap", "workday", "servicenow", "salesforce", "oracle",
    "totvs", "senior", "protheus",

    # Gov BR
    "receita", "sefaz", "govbr", "previdencia",

    # Outros
    "apple", "amazon", "netflix", "instagram", "facebook",
    "linkedin", "dropbox", "docusign",
}

def get_reg_domain(host: str) -> str:
    """
    Retorna algo próximo do eTLD+1 (simples).
    Trata alguns TLDs de 2 níveis comuns.
    """
    if not host:
        return host
    host = host.lower().strip(".")
    parts = host.split(".")
    if len(parts) <= 2:
        return host
    multi = {"com.br","gov.br","org.br","com.ar","co.uk","com.au","gov.uk"}
    last2 = ".".join(parts[-2:])
    last3 = ".".join(parts[-3:])
    if last2 in multi:
        return ".".join(parts[-3:])
    if last3 in multi:
        return ".".join(parts[-4:])
    return ".".join(parts[-2:])

def levenshtein(a: str, b: str) -> int:
    """Distância de Levenshtein simples."""
    a, b = a.lower(), b.lower()
    if not a: return len(b)
    if not b: return len(a)
    prev = list(range(len(b)+1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            ins = prev[j] + 1
            dele = cur[j-1] + 1
            sub = prev[j-1] + (ca != cb)
            cur.append(min(ins, dele, sub))
        prev = cur
    return prev[-1]

def has_homoglyph_suspects(label: str) -> bool:
    """
    Heurística simples: sequências que imitam letras (rn ≈ m, vv ≈ w, cl ≈ d).
    """
    lab = label.lower()
    patterns = ["rn", "vv", "cl", "li", "i1", "0o", "o0"]
    return any(p in lab for p in patterns)

def analyze_domain(url: str):
    p = urlparse(url)
    host = (p.hostname or "").lower()
    reg = get_reg_domain(host)

    # FIX #3: Normalização Unicode NFKC no host da URL
    # Converte homoglyphs matemáticos/cirílicos para ASCII equivalente antes
    # de qualquer checagem — alinha o comportamento com o email_analyzer.
    # Ex: "mіcrosoft.com" (с cirílico) → "microsoft.com" após NFKC.
    host_normalized = unicodedata.normalize("NFKC", host).lower()
    unicode_homoglyph_in_url = (host_normalized != host)

    # A partir daqui todas as checagens operam no host normalizado
    host = host_normalized
    reg  = get_reg_domain(host)

    # TLD
    tld = host.split(".")[-1] if "." in host else host
    tld_suspicious = tld in SUSPICIOUS_TLDS

    # IDN/punycode e não-ASCII (checagem no host original, antes da normalização)
    original_host = (p.hostname or "").lower()
    is_idn = "xn--" in original_host or (any(ord(c) > 127 for c in original_host))

    # Shortener
    is_shortener = host in URL_SHORTENERS

    # Palavras de isca — escaneia a URL RAW COMPLETA (incluindo parte antes do @)
    url_lower = url.lower()
    bait_words = [w for w in PHISHING_KEYWORDS_URL if w in url_lower]

    # Detecção adicional por tokens
    host_tokens = re.split(r'[\.\-\_]', host)
    for token in host_tokens:
        for kw in PHISHING_KEYWORDS_URL:
            clean_kw = kw.replace("-", "").replace("_", "")
            clean_token = token.replace("-", "").replace("_", "")
            if clean_kw in clean_token and kw not in bait_words:
                bait_words.append(kw)

    # --- CREDENTIAL SPOOFING via @ na URL ---
    credential_spoof = False
    spoofed_brand = None
    at_pos = url.find("@")
    if at_pos != -1:
        scheme_end = url.find("://")
        fake_part = url[scheme_end + 3:at_pos].lower() if scheme_end != -1 else url[:at_pos].lower()
        credential_spoof = True

        fake_tokens = re.split(r'[\.\-\_\/]', fake_part)

        for brand in BRANDS:
            if brand in fake_part:
                spoofed_brand = brand
                break
            if brand in fake_tokens:
                spoofed_brand = brand
                break

        if not spoofed_brand:
            if any(t in fake_part for t in [".com.br", ".gov.br", ".com", ".org"]):
                spoofed_brand = fake_part.split("/")[0]

        for w in PHISHING_KEYWORDS_URL:
            if w in fake_part and w not in bait_words:
                bait_words.append(w)

    # --- HOSTING GRATUITO ABUSADO ---
    is_free_hosting = any(host.endswith(platform) for platform in FREE_HOSTING_PLATFORMS)
    free_hosting_platform = next((p for p in FREE_HOSTING_PLATFORMS if host.endswith(p)), None)

    # Lookalike
    label = reg.split(".")[0]
    lookalike = []
    checked_brands = set()

    all_tokens = re.split(r'[\.\-\_]', host) + [label]

    for token in all_tokens:
        if not token or len(token) < 3:
            continue
        for b in BRANDS:
            if b in checked_brands:
                continue
            if b == token and (host.endswith(f"{b}.com") or host.endswith(f"{b}.com.br")):
                checked_brands.add(b)
                continue
            if token == b:
                lookalike.append(f"{token}={b} (match exato no hostname)")
                checked_brands.add(b)
            elif b in host and len(b) >= 5:
                official_domains = [f"{b}.com", f"{b}.com.br", f"{b}.org", f"{b}.net"]
                is_official = any(host == d or host.endswith(f".{d}") for d in official_domains)
                if not is_official:
                    lookalike.append(f"'{b}' presente no hostname '{host}'")
                    checked_brands.add(b)
            else:
                d = levenshtein(token, b)
                if d == 1 or (d == 2 and len(token) >= 5):
                    lookalike.append(f"{token}~{b} (dist={d})")
                    checked_brands.add(b)

    homo = has_homoglyph_suspects(label)

    return {
        "host": host,
        "reg_domain": reg,
        "tld": tld,
        "tld_suspicious": tld_suspicious,
        "is_idn": is_idn,
        "is_shortener": is_shortener,
        "bait_words": bait_words,
        "lookalike": lookalike,
        "homoglyph_suspect": homo,
        "credential_spoof": credential_spoof,
        "spoofed_brand": spoofed_brand,
        "is_free_hosting": is_free_hosting,
        "free_hosting_platform": free_hosting_platform,
        # FIX #3: expõe o flag para uso no compute_phishing_score
        "unicode_homoglyph_in_url": unicode_homoglyph_in_url,
    }

def analyze_content(url: str, html: str, final_url: str):
    """
    Heurísticas no HTML:
    - formulário com 'password' (especialmente GET ou action externo)
    - termos sensíveis em texto
    - JS bloqueando ações de usuário (leve)
    """
    findings = {
        "password_forms": [],
        "sensitive_terms": [],
        "external_form_actions": [],
        "js_user_block": []
    }
    if not html:
        return findings

    text_lower = html.lower()
    findings["sensitive_terms"] = [w for w in PHISHING_KEYWORDS_HTML if w in text_lower]

    for m in re.finditer(r"<form\b([^>]*)>(.*?)</form>", html, re.I | re.S):
        attrs = m.group(1) or ""
        body = m.group(2) or ""
        has_pwd = bool(re.search(r"""type\s*=\s*['"]password['"]""", body, re.I))
        mm = re.search(r"""method\s*=\s*['"]?([A-Za-z]+)""", attrs, re.I)
        method = (mm.group(1) if mm else "GET").upper()
        ma = re.search(r"""action\s*=\s*['"]([^'"]+)['"]""", attrs, re.I)
        action = ma.group(1) if ma else ""
        if has_pwd:
            findings["password_forms"].append({"method": method, "action": action})
        if action.startswith("http"):
            src_host = urlparse(final_url).netloc
            dst_host = urlparse(action).netloc
            if dst_host and src_host and dst_host != src_host:
                findings["external_form_actions"].append({"method": method, "action": action, "dest": dst_host})

    if re.search(r"oncontextmenu\s*=", html, re.I) or re.search(r"\.preventDefault\s*\(", html, re.I):
        findings["js_user_block"].append("Bloqueio de clique/contexto detectado")

    return findings

def analyze_transport(url: str):
    """
    Checa HTTPS/TLS e usa notBefore (quando disponível) como proxy de idade do domínio.
    """
    p = urlparse(url)
    host = p.hostname
    scheme = p.scheme or "https"
    if scheme != "https":
        return {"https": False, "tls_ok": False, "cert_days_left": None, "cert_days_since_start": None, "verified": False}

    sslinfo = get_ssl_info(host, 443)
    return {
        "https": True,
        "tls_ok": bool(sslinfo.get("connected")),
        "verified": bool(sslinfo.get("verified")),
        "cert_days_left": sslinfo.get("cert_days_left"),
        "cert_days_since_start": sslinfo.get("cert_days_since_start"),
        "tls_version": sslinfo.get("tls_version"),
    }

def compute_phishing_score(domain_info: dict, transport: dict, content: dict, initial_url: str, final_url: str):
    """
    Score opinativo voltado a phishing (0–100+).
    """
    score = 0
    reasons = []

    # FIX #3: Unicode homoglyph na URL — pontuado antes das demais checagens
    # para que o sinal mais forte apareça em primeiro lugar nas razões.
    if domain_info.get("unicode_homoglyph_in_url"):
        score += 25
        reasons.append("Homoglyph Unicode detectado no host da URL (NFKC normalization)")

    # Domínio/TLD/IDN/Shortener
    if domain_info["tld_suspicious"]:
        score += 18; reasons.append(f"TLD suspeito: .{domain_info['tld']}")
    if domain_info["is_idn"]:
        score += 18; reasons.append("Domínio IDN/punycode/não-ASCII")
    if domain_info["is_shortener"]:
        score += 14; reasons.append("URL encurtador")
    if domain_info["bait_words"]:
        bait_count = len(domain_info["bait_words"])
        base_pts = 10 + 2 * bait_count
        score += base_pts
        reasons.append("Palavras de isca na URL: " + ", ".join(domain_info["bait_words"]))

        host_lower = domain_info.get("host", "")
        bait_in_host = [w for w in domain_info["bait_words"]
                        if w.replace("-","").replace("_","") in host_lower.replace("-","").replace("_","").replace(".","")]
        if len(bait_in_host) >= 2:
            bonus = 15 * (len(bait_in_host) - 1)
            score += bonus
            reasons.append(f"Domínio construído com {len(bait_in_host)} termos de isca no hostname — forte indicativo de phishing deliberado")
    if domain_info["lookalike"]:
        score += 20; reasons.append("Possível lookalike de marca: " + ", ".join(domain_info["lookalike"]))
    if domain_info["homoglyph_suspect"]:
        score += 10; reasons.append("Padrões homoglifos suspeitos no rótulo do domínio")

    # --- CREDENTIAL SPOOFING via @ ---
    if domain_info.get("credential_spoof"):
        score += 40
        brand = domain_info.get("spoofed_brand")
        if brand:
            score += 20
            reasons.append(f"🚨 CREDENTIAL SPOOFING: URL usa '@' para simular '{brand}' — domínio real é '{domain_info['host']}'")
        else:
            reasons.append(f"🚨 CREDENTIAL SPOOFING: URL usa '@' para ocultar o domínio real '{domain_info['host']}'")

    # --- HOSTING GRATUITO ABUSADO ---
    if domain_info.get("is_free_hosting"):
        platform = domain_info.get("free_hosting_platform", "plataforma gratuita")
        score += 15
        reasons.append(f"Hospedado em plataforma gratuita frequentemente abusada: {platform}")

    # Transporte / Certificado
    if not transport["https"]:
        score += 30; reasons.append("Sem HTTPS")
    else:
        if not transport["tls_ok"] or not transport["verified"]:
            score += 25; reasons.append("TLS inválido/não verificado")
        days = transport.get("cert_days_since_start")
        if isinstance(days, int):
            if days <= 30:
                score += 22; reasons.append(f"Certificado recente (≈{days} dias) — domínio possivelmente novo")
            elif days <= 90:
                score += 12; reasons.append(f"Certificado relativamente novo (≈{days} dias)")
        left = transport.get("cert_days_left")
        if isinstance(left, int) and left <= 7:
            score += 6; reasons.append("Certificado expirando em ≤7 dias")

    # Conteúdo
    if content["password_forms"]:
        score += 20; reasons.append("Formulário de senha detectado")
        for f in content["password_forms"]:
            if f["method"] == "GET":
                score += 8; reasons.append("Senha enviada via GET (vaza na URL)")
    if content["external_form_actions"]:
        score += 16; reasons.append("Form envia credenciais para domínio externo")
    if content["sensitive_terms"]:
        term_count = len(set(content["sensitive_terms"]))
        if term_count >= 3:
            score += 4
            reasons.append("Pede dados sensíveis: " + ", ".join(sorted(set(content["sensitive_terms"]))))
        elif content["password_forms"] or content["external_form_actions"]:
            score += 4
            reasons.append("Pede dados sensíveis: " + ", ".join(sorted(set(content["sensitive_terms"]))))
    if content["js_user_block"]:
        score += 4; reasons.append("Bloqueios de usuário via JS (leve)")

    # Redirecionamento entre domínios distintos
    init_host = urlparse(initial_url).netloc
    final_host = urlparse(final_url).netloc if final_url else init_host
    init_domain = init_host.split(":")[0].lstrip("www.")
    final_domain = final_host.split(":")[0].lstrip("www.")
    if final_domain and init_domain and final_domain != init_domain:
        score += 10
        reasons.append(f"Redirecionamento entre domínios distintos: {init_host} -> {final_host}")

    # Nível/Veredito
    if score >= 75:
        level = "CRÍTICO"
        verdict = "Provável phishing"
    elif score >= 40:
        level = "MÉDIO"
        verdict = "Potencial phishing"
    else:
        level = "BAIXO"
        verdict = "Baixo risco (monitorar)"

    return score, level, verdict, reasons

def analyze_phishing(initial_url: str, final_url: str, headers, html: str):
    """
    Pipeline de análise anti-phishing.
    """
    domain_info = analyze_domain(final_url or initial_url)
    transport = analyze_transport(final_url or initial_url)
    content = analyze_content(final_url or initial_url, html, final_url or initial_url)

    score, level, verdict, reasons = compute_phishing_score(
        domain_info, transport, content, initial_url, final_url or initial_url
    )

    return {
        "verdict": verdict,
        "level": level,
        "score": score,
        "reasons": reasons,
        "domain": domain_info,
        "transport": transport,
        "content": content,
    }