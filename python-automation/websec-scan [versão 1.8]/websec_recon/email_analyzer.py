#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de análise de remetente de e-mail — CSIRT Edition.
100% standard library. Sem dependências externas.

Vereditos: CONFIÁVEL | SUSPEITO | MALICIOSO

Técnicas cobertas:
    - Unicode Mathematical/Letterlike homoglyphs (𝐆𝟎𝟎𝐆𝐋𝐄 → g00gle via NFKC)
    - Caracteres non-BMP (U+10000+) — sempre suspeito em domínios
    - Punycode / IDN (xn--)
    - Lookalike de marcas via Levenshtein (opera no domínio normalizado)
    - Display Name Spoofing (marca no nome ≠ domínio real)
    - TLDs historicamente abusados
    - Free hosting / provedores gratuitos
    - Domínios externos sem vínculo corporativo
    - Subdomain abuse, dígitos excessivos, hífens
"""

import re
import unicodedata

# ── Allowlist corporativa ─────────────────────────────────────────────────────
EMAIL_ALLOWLIST = {
    "hyundai.com", "autoever.com", "hyundaimotorgroup.com",
    "hyundai.com.br", "mobis.com",
    "microsoft.com", "office365.com", "microsoftonline.com",
    "google.com", "googlemail.com",
    "amazon.com", "amazonaws.com",
    "apple.com",
    "gov.br", "receita.fazenda.gov.br", "serpro.gov.br",
}

SUSPICIOUS_TLDS = {
    "xyz", "top", "click", "country", "gq", "ml", "cf", "tk",
    "work", "rest", "cam", "loan", "men", "stream", "bid", "win",
    "party", "faith", "date", "zip", "mov",
    "online", "site", "store", "shop", "digital", "live", "cloud",
    "network", "solutions", "info", "biz", "icu", "pw", "cc",
}

FREE_EMAIL_PROVIDERS = {
    "gmail.com", "yahoo.com", "hotmail.com", "outlook.com",
    "live.com", "protonmail.com", "proton.me", "tutanota.com",
    "icloud.com", "aol.com", "mail.com", "zoho.com",
    "ymail.com", "msn.com", "bol.com.br", "uol.com.br",
    "terra.com.br", "ig.com.br", "globo.com",
}

FREE_HOSTING_DOMAINS = {
    "run.app", "web.app", "firebaseapp.com", "pages.dev",
    "netlify.app", "vercel.app", "github.io", "glitch.me",
    "replit.app", "onrender.com", "pythonanywhere.com",
    "000webhostapp.com", "infinityfreeapp.com",
}

BRANDS = {
    "microsoft", "outlook", "office", "office365", "sharepoint",
    "onedrive", "teams", "azure", "microsoftonline",
    "google", "gmail", "workspace",
    "okta", "auth0", "onelogin", "duo",
    "slack", "zoom", "webex", "whatsapp", "telegram",
    "itau", "bradesco", "santander", "bancodobrasil", "caixa",
    "nubank", "inter", "sicoob", "sicredi",
    "paypal", "citibank", "hsbc",
    "sap", "workday", "servicenow", "salesforce", "oracle",
    "totvs", "senior", "protheus",
    "receita", "sefaz", "govbr", "previdencia",
    "apple", "amazon", "netflix", "linkedin", "docusign",
    "hyundai", "autoever",
}

DISPLAY_NAME_BAIT = {
    "urgente", "urgent", "importante", "critical", "alerta", "alert",
    "atencao", "aviso", "warning", "notificacao", "security",
    "seguranca", "suporte", "support", "helpdesk", "servicedesk",
    "noreply", "no-reply", "donotreply",
    "financeiro", "tesouraria", "pagamento", "payment", "fatura", "invoice",
    "cobranca", "boleto", "pix", "transferencia",
    "recursos humanos", "rh", "beneficios", "folha", "holerite",
    "admissao", "compliance", "juridico",
    "sistema", "portal", "intranet", "vpn", "acesso", "autenticacao",
    "verificacao",
}

# ── Normalização Unicode ──────────────────────────────────────────────────────

def _normalize_domain(domain):
    had_non_bmp   = any(ord(c) > 0xFFFF for c in domain)
    had_non_ascii = any(ord(c) > 127    for c in domain)
    normalized    = unicodedata.normalize("NFKC", domain).lower().strip(".")
    return normalized, had_non_bmp, had_non_ascii

# ── Helpers ───────────────────────────────────────────────────────────────────

def _parse_email(raw):
    raw = raw.strip()
    m = re.match(r'^(.*?)\s*<([^>]+)>', raw)
    if m:
        return m.group(1).strip().strip('"').strip("'"), m.group(2).strip()
    m = re.match(r'^([^\s(]+@[^\s(]+)\s*\(([^)]+)\)', raw)
    if m:
        return m.group(2).strip(), m.group(1).strip()
    m = re.match(r'^([^\s@]+@[^\s@]+\.[^\s@]+)$', raw)
    if m:
        return "", m.group(1).strip()
    return "", ""

def _extract_domain(email):
    if "@" in email:
        return email.split("@", 1)[1].strip().lower()
    return ""

def _get_tld(domain):
    parts = domain.rstrip(".").split(".")
    return parts[-1] if parts else ""

def _get_reg_domain(domain):
    if not domain:
        return ""
    parts = domain.lower().strip(".").split(".")
    if len(parts) <= 2:
        return domain
    multi = {"com.br", "gov.br", "org.br", "com.ar", "co.uk", "com.au", "gov.uk"}
    last2 = ".".join(parts[-2:])
    if last2 in multi:
        return ".".join(parts[-3:])
    return ".".join(parts[-2:])

def _levenshtein(a, b):
    a, b = a.lower(), b.lower()
    if not a: return len(b)
    if not b: return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j-1] + 1, prev[j-1] + (ca != cb)))
        prev = cur
    return prev[-1]

def _lookalike_brands(domain_norm):
    """
    Detecta lookalike de marcas no domínio normalizado.

    FIX #4: Marcas curtas (< 4 caracteres) são ignoradas na checagem por
    substring para evitar falsos positivos — ex: "sap" dentro de "sapatos.com.br",
    "inter" dentro de "interbank.com.br", "duo" dentro de "enduro.net".
    A distância de Levenshtein só é aplicada a marcas com 5+ caracteres,
    mantendo a mesma regra já existente.
    """
    parts = domain_norm.split(".")
    candidates = set()
    if len(parts) >= 2:
        candidates.add(parts[0])
        candidates.add(".".join(parts[:-1]))
    candidates.add(domain_norm)

    hits = []
    for candidate in candidates:
        slug = candidate.replace("-", "").replace(".", "")
        for brand in BRANDS:
            brand_slug = brand.replace("-", "")

            # FIX #4: substring só aciona se a marca tiver 4+ caracteres E
            # o candidato for maior que a marca (evita match exato legítimo)
            if (
                len(brand_slug) >= 4
                and brand_slug in slug
                and brand_slug != slug
            ):
                if brand not in hits:
                    hits.append(brand)

            # Levenshtein: mantém o requisito existente de 5+ caracteres
            elif len(brand_slug) >= 5 and _levenshtein(slug, brand_slug) <= 2:
                if brand not in hits:
                    hits.append(brand)

    return hits

def _display_name_spoof(display_name, email_domain):
    if not display_name:
        return []
    dn = unicodedata.normalize("NFKC", display_name).lower()
    return [b for b in BRANDS if b in dn and b not in email_domain]

def _display_name_bait_words(display_name):
    if not display_name:
        return []
    dn = unicodedata.normalize("NFKC", display_name).lower()
    dn_ascii = unicodedata.normalize("NFD", dn)
    dn_ascii = "".join(c for c in dn_ascii if unicodedata.category(c) != "Mn")
    return [w for w in DISPLAY_NAME_BAIT if w in dn or w in dn_ascii]

def _is_likely_corporate_domain(domain):
    SAFE_TLDS = {"com", "br", "ca", "fr", "de", "uk", "au", "jp", "pt",
                 "eu", "net", "org", "co"}
    parts = domain.split(".")
    tld = parts[-1] if parts else ""
    if tld not in SAFE_TLDS:
        return False
    sld = parts[0] if parts else ""
    digit_ratio = sum(c.isdigit() for c in sld) / max(len(sld), 1)
    if digit_ratio > 0.3 or sld.count("-") >= 2:
        return False
    return True

# ── Função principal ──────────────────────────────────────────────────────────

def analyze_email_sender(raw_sender):
    """
    Analisa remetente de e-mail e retorna dict com:
    raw, display_name, email, domain, domain_normalized,
    verdict, score, reasons, indicators
    """
    result = {
        "raw": raw_sender, "display_name": "", "email": "",
        "domain": "", "domain_normalized": "",
        "verdict": "CONFIÁVEL", "score": 0, "reasons": [], "indicators": {},
    }

    if not raw_sender or not raw_sender.strip():
        result["reasons"].append("Nenhum remetente informado — análise ignorada.")
        return result

    display_name, email = _parse_email(raw_sender)
    result["display_name"] = display_name
    result["email"]        = email

    if not email:
        domain_raw = raw_sender.strip().lower().lstrip("@")
        if "." not in domain_raw:
            result["verdict"] = "SUSPEITO"
            result["reasons"].append("Formato de remetente inválido ou não reconhecido.")
            result["indicators"]["invalid_format"] = True
            return result
        email = f"unknown@{domain_raw}"
        result["email"] = email

    domain_raw = _extract_domain(email)
    result["domain"] = domain_raw

    if not domain_raw:
        result["verdict"] = "SUSPEITO"
        result["reasons"].append("Não foi possível extrair domínio do e-mail.")
        return result

    domain_norm, had_non_bmp, had_non_ascii = _normalize_domain(domain_raw)
    result["domain_normalized"] = domain_norm

    score, reasons, indic = 0, [], {}

    # ── 1. Unicode homoglyph ──────────────────────────────────────────────────
    if had_non_bmp:
        score += 50
        reasons.append(
            f"Dominio usa caracteres Unicode ocultos (Mathematical Bold/Script) "
            f"para imitar '{domain_norm}' — homoglyph spoofing avancado"
        )
        indic["unicode_homoglyph"] = True
    elif had_non_ascii and "xn--" not in domain_raw:
        score += 25
        reasons.append(
            f"Dominio com caracteres nao-ASCII fora do padrao punycode: "
            f"'{domain_raw}' (normalizado: '{domain_norm}')"
        )
        indic["non_ascii_domain"] = True

    if "xn--" in domain_norm:
        score += 20
        reasons.append(f"Dominio IDN/punycode: '{domain_raw}'")
        indic["idn_domain"] = True

    # Opera no domínio normalizado a partir daqui
    domain = domain_norm
    reg_domain = _get_reg_domain(domain)

    # ── 2. Allowlist ──────────────────────────────────────────────────────────
    if domain in EMAIL_ALLOWLIST or reg_domain in EMAIL_ALLOWLIST:
        spoof_hits = _display_name_spoof(display_name, domain)
        if spoof_hits:
            score += 35
            reasons.append(
                f"Nome exibido impersona '{', '.join(spoof_hits)}' "
                f"mas dominio e '{domain}' — possivel spear-phishing interno"
            )
            indic["display_name_spoof"] = True
        else:
            result.update({
                "verdict": "CONFIÁVEL", "score": 0,
                "reasons": [f"Dominio '{domain}' presente na allowlist interna."],
                "indicators": {"allowlisted": True},
            })
            return result

    # ── 3. Provedor gratuito ──────────────────────────────────────────────────
    if domain in FREE_EMAIL_PROVIDERS:
        score += 12
        reasons.append(
            f"Provedor de e-mail gratuito: '{domain}' — "
            f"incomum para comunicacoes corporativas oficiais"
        )
        indic["free_provider"] = True

    # ── 4. TLD suspeito ───────────────────────────────────────────────────────
    tld = _get_tld(domain)
    if tld in SUSPICIOUS_TLDS:
        score += 22
        reasons.append(f"TLD de alto risco para phishing: .{tld}")
        indic["suspicious_tld"] = True

    # ── 5. Free hosting ───────────────────────────────────────────────────────
    for fh in FREE_HOSTING_DOMAINS:
        if domain.endswith(fh):
            score += 22
            reasons.append(f"Dominio hospedado em plataforma gratuita abusada: '{fh}'")
            indic["free_hosting"] = True
            break

    # ── 6. Lookalike de marca ─────────────────────────────────────────────────
    lookalikes = _lookalike_brands(domain)
    if lookalikes:
        bonus = 15 if had_non_bmp else 0
        score += 28 + bonus
        suffix = " (confirmado via normalizacao Unicode)" if had_non_bmp else ""
        reasons.append(
            f"Dominio imita marca conhecida: {', '.join(lookalikes)}{suffix}"
        )
        indic["domain_lookalike"] = True

    # ── 7. Display Name Spoof ─────────────────────────────────────────────────
    spoof_hits = _display_name_spoof(display_name, domain)
    if spoof_hits and not indic.get("display_name_spoof"):
        score += 35
        reasons.append(
            f"Nome exibido impersona '{', '.join(spoof_hits)}' "
            f"mas e-mail vem de '{domain}' — tecnica classica de phishing"
        )
        indic["display_name_spoof"] = True

    # ── 8. Bait words no display name ────────────────────────────────────────
    bait_words = _display_name_bait_words(display_name)
    if bait_words:
        pts = min(15, 5 * len(bait_words))
        score += pts
        reasons.append(f"Palavras de alerta no nome exibido: {', '.join(bait_words[:5])}")
        indic["display_name_bait"] = True

    # ── 9. Domínio externo sem vínculo corporativo ────────────────────────────
    has_structural_flag = any(indic.get(k) for k in (
        "allowlisted", "free_provider", "suspicious_tld", "free_hosting",
        "domain_lookalike", "unicode_homoglyph", "non_ascii_domain", "idn_domain"
    ))
    if not has_structural_flag:
        if not _is_likely_corporate_domain(domain):
            score += 15
            reasons.append(
                f"Dominio '{domain}' desconhecido e fora do padrao corporativo esperado"
            )
            indic["unknown_domain"] = True
        else:
            score += 8
            reasons.append(
                f"Dominio externo nao verificado: '{domain}' — "
                f"confirme se este remetente e esperado"
            )
            indic["unverified_external"] = True

    # ── 10. Subdomain / dígitos / hífens ─────────────────────────────────────
    subdomain_parts = domain.split(".")
    if len(subdomain_parts) > 4:
        score += 10
        reasons.append(f"Dominio com muitos subdominios ({len(subdomain_parts)} niveis)")
        indic["deep_subdomain"] = True

    sld = subdomain_parts[0] if subdomain_parts else ""
    digit_ratio = sum(c.isdigit() for c in sld) / max(len(sld), 1)
    if digit_ratio > 0.4 and len(sld) > 3:
        score += 10
        reasons.append(f"SLD com muitos digitos — possivel dominio gerado: '{sld}'")
        indic["high_digit_ratio"] = True

    if sld.count("-") >= 3:
        score += 8
        reasons.append(f"Muitos hifens no dominio: '{domain}'")
        indic["excessive_hyphens"] = True

    # ── Veredito ──────────────────────────────────────────────────────────────
    score = min(score, 100)
    if score >= 55 or indic.get("display_name_spoof") or indic.get("unicode_homoglyph"):
        verdict = "MALICIOSO"
    elif score >= 20:
        verdict = "SUSPEITO"
    else:
        verdict = "CONFIÁVEL"

    result.update({"score": score, "verdict": verdict, "reasons": reasons, "indicators": indic})
    return result