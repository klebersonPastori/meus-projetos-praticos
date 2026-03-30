#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exportadores de relatórios: JSON, Markdown e HTML Corporativo.
Phishing Scan · CSIRT Edition — WebSec Scanner v1.8
"""

import json
import os
import base64
import webbrowser
from datetime import datetime

# ── Logo embedado (base64) ──────────────────────────────────
_LOGO_B64 = "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAIBAQEBAQIBAQECAgICAgQDAgICAgUEBAMEBgUGBgYFBgYGBwkIBgcJBwYGCAsICQoKCgoKBggLDAsKDAkKCgr/2wBDAQICAgICAgUDAwUKBwYHCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgr/wAARCACAAfQDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD9/KKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKK5/wCJfxa+FfwX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3KyjbX0Vj81f+Daj4E/G/wCBHwF+JOj/ABw+Dfivwbd33i+2msbXxX4eudOkuIxahS6LcIhdQeMjIzxXtv8AwXT+GnxG+Lv/AATS8b+A/hR4A1vxPrl3qGjta6N4e0qa9u5lTUrd3KQwqzsFVWY4HABJ4FfXtFYVs2qVs4WYOKvzKVumlv8AI1hg4wwX1a+lmr+p/NP+wR+wj+3B4O/bl+Dfi3xd+xr8VtK0rS/inoF3qep6l8PNTgt7S3j1GB5JpZHgCxoqgszMQAASSAK/pWmhiuImt7iJXjdSro65DA8EEHqKdRWud53VzqrCpOCjyq2hGAwEMBCUYyvc/Cb/AIKkf8G+vxv+Ffj/AFf4yfsS+DJ/F3gfUrmS7fwjpa7tS0EsdzQxQ53XUAJxH5e6VRhWQ7fMb5T+Dv7dP/BTD9gTTJPhl8PPil408D2MMzH/AIRzX9ESWC2djltltqEEiwkkknaq5Jycmv6haK9fDcYVlhlQxlGNZLv+t00352OKrklN1faUJuD8v01R/NBrn7eH/BZP9r+3PhfT/ix8WfEkd2PLew8EaLLbCcHqrJpkMe8HuDkGv1T/AODdn9l39o79mb9njx1F+0d8L9W8L3/iTxdFf6db62VW5uIhbKrSPHuLxnfkYkCsfSv0MorkzLiOONwTwtHDxpwbTdvLXokvwNsJlbw9dVp1HNrv/TPxw/4OU/2Yf2lfjt+0b8PNc+CH7PPjnxlZWXgmWC9vPCnhK81GK3lN5Iwjd7eNwjbSDtJBwc1f/wCDaT9mf9o/4D/Gf4n6p8cf2fvG/gy11DwxYxWFz4r8KXmnR3Mi3Llkja4jQOwByQMkCv2AorN8R1nkv9nezXLa17u+9yv7Lp/X/rXM79vlYKKKK+cPUCiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigArx/47fsAfsV/tMX0mr/HH9mXwjr2ozf63V5dJSG+f2a5h2TEexevYKK0pVq1CfNTk4vunZ/gTOEKkbSV15nyNYf8ABCP/AIJQade/b7f9kezaTcDtn8VaxKmf9x7wrj2xX0D8E/2aP2e/2b9Ik0P4CfBbwz4Rt5wPtI0HR4rd7jHQyuihpT7uSa7iit62Px2Jjy1qspLzk3+bM6eGw9J3hBJ+SSCiiiuQ2CiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAP/Z"
# ── Mapeamento de categorias de findings ─────────────────────────────────────
_CATEGORY_MAP = {
    "http_only":           "Tráfego HTTP Puro (Sem Criptografia)",
    "hsts_missing":        "HSTS Ausente (Strict-Transport-Security)",
    "weak_csp":            "Política de Segurança de Conteúdo (CSP) Fraca",
    "sec_headers_missing": "Cabeçalhos de Segurança Ausentes",
    "cookies_weak":        "Cookies Inseguros (flags Secure/HttpOnly ausentes)",
    "mixed_content":       "Conteúdo Misto (HTTP dentro de HTTPS)",
    "forms_insecure":      "Formulários Inseguros ou Exfiltração",
    "js_suspicious":       "Código JavaScript Suspeito / Ofuscado",
    "external_js_no_sri":  "Scripts Externos sem Validação de Integridade (SRI)",
    "cert_invalid":        "Certificado TLS/SSL Inválido ou Ausente",
    "cert_expiring_soon":  "Certificado TLS/SSL Expirando em Breve",
    "notes":               "Notas e Intervenções do Analista",
    "redirect_note":       "Redirecionamento de Tráfego Detectado",
}

# ── Severidade por categoria ──────────────────────────────────────────────────
_SEVERITY_MAP = {
    "http_only":           ("Alto",  "sev-high"),
    "hsts_missing":        ("Médio", "sev-medium"),
    "weak_csp":            ("Médio", "sev-medium"),
    "sec_headers_missing": ("Médio", "sev-medium"),
    "cookies_weak":        ("Médio", "sev-medium"),
    "mixed_content":       ("Médio", "sev-medium"),
    "forms_insecure":      ("Alto",  "sev-high"),
    "js_suspicious":       ("Alto",  "sev-high"),
    "external_js_no_sri":  ("Médio", "sev-medium"),
    "cert_invalid":        ("Alto",  "sev-high"),
    "cert_expiring_soon":  ("Médio", "sev-medium"),
    "notes":               ("Info",  "sev-info"),
    "redirect_note":       ("Info",  "sev-info"),
}

# ─────────────────────────────────────────────────────────────────────────────

def export_json(report: dict, filename="scan_report.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=4)
    print(f"[+] JSON salvo em {filename}")


def export_markdown(report: dict, filename="scan_report.md"):
    md = [
        "# WebSec Recon Report\n",
        f"Gerado em: **{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}**",
        f"Alvo: **{report.get('target','')}**\n",
        "---\n",
        f"## 🛡️ Risco: {report.get('root_score','n/d')}/100 ({report.get('root_level','n/d')})\n",
        f"> **Recomendação:** {report.get('root_action', 'n/d')}\n"
    ]
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(md))
    print(f"[+] Markdown salvo em {filename}")


def _build_email_sender_html(email_data: dict) -> str:
    """
    Gera o bloco HTML de análise do remetente para inserção no cabeçalho do relatório.
    Retorna string vazia se email_data for None ou sem e-mail.
    """
    if not email_data or not email_data.get("raw", "").strip():
        return ""

    verdict = email_data.get("verdict", "CONFIÁVEL")
    score   = email_data.get("score", 0)
    email   = email_data.get("email", "—")
    display = email_data.get("display_name", "")
    domain  = email_data.get("domain", "—")
    reasons = email_data.get("reasons", [])

    # Paleta de cores por veredito
    palette = {
        "MALICIOSO": {
            "accent":  "#c0392b",
            "bg":      "#fdf3f2",
            "border":  "#f5c0bc",
            "badge_bg":"#fdf3f2",
            "icon":    (
                '<svg width="18" height="18" viewBox="0 0 24 24" fill="none">'
                '<path d="M12 2L2 19h20L12 2z" fill="#c0392b" opacity="0.18" '
                'stroke="#c0392b" stroke-width="1.5" stroke-linejoin="round"/>'
                '<line x1="12" y1="9" x2="12" y2="14" stroke="#c0392b" stroke-width="2" stroke-linecap="round"/>'
                '<circle cx="12" cy="17" r="1" fill="#c0392b"/></svg>'
            ),
        },
        "SUSPEITO": {
            "accent":  "#854d0e",
            "bg":      "#fef3c7",
            "border":  "#d97706",
            "badge_bg":"#fef3c7",
            "icon":    (
                '<svg width="18" height="18" viewBox="0 0 24 24" fill="none">'
                '<circle cx="12" cy="12" r="9" fill="#854d0e" opacity="0.13" '
                'stroke="#854d0e" stroke-width="1.5"/>'
                '<line x1="12" y1="7" x2="12" y2="13" stroke="#854d0e" stroke-width="2" stroke-linecap="round"/>'
                '<circle cx="12" cy="16" r="1" fill="#854d0e"/></svg>'
            ),
        },
        "CONFIÁVEL": {
            "accent":  "#166534",
            "bg":      "#f0fdf4",
            "border":  "#86efac",
            "badge_bg":"#f0fdf4",
            "icon":    (
                '<svg width="18" height="18" viewBox="0 0 24 24" fill="none">'
                '<circle cx="12" cy="12" r="9" fill="#166534" opacity="0.13" '
                'stroke="#166534" stroke-width="1.5"/>'
                '<path d="M8 12l3 3 5-5" stroke="#166534" stroke-width="2" '
                'stroke-linecap="round" stroke-linejoin="round"/></svg>'
            ),
        },
    }
    p = palette.get(verdict, palette["SUSPEITO"])

    # Linhas de razões
    reasons_html = ""
    if reasons:
        items_html = "".join(
            f'<li style="margin-bottom:4px;color:#374151;">{r}</li>'
            for r in reasons
        )
        reasons_html = f"""
        <div style="margin-top:12px;padding:10px 14px;
                    background:#f9fafb;border:1px solid #e2e4ea;border-radius:6px;">
            <div style="font-size:10px;font-weight:600;letter-spacing:1.5px;
                        text-transform:uppercase;color:#6b7280;margin-bottom:6px;">
                Indicadores Detectados
            </div>
            <ul style="margin:0;padding-left:18px;font-family:'IBM Plex Mono',monospace;
                       font-size:11.5px;line-height:1.7;list-style:disc;">
                {items_html}
            </ul>
        </div>"""

    display_row = ""
    if display:
        display_row = f"""
            <div style="display:grid;grid-template-columns:120px 1fr;gap:4px 12px;
                        padding:7px 0;border-bottom:1px solid #e2e4ea;align-items:baseline;">
                <span style="font-size:10px;font-weight:600;letter-spacing:1px;
                             text-transform:uppercase;color:#9ca3af;">Nome Exibido</span>
                <span style="font-family:'IBM Plex Mono',monospace;font-size:12px;
                             color:#374151;word-break:break-all;">{display}</span>
            </div>"""

    return f"""
    <!-- E-mail Sender Analysis Block -->
    <div style="background:{p['bg']};border:1px solid {p['border']};
                border-radius:8px;overflow:hidden;margin-bottom:12px;">

        <!-- Cabeçalho -->
        <div style="background:linear-gradient(90deg,{p['bg']} 0%,#fff 100%);
                    border-bottom:1px solid {p['border']};
                    padding:12px 20px;display:flex;align-items:center;gap:10px;">
            {p['icon']}
            <span style="font-family:'DM Sans',sans-serif;font-size:11px;font-weight:700;
                         letter-spacing:2px;text-transform:uppercase;color:{p['accent']};">
                Análise do Remetente
            </span>
            <span style="margin-left:auto;font-family:'IBM Plex Mono',monospace;font-size:11px;
                         color:{p['accent']};background:rgba(255,255,255,0.75);
                         border:1px solid {p['border']};
                         padding:2px 10px;border-radius:10px;white-space:nowrap;font-weight:600;">
                {verdict} · {score}/100
            </span>
        </div>

        <!-- Corpo -->
        <div style="padding:16px 20px;">
            <!-- Campos -->
            <div style="margin-bottom:2px;">
                {display_row}
                <div style="display:grid;grid-template-columns:120px 1fr;gap:4px 12px;
                            padding:7px 0;border-bottom:1px solid #e2e4ea;align-items:baseline;">
                    <span style="font-size:10px;font-weight:600;letter-spacing:1px;
                                 text-transform:uppercase;color:#9ca3af;">Endereço</span>
                    <span style="font-family:'IBM Plex Mono',monospace;font-size:12px;
                                 color:#374151;word-break:break-all;">{email}</span>
                </div>
                <div style="display:grid;grid-template-columns:120px 1fr;gap:4px 12px;
                            padding:7px 0;align-items:baseline;">
                    <span style="font-size:10px;font-weight:600;letter-spacing:1px;
                                 text-transform:uppercase;color:#9ca3af;">Domínio</span>
                    <span style="font-family:'IBM Plex Mono',monospace;font-size:12px;
                                 color:#374151;">{domain}</span>
                </div>
            </div>
            {reasons_html}
        </div>
    </div>
    <!-- /E-mail Sender Analysis Block -->"""


def export_html(report: dict, filename="evidencia_phishing.html"):

    # ── Pasta de saída e auto-incremento de nome ─────────────────────────────
    folder_name = "Evidencias_Coletadas"
    os.makedirs(folder_name, exist_ok=True)

    base_name, ext = os.path.splitext(os.path.basename(filename))
    counter = 1
    full_path = os.path.join(folder_name, f"{base_name}{ext}")
    while os.path.exists(full_path):
        full_path = os.path.join(folder_name, f"{base_name}_{counter}{ext}")
        counter += 1

    # ── Dados do relatório ────────────────────────────────────────────────────
    level          = report.get("root_level", "MÉDIO")
    score          = report.get("root_score", 0)
    target         = report.get("target", "N/A")
    action         = report.get("root_action", "N/A")
    response_time  = report.get("response_time", 0)
    scan_time      = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    tls_info       = report.get("tls_data") or {}
    tls_version    = tls_info.get("version", "N/A")
    tls_days       = tls_info.get("days_left", "N/A")
    tls_issuer_raw = tls_info.get("issuer", "N/A")

    if tls_issuer_raw != "N/A" and "O=" in tls_issuer_raw:
        try:
            parts      = dict(item.split("=") for item in tls_issuer_raw.split(", ") if "=" in item)
            tls_org    = parts.get("O", tls_issuer_raw)
            tls_cn     = parts.get("CN", "")
            tls_c      = parts.get("C", "")
            tls_issuer = f"{tls_org}"
            tls_issuer_sub = f"{tls_cn} · {tls_c}" if tls_cn else tls_c
        except Exception:
            tls_issuer     = tls_issuer_raw
            tls_issuer_sub = ""
    else:
        tls_issuer     = tls_issuer_raw
        tls_issuer_sub = ""

    # ── Bloco de análise do remetente ────────────────────────────────────────
    email_html = _build_email_sender_html(report.get("email_sender"))

    # ── Cor de acento por nível de risco ──────────────────────────────────────
    accent_map = {
        "CRÍTICO":     ("#c0392b", "#fdf3f2", "#f5c0bc"),
        "MÉDIO":       ("#854d0e", "#fef3c7", "#d97706"),
        "BAIXO":       ("#166534", "#f0fdf4", "#86efac"),
        "INACESSÍVEL": ("#374151", "#f9fafb", "#d1d5db"),
        "INFO":        ("#1d4ed8", "#eff6ff", "#bfdbfe"),
    }
    accent_color, accent_bg, accent_border = accent_map.get(level, accent_map["MÉDIO"])

    # ── Ícone SVG por nível de risco ─────────────────────────────────────────
    _svg_c = f'<svg width="32" height="32" viewBox="0 0 24 24" fill="none"><path d="M12 2L2 19h20L12 2z" fill="{accent_color}" opacity="0.15" stroke="{accent_color}" stroke-width="1.5" stroke-linejoin="round"/><line x1="12" y1="9" x2="12" y2="14" stroke="{accent_color}" stroke-width="2" stroke-linecap="round"/><circle cx="12" cy="17" r="1" fill="{accent_color}"/></svg>'
    _svg_m = f'<svg width="32" height="32" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" fill="{accent_color}" opacity="0.12" stroke="{accent_color}" stroke-width="1.5"/><line x1="12" y1="7" x2="12" y2="13" stroke="{accent_color}" stroke-width="2" stroke-linecap="round"/><circle cx="12" cy="16" r="1" fill="{accent_color}"/></svg>'
    _svg_b = f'<svg width="32" height="32" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" fill="{accent_color}" opacity="0.12" stroke="{accent_color}" stroke-width="1.5"/><path d="M8 12l3 3 5-5" stroke="{accent_color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    _svg_i = f'<svg width="32" height="32" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" fill="{accent_color}" opacity="0.12" stroke="{accent_color}" stroke-width="1.5"/><line x1="8" y1="12" x2="16" y2="12" stroke="{accent_color}" stroke-width="2" stroke-linecap="round"/></svg>'
    _svg_n = f'<svg width="32" height="32" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" fill="{accent_color}" opacity="0.12" stroke="{accent_color}" stroke-width="1.5"/><line x1="12" y1="11" x2="12" y2="17" stroke="{accent_color}" stroke-width="2" stroke-linecap="round"/><circle cx="12" cy="8" r="1" fill="{accent_color}"/></svg>'
    level_icon = {"CRÍTICO": _svg_c, "MÉDIO": _svg_m, "BAIXO": _svg_b, "INACESSÍVEL": _svg_i, "INFO": _svg_n}.get(level, _svg_m)

    # ── Linhas da tabela de evidências ────────────────────────────────────────
    findings     = report.get("root_findings", {})
    table_rows   = ""
    row_counter  = 0

    # Idade do domínio (linha especial)
    age = findings.get("domain_age_days")
    if age is not None:
        row_counter += 1
        table_rows += f"""
                <tr>
                    <td class="td-num">{row_counter:02d}</td>
                    <td class="td-sev"><span class="badge sev-info">Info</span></td>
                    <td class="td-cat">Idade do Domínio</td>
                    <td class="td-detail">Domínio registrado há <strong>{age} dias</strong> (via Whois). Domínios recém-criados são forte indicativo de phishing.</td>
                </tr>"""

    for category, items in findings.items():
        if not items or category == "domain_age_days":
            continue

        # Ignora booleanos True soltos — já são representados pelo próprio
        # campo estar presente (ex: hsts_missing=True não precisa de linha)
        if items is True:
            continue

        title        = _CATEGORY_MAP.get(category, category.replace("_", " ").title())
        sev_label, sev_class = _SEVERITY_MAP.get(category, ("Info", "sev-info"))
        item_list    = items if isinstance(items, list) else [items]

        for item in item_list:
            row_counter += 1

            # ── Formata cada tipo de item corretamente ──────────────────────
            if item is True or item is False:
                # Booleano solto — representa o estado da categoria
                detail = title
                row_counter -= 1  # não gera linha extra, já está no título
                continue

            elif isinstance(item, dict):
                # Cookies: {'cookie': 'nome', 'issues': ['Secure', 'HttpOnly']}
                if "cookie" in item and "issues" in item:
                    cookie_name = item.get("cookie") or "desconhecido"
                    issues = ", ".join(item.get("issues", []))
                    detail = (f'Cookie <span class="flag">{cookie_name}</span> '
                              f'sem flags: <span class="flag">{issues}</span>')
                # Forms: {'method': 'POST', 'action': '...', 'issues': [...]}
                elif "method" in item and "action" in item:
                    method = item.get("method", "")
                    action_url = item.get("action", "")
                    issues = "; ".join(item.get("issues", []))
                    detail = (f'Método: <span class="flag">{method}</span> · '
                              f'Action: <span class="url">{action_url}</span><br>'
                              f'<span class="flag">{issues}</span>')
                else:
                    # Dict genérico — formata chave: valor
                    detail = " · ".join(f"{k}: {v}" for k, v in item.items())

            elif isinstance(item, str):
                # String com URL e padrão separados por ": "
                if ": " in item:
                    parts = item.split(": ", 1)
                    detail = (f'<span class="url">{parts[0]}</span><br>'
                              f'<span class="flag">{parts[1]}</span>')
                # Redirecionamento
                elif "➜" in item or "->" in item:
                    detail = f'<span class="url">{item}</span>'
                else:
                    detail = item
            else:
                detail = str(item)

            table_rows += f"""
                <tr>
                    <td class="td-num">{row_counter:02d}</td>
                    <td class="td-sev"><span class="badge {sev_class}">{sev_label}</span></td>
                    <td class="td-cat">{title}</td>
                    <td class="td-detail">{detail}</td>
                </tr>"""

    total_findings = row_counter

    # ── Bloco VirusTotal ──────────────────────────────────────────────────────
    vt_data     = report.get("virustotal") or {}
    vt_status   = vt_data.get("status", "")
    vt_html     = ""

    if vt_status == "ok":
        vt_mal      = vt_data.get("malicious",  0)
        vt_sus      = vt_data.get("suspicious", 0)
        vt_harm     = vt_data.get("harmless",   0)
        vt_undet    = vt_data.get("undetected", 0)
        vt_total    = vt_data.get("total",      0)
        vt_link     = vt_data.get("permalink",  "https://www.virustotal.com")
        vt_detects  = vt_data.get("detections", [])

        # Cor da barra de veredicto
        if vt_mal >= 5:
            vt_verdict_color = "#c0392b"
            vt_verdict_bg    = "#fdf3f2"
            vt_verdict_text  = f"PERIGOSO — {vt_mal} engine(s) detectaram como MALICIOSO"
        elif vt_mal > 0 or vt_sus > 0:
            vt_verdict_color = "#854d0e"
            vt_verdict_bg    = "#fef3c7"
            vt_verdict_text  = f"SUSPEITO — {vt_mal} malicioso(s) e {vt_sus} suspeito(s)"
        else:
            vt_verdict_color = "#166534"
            vt_verdict_bg    = "#f0fdf4"
            vt_verdict_text  = "LIMPO — Nenhuma engine detectou ameaça"

        # Tabela de detecções (máx 40 linhas para não poluir o relatório)
        detect_rows = ""
        for i, d in enumerate(vt_detects[:40], 1):
            cat   = d.get("category", "")
            badge = "sev-high" if cat == "malicious" else "sev-medium"
            detect_rows += f"""
                    <tr>
                        <td class="td-num">{i:02d}</td>
                        <td class="td-sev"><span class="badge {badge}">{cat.capitalize()}</span></td>
                        <td class="td-cat">{d.get('engine','')}</td>
                        <td class="td-detail">{d.get('result','') or '—'}</td>
                    </tr>"""

        if not detect_rows:
            detect_rows = """
                    <tr>
                        <td colspan="4" style="text-align:center;padding:18px;color:#6b7280;font-family:var(--mono);font-size:12px;">
                            Nenhum antivírus detectou ameaça para esta URL.
                        </td>
                    </tr>"""

        extra_note = ""
        if len(vt_detects) > 40:
            extra_note = (f'<p style="font-size:11px;color:var(--text-faint);margin-top:8px;'
                          f'font-family:var(--mono);">+ {len(vt_detects)-40} detecções adicionais — '
                          f'<a href="{vt_link}" target="_blank" style="color:var(--blue)">ver relatório completo</a></p>')

        vt_html = f"""
    <!-- VirusTotal Section -->
    <div style="margin-top:32px;background:#f0f6ff;border:1px solid #c7d9f8;
                border-radius:12px;overflow:hidden;">

        <!-- Cabecalho azul claro -->
        <div style="background:linear-gradient(90deg,#bfdbfe 0%,#dbeafe 60%,#eff6ff 100%);
                    border-bottom:1px solid #c7d9f8;
                    padding:14px 24px;display:flex;align-items:center;gap:12px;">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="12" r="11" fill="#93c5fd" fill-opacity="0.4"/>
                <path d="M7 12l3.5 4L17 8" stroke="#1e40af" stroke-width="2.2"
                      stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span style="font-family:var(--sans);font-size:11px;font-weight:700;
                         letter-spacing:2px;text-transform:uppercase;color:#1e40af;">
                VirusTotal &mdash; Análise Comunitária de Reputação
            </span>
            <span style="margin-left:auto;font-family:var(--mono);font-size:11px;
                         color:#1e40af;background:rgba(255,255,255,0.7);
                         border:1px solid #93c5fd;
                         padding:2px 10px;border-radius:10px;white-space:nowrap;">
                {vt_mal + vt_sus} detecção(ões) em {vt_total} engines
            </span>
        </div>

        <!-- Placar -->
        <div style="display:grid;grid-template-columns:repeat(5,minmax(0,1fr));
                    gap:1px;background:#c7d9f8;">
            <div style="background:#f0f6ff;padding:18px 12px;text-align:center;">
                <div style="font-size:10px;font-weight:600;letter-spacing:1.5px;
                            text-transform:uppercase;color:#1e40af;margin-bottom:8px;">Malicioso</div>
                <div style="font-family:var(--mono);font-size:1.8em;font-weight:700;
                            color:{vt_verdict_color};">{vt_mal}</div>
            </div>
            <div style="background:#f0f6ff;padding:18px 12px;text-align:center;">
                <div style="font-size:10px;font-weight:600;letter-spacing:1.5px;
                            text-transform:uppercase;color:#1e40af;margin-bottom:8px;">Suspeito</div>
                <div style="font-family:var(--mono);font-size:1.8em;font-weight:700;
                            color:#854d0e;">{vt_sus}</div>
            </div>
            <div style="background:#f0f6ff;padding:18px 12px;text-align:center;">
                <div style="font-size:10px;font-weight:600;letter-spacing:1.5px;
                            text-transform:uppercase;color:#1e40af;margin-bottom:8px;">Inofensivo</div>
                <div style="font-family:var(--mono);font-size:1.8em;font-weight:700;
                            color:#166534;">{vt_harm}</div>
            </div>
            <div style="background:#f0f6ff;padding:18px 12px;text-align:center;">
                <div style="font-size:10px;font-weight:600;letter-spacing:1.5px;
                            text-transform:uppercase;color:#1e40af;margin-bottom:8px;">Não detectado</div>
                <div style="font-family:var(--mono);font-size:1.8em;font-weight:700;
                            color:#374151;">{vt_undet}</div>
            </div>
            <div style="background:#e8f0fe;padding:18px 12px;text-align:center;">
                <div style="font-size:10px;font-weight:600;letter-spacing:1.5px;
                            text-transform:uppercase;color:#1e40af;margin-bottom:8px;">Total Engines</div>
                <div style="font-family:var(--mono);font-size:1.8em;font-weight:700;
                            color:#1a56db;">{vt_total}</div>
            </div>
        </div>

        <!-- Veredicto -->
        <div style="background:{vt_verdict_bg};border-top:1px solid #c7d9f8;
                    border-bottom:1px solid #c7d9f8;
                    padding:12px 24px;display:flex;align-items:center;gap:12px;">
            <span style="font-size:11px;font-weight:700;letter-spacing:1.5px;
                         text-transform:uppercase;color:{vt_verdict_color};">{vt_verdict_text}</span>
            <a href="{vt_link}" target="_blank"
               style="margin-left:auto;font-family:var(--mono);font-size:11px;
                      color:#1a56db;text-decoration:none;white-space:nowrap;
                      background:#dbeafe;border:1px solid #93c5fd;
                      padding:4px 12px;border-radius:4px;">
                Ver no VirusTotal ↗
            </a>
        </div>

        <!-- Tabela de detecções -->
        <div style="background:white;">
            <table style="width:100%;border-collapse:collapse;">
                <thead>
                    <tr style="background:#e8f0fe;border-bottom:1px solid #c7d9f8;">
                        <th style="font-size:10px;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;
                                   color:#1e40af;padding:10px 16px;text-align:left;white-space:nowrap;">#</th>
                        <th style="font-size:10px;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;
                                   color:#1e40af;padding:10px 16px;text-align:left;white-space:nowrap;">Categoria</th>
                        <th style="font-size:10px;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;
                                   color:#1e40af;padding:10px 16px;text-align:left;white-space:nowrap;">Antivírus / Engine</th>
                        <th style="font-size:10px;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;
                                   color:#1e40af;padding:10px 16px;text-align:left;">Classificação Reportada</th>
                    </tr>
                </thead>
                <tbody>{detect_rows}
                </tbody>
            </table>
        </div>

    </div>
    {extra_note}"""

    elif vt_status == "queued":
        vt_html = f"""
    <div style="margin-top:32px;background:#f0f6ff;border:1px solid #c7d9f8;border-radius:12px;overflow:hidden;">
        <div style="background:linear-gradient(90deg,#bfdbfe,#eff6ff);border-bottom:1px solid #c7d9f8;padding:14px 24px;">
            <span style="font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#1e40af;">
                VirusTotal &mdash; Análise Comunitária de Reputação
            </span>
        </div>
        <div style="padding:18px 24px;font-family:var(--mono);font-size:12px;color:#1e40af;">
            Análise ainda em processamento no VirusTotal. {vt_data.get('error','')}
        </div>
    </div>"""

    elif vt_status == "error":
        vt_html = f"""
    <div style="margin-top:32px;background:#f0f6ff;border:1px solid #c7d9f8;border-radius:12px;overflow:hidden;">
        <div style="background:linear-gradient(90deg,#bfdbfe,#eff6ff);border-bottom:1px solid #c7d9f8;padding:14px 24px;">
            <span style="font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#1e40af;">
                VirusTotal &mdash; Análise Comunitária de Reputação
            </span>
        </div>
        <div style="padding:18px 24px;font-family:var(--mono);font-size:12px;color:#854d0e;">
            VirusTotal indisponível: {vt_data.get('error','Erro desconhecido.')}
        </div>
    </div>"""

    # ── HTML final ────────────────────────────────────────────────────────────
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CSIRT · Evidência de Segurança — {target}</title>
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --white:          #ffffff;
            --bg:             #f4f5f7;
            --surface:        #ffffff;
            --border:         #e2e4ea;
            --border-mid:     #cdd0da;
            --text-primary:   #111827;
            --text-mid:       #374151;
            --text-muted:     #6b7280;
            --text-faint:     #9ca3af;
            --accent:         {accent_color};
            --accent-bg:      {accent_bg};
            --accent-border:  {accent_border};
            --amber:          #854d0e;
            --amber-bg:       #fef3c7;
            --amber-border:   #d97706;
            --blue:           #1d4ed8;
            --blue-bg:        #eff6ff;
            --blue-border:    #bfdbfe;
            --green:          #166534;
            --green-bg:       #f0fdf4;
            --green-border:   #86efac;
            --mono:           'IBM Plex Mono', monospace;
            --sans:           'DM Sans', sans-serif;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: var(--sans);
            background: var(--bg);
            color: var(--text-primary);
            font-size: 13.5px;
            line-height: 1.6;
            -webkit-font-smoothing: antialiased;
        }}
        .page {{ max-width: 900px; margin: 32px auto; padding: 0 24px 80px; }}

        /* stripe */
        .doc-stripe {{ height: 4px; background: var(--accent); border-radius: 2px 2px 0 0; }}

        /* letterhead */
        .letterhead {{
            background: var(--surface); border: 1px solid var(--border);
            border-top: none; border-radius: 0 0 8px 8px;
            padding: 24px 28px 20px;
            display: flex; justify-content: space-between; align-items: flex-start;
            margin-bottom: 2px;
        }}
        .lh-left {{ display: flex; align-items: center; gap: 20px; }}
        .lh-logo {{ height: 36px; width: auto; display: block; }}
        .lh-divider {{ width: 1px; height: 36px; background: var(--border-mid); flex-shrink: 0; }}
        .lh-org {{ font-size: 11px; font-weight: 600; letter-spacing: 2px; text-transform: uppercase; color: var(--text-muted); }}
        .lh-title {{ font-size: 1.35em; font-weight: 600; color: var(--text-primary); margin-top: 2px; }}
        .lh-right {{ font-family: var(--mono); font-size: 11px; color: var(--text-muted); text-align: right; line-height: 2; }}
        .lh-right strong {{ color: var(--text-primary); font-weight: 600; }}
        .confidential-tag {{
            display: inline-block; font-family: var(--mono); font-size: 10px; font-weight: 600;
            letter-spacing: 1.5px; text-transform: uppercase; color: var(--accent);
            border: 1px solid var(--accent-border); background: var(--accent-bg);
            padding: 2px 8px; border-radius: 3px; margin-top: 4px;
        }}

        .divider {{ height: 1px; background: var(--border); margin: 20px 0; }}

        /* exec block */
        .exec-block {{
            background: var(--surface); border: 1px solid var(--border);
            border-radius: 8px; overflow: hidden; margin-bottom: 12px;
        }}
        .exec-header {{
            background: var(--accent-bg); border-bottom: 1px solid var(--accent-border);
            padding: 14px 24px;
        }}
        .exec-header-label {{
            font-size: 10px; font-weight: 600; letter-spacing: 2px;
            text-transform: uppercase; color: var(--accent);
        }}
        .exec-body {{ display: grid; grid-template-columns: 160px 1fr; }}
        .score-col {{
            border-right: 1px solid var(--border); padding: 28px 24px;
            display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 4px;
        }}
        .score-icon {{ line-height: 1; margin-bottom: 4px; }}
        .score-number {{ font-family: var(--mono); font-size: 3em; font-weight: 600; color: var(--accent); line-height: 1; }}
        .score-max {{ font-family: var(--mono); font-size: 12px; color: var(--text-faint); }}
        .score-pill {{
            font-family: var(--mono); font-size: 11px; font-weight: 600; letter-spacing: 1.5px;
            background: var(--accent); color: #fff; padding: 3px 12px; border-radius: 2px; margin-top: 10px;
        }}
        .meta-col {{ padding: 20px 28px; }}
        .meta-row {{
            display: grid; grid-template-columns: 100px 1fr;
            gap: 4px 16px; padding: 8px 0;
            border-bottom: 1px solid var(--border); align-items: baseline;
        }}
        .meta-row:last-child {{ border-bottom: none; }}
        .meta-key {{ font-size: 10px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; color: var(--text-faint); padding-top: 1px; }}
        .meta-val {{ font-family: var(--mono); font-size: 12px; color: var(--text-mid); word-break: break-all; line-height: 1.6; }}
        .meta-val.action {{ font-family: var(--sans); font-size: 13px; font-weight: 600; color: var(--accent); }}

        /* metrics */
        .metrics-row {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 10px; margin-bottom: 12px; }}
        .metric-card {{ background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 16px 18px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; min-height: 90px; min-width: 0; position: relative; }}
        .metric-key {{ font-size: 10px; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase; color: var(--text-faint); margin-bottom: 8px; }}
        .metric-val {{ font-family: var(--mono); font-size: 1.1em; font-weight: 600; color: var(--text-primary); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; width: 100%; }}
        .metric-sub {{ font-size: 11px; color: var(--text-faint); margin-top: 3px; }}
        
        /* tooltip customizado corrigido */
        .metric-val[data-tooltip] {{
            cursor: pointer; /* Troca a interrogação pela mãozinha */
        }}
        
        .metric-val[data-tooltip]:hover::after {{
            content: attr(data-tooltip);
            position: absolute;
            bottom: calc(100% + 8px); /* Flutua elegantemente acima do card */
            left: 50%;
            transform: translateX(-50%);
            background: var(--text-mid);
            color: var(--white);
            padding: 8px 12px;
            border-radius: 6px;
            font-family: var(--sans);
            font-size: 12px;
            font-weight: 400;
            white-space: normal;
            word-break: break-word;
            width: max-content;
            max-width: 250px;
            z-index: 100;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            pointer-events: none;
            line-height: 1.4;
        }}

        /* setinha do tooltip */
        .metric-val[data-tooltip]:hover::before {{
            content: '';
            position: absolute;
            bottom: calc(100% + 8px);
            left: 50%;
            transform: translateX(-50%);
            border: 6px solid transparent;
            border-top-color: var(--text-mid);
            margin-bottom: -11px; /* Puxa a setinha para baixo do balão */
            z-index: 100;
            pointer-events: none;
        }}
        
        .metric-val[data-tooltip]:hover::after {{
            content: attr(data-tooltip);
            position: absolute;
            bottom: 100%;
            left: 50%;
            transform: translateX(-50%);
            background: var(--text-mid);
            color: var(--white);
            padding: 8px 12px;
            border-radius: 6px;
            font-family: var(--sans);
            font-size: 12px;
            font-weight: 400;
            white-space: normal;
            word-break: break-word;
            width: max-content;
            max-width: 250px;
            z-index: 100;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            margin-bottom: 8px;
            pointer-events: none;
            line-height: 1.4;
        }}

        /* setinha do tooltip */
        .metric-val[data-tooltip]:hover::before {{
            content: '';
            position: absolute;
            bottom: 100%;
            left: 50%;
            transform: translateX(-50%);
            border: 6px solid transparent;
            border-top-color: var(--text-mid);
            margin-bottom: -4px;
            z-index: 100;
            pointer-events: none;
        }}

        /* section label */
        .section-label {{ display: flex; align-items: center; gap: 10px; margin: 24px 0 10px; }}
        .section-label span {{ font-size: 10px; font-weight: 600; letter-spacing: 2px; text-transform: uppercase; color: var(--text-faint); }}
        .section-label::after {{ content: ''; flex: 1; height: 1px; background: var(--border); }}
        .section-count {{
            font-family: var(--mono); font-size: 10px; color: var(--text-faint);
            background: var(--bg); border: 1px solid var(--border); border-radius: 10px; padding: 1px 9px;
        }}

        /* table */
        .table-wrap {{ background: var(--surface); border: 1px solid var(--border); border-radius: 8px; overflow: hidden; }}
        table {{ width: 100%; border-collapse: collapse; }}
        thead tr {{ background: var(--bg); border-bottom: 1px solid var(--border-mid); }}
        th {{
            font-size: 10px; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase;
            color: var(--text-faint); padding: 10px 16px; text-align: left; white-space: nowrap;
        }}
        td {{ padding: 11px 16px; border-bottom: 1px solid var(--border); vertical-align: top; }}
        tbody tr:last-child td {{ border-bottom: none; }}
        tbody tr:nth-child(even) {{ background: #fafbfc; }}
        tbody tr:hover {{ background: #f0f4ff; }}
        .td-num {{ font-family: var(--mono); font-size: 11px; color: var(--text-faint); width: 32px; }}
        .td-sev {{ width: 80px; }}
        .td-cat {{ font-size: 12.5px; font-weight: 500; color: var(--text-primary); width: 210px; }}
        .td-detail {{ font-family: var(--mono); font-size: 11.5px; color: var(--text-muted); word-break: break-all; line-height: 1.75; }}
        .td-detail .url  {{ color: var(--blue); }}
        .td-detail .flag {{ color: var(--amber); }}

        /* badges */
        .badge {{
            display: inline-block; font-family: var(--mono); font-size: 10px; font-weight: 600;
            padding: 2px 8px; border-radius: 3px; letter-spacing: .5px; text-transform: uppercase; white-space: nowrap;
        }}
        .sev-high   {{ background: #fdf3f2; color: #c0392b; border: 1px solid #f5c0bc; }}
        .sev-medium {{ background: #fef3c7; color: #854d0e; border: 1px solid #d97706; }}
        .sev-low    {{ background: #f0fdf4; color: #166534; border: 1px solid #86efac; }}
        .sev-info   {{ background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; }}

        /* footer */
        .doc-footer {{
            margin-top: 36px; padding-top: 14px;
            border-top: 1px solid var(--border); text-align: center;
        }}
        .footer-center {{ font-family: var(--mono); font-size: 11px; color: var(--text-faint); }}
        .footer-center strong {{ color: var(--text-muted); font-weight: 500; }}
        .brand-footer {{ margin-top: 28px; display: flex; justify-content: center; opacity: 0.28; }}
        .brand-logo {{ height: 22px; width: auto; filter: grayscale(100%); }}

        /* print */
        @media print {{
            body {{ background: #fff; font-size: 12px; }}
            .page {{ margin: 0; padding: 20px; max-width: 100%; }}
            .doc-stripe {{ display: none; }}
            tbody tr:hover {{ background: none; }}
        }}
    </style>
</head>
<body>
<div class="page">

    <div class="doc-stripe"></div>

    <div class="letterhead">
        <div class="lh-left">
            <img src="data:image/jpeg;base64,{_LOGO_B64}" alt="Phishing Scan" class="lh-logo">
            <div class="lh-divider"></div>
            <div>
                <div class="lh-org">CSIRT</div>
                <div class="lh-title">Evidência de Análise de Phishing</div>
            </div>
        </div>
        <div class="lh-right">
            <div>WebSec Scanner <strong>v1.8</strong></div>
            <div><span class="confidential-tag">Confidencial</span></div>
        </div>
    </div>

    <div class="divider"></div>

    {email_html}

    <div class="exec-block">
        <div class="exec-header">
            <div class="exec-header-label">Resumo Executivo</div>
        </div>
        <div class="exec-body">
            <div class="score-col">
                <div class="score-icon">{level_icon}</div>
                <div class="score-number">{score}</div>
                <div class="score-max">/ 100 pontos</div>
                <div class="score-pill">{level}</div>
            </div>
            <div class="meta-col">
                <div class="meta-row">
                    <span class="meta-key">Alvo</span>
                    <span class="meta-val">{target}</span>
                </div>
                <div class="meta-row">
                    <span class="meta-key">Data / Hora</span>
                    <span class="meta-val">{scan_time} · Horário local</span>
                </div>
                <div class="meta-row">
                    <span class="meta-key">Método</span>
                    <span class="meta-val">Varredura passiva automatizada — sem interação ativa com o alvo</span>
                </div>
                <div class="meta-row">
                    <span class="meta-key">Ação</span>
                    <span class="meta-val action">{action}</span>
                </div>
            </div>
        </div>
    </div>

    <div class="metrics-row">
        <div class="metric-card">
            <div class="metric-key">Resposta HTTP</div>
            <div class="metric-val">{response_time} ms</div>
            <div class="metric-sub">Tempo de resposta</div>
        </div>
        <div class="metric-card">
            <div class="metric-key">Protocolo TLS</div>
            <div class="metric-val">{tls_version}</div>
            <div class="metric-sub">Versão do handshake</div>
        </div>
        <div class="metric-card">
            <div class="metric-key">Emissor do Cert.</div>
            <div class="metric-val" style="font-size:.95em" data-tooltip="{tls_issuer}">{tls_issuer}</div>
            <div class="metric-sub">{tls_issuer_sub}</div>
        </div>
        <div class="metric-card">
            <div class="metric-key">Validade do Cert.</div>
            <div class="metric-val">{tls_days} dias</div>
            <div class="metric-sub">A partir de hoje</div>
        </div>
    </div>

    <div class="section-label">
        <span>Detalhamento de Evidências</span>
        <span class="section-count">{total_findings} ocorrências</span>
    </div>

    <div class="table-wrap">
        <table>
            <thead>
                <tr>
                    <th>#</th>
                    <th>Severidade</th>
                    <th>Categoria</th>
                    <th>Detalhe Técnico</th>
                </tr>
            </thead>
            <tbody>
                {table_rows}
            </tbody>
        </table>
    </div>

    {vt_html}

    <div class="doc-footer">
        <div class="footer-center">
            Responsável pela análise e revisão: <strong>Time de Governança · </strong> · Scan realizado em {scan_time}
        </div>
    </div>

</div>
</body>
</html>"""

    with open(full_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[+] Relatorio HTML salvo em {full_path}")

    # Abre o navegador em thread separada para nao bloquear o terminal
    try:
        import threading
        abs_path = os.path.abspath(full_path)
        t = threading.Timer(0.5, webbrowser.open, args=[f"file:///{abs_path}"])
        t.daemon = True
        t.start()
    except Exception as e:
        print(f"[-] Nao foi possivel abrir o navegador: {e}")