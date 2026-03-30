#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI do WebSec Recon — Interface atualizada com foco em Triage de Phishing.
"""

import argparse
import sys
import os
from datetime import datetime

from . import __version__
from .utils import banner, info, warn, err, good, GREEN, BOLD, RESET, DIM, CYAN, YELLOW, RED, BLUE, normalize_url
from .scanner import scan_single_page
from .crawler import crawl
from .exporters import export_json, export_markdown, export_html
from .email_analyzer import analyze_email_sender

# ── Persistência da chave VirusTotal ─────────────────────────────────────────
import pathlib

def _vt_key_path() -> pathlib.Path:
    """Retorna o caminho do arquivo que armazena a chave VT."""
    base = pathlib.Path(__file__).parent.parent
    venv_dir = base / "venv"
    if venv_dir.exists():
        return venv_dir / ".vt_api_key"
    return base / ".vt_api_key"

def _load_vt_key() -> str:
    """Carrega a chave VT do arquivo, se existir."""
    try:
        key = _vt_key_path().read_text(encoding="utf-8").strip()
        return key if key else ""
    except Exception:
        return ""

def _save_vt_key(key: str):
    """Salva a chave VT no arquivo."""
    try:
        _vt_key_path().write_text(key.strip(), encoding="utf-8")
    except Exception as e:
        warn(f"Nao foi possivel salvar a chave VT: {e}")

def _prompt_vt_key() -> str:
    """Pede a chave VT ao utilizador."""
    print(f"\n{BOLD}{'─'*58}{RESET}")
    print(f"  {CYAN}[?] Chave de API do VirusTotal{RESET}")
    print(f"  Deixe em branco e pressione ENTER para pular.")
    print(f"{BOLD}{'─'*58}{RESET}")
    try:
        return input("  Cole sua chave aqui: ").strip().strip('"').strip("'")
    except (KeyboardInterrupt, EOFError):
        return ""

def resolve_vt_key(cli_key: str) -> str:
    """
    Resolve a chave VT na seguinte ordem de prioridade:
      1. Argumento --vt-key passado na linha de comando
      2. Chave salva no arquivo .vt_api_key (sessão anterior)
      3. Prompt interativo com opção de salvar (só aceita S/N)
    """
    # 1. Linha de comando
    if cli_key and cli_key.strip():
        return cli_key.strip()

    # 2. Arquivo salvo
    saved = _load_vt_key()
    if saved:
        good("Chave VirusTotal carregada automaticamente.")
        return saved

    # 3. Prompt interativo
    key = _prompt_vt_key()
    if key:
        # Loop até receber S ou N — nenhum outro caractere é aceito
        while True:
            try:
                resp = input("\n  Salvar chave para proximas execucoes? (S/N): ").strip().lower()
                if resp == 's':
                    _save_vt_key(key)
                    good("Chave salva com sucesso!")
                    break
                elif resp == 'n':
                    break
                else:
                    warn("Digite apenas S para salvar ou N para pular.")
            except (KeyboardInterrupt, EOFError):
                break
    return key
# ─────────────────────────────────────────────────────────────────────────────

def build_parser():
    p = argparse.ArgumentParser(
        prog="websec-recon",
        description="WebSec Recon CSIRT Edition - Phishing Triage Scanner"
    )
    p.add_argument("--url", "-u", help="URL alvo (ex.: https://exemplo.com)")
    p.add_argument("--recursive", "-r", action="store_true", help="Ativa varredura de subpáginas")
    p.add_argument("--depth", "-d", type=int, default=2, help="Profundidade do crawler")
    p.add_argument("--max-pages", "-m", type=int, default=15, help="Máximo de páginas")
    p.add_argument("--json", type=str, help="Exportar JSON")
    p.add_argument("--markdown", "--md", type=str, help="Exportar Markdown")
    p.add_argument("--html", type=str, help="Exportar relatório executivo HTML")
    p.add_argument("--timeout", type=int, default=12, help="Timeout HTTP")
    p.add_argument("--js-fetch-limit", type=int, default=10, help="Limite de inspeção JS")
    p.add_argument("--verbose", "-v", action="store_true", help="Exibe logs detalhados durante o scan")
    p.add_argument("--vt-key", type=str, default="", help="Chave de API do VirusTotal (opcional)")
    p.add_argument("--version", "-V", action="store_true", help="Exibe versão")
    return p

def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.version:
        print(__version__)
        return 0

    current_url = args.url

    # Resolve a chave VT uma única vez (arquivo / prompt / CLI arg)
    vt_key = resolve_vt_key(args.vt_key)

    # Laço de repetição contínuo para múltiplas análises
    first_run = True
    while True:
        # Na primeira execução, limpa para exibir o banner limpo.
        # Nas seguintes, limpa APÓS confirmar nova análise — mantendo o
        # resultado anterior visível até o analista decidir continuar.
        if first_run:
            os.system('cls' if os.name == 'nt' else 'clear')
            first_run = False

        banner()

        url = current_url
        if not url:
            try:
                print(f"{BOLD}{GREEN}URL do site alvo:{RESET} ", end="", flush=True)
                url = input().strip()
            except KeyboardInterrupt:
                print()
                break
            except EOFError:
                # Ocorre em alguns terminais Windows ao colar texto com caracteres especiais
                print()
                err("Erro ao ler a URL. Tente digitar manualmente ou use o parâmetro --url.")
                continue

        if not url:
            err("Nenhuma URL informada.")
            continue

        # Sanitiza a URL: remove aspas, espaços e caracteres de controle que
        # o CMD do Windows pode injetar ao colar com Ctrl+V
        url = url.strip().strip('"').strip("'").strip()

        # Remove caracteres de controle invisíveis (BOM, zero-width, etc.)
        url = ''.join(c for c in url if ord(c) >= 32 or c in '\t')

        url = normalize_url(url)

        # ── Prompt de remetente (opcional) ────────────────────────────────────
        email_result = None
        try:
            print(f"\n{BOLD}{CYAN}Remetente do e-mail suspeito (opcional — pressione ENTER para pular):{RESET} ", end="", flush=True)
            raw_sender = input().strip()
        except (KeyboardInterrupt, EOFError):
            raw_sender = ""

        if raw_sender:
            raw_sender = raw_sender.strip().strip('"').strip("'")
            raw_sender = ''.join(c for c in raw_sender if ord(c) >= 32 or c in '\t')
            try:
                email_result = analyze_email_sender(raw_sender)
            except Exception:
                email_result = None
        # ─────────────────────────────────────────────────────────────────────

        print(f"\n{BOLD}=== Varredura da pagina raiz ==={RESET}")
        root = scan_single_page(url, timeout=args.timeout, js_fetch_limit=args.js_fetch_limit,
                                silent=not args.verbose, vt_api_key=vt_key)

        subpages_data = {}
        if args.recursive:
            print(f"\n{BOLD}=== Crawler (subpáginas) ==={RESET}")
            subpages_list = [p for p in crawl(url, max_depth=args.depth, max_pages=args.max_pages, verbose=args.verbose) if p not in (root["final_url"], url)]

            for i, page in enumerate(subpages_list, 1):
                print(f"\n{BOLD}--- [{i}/{len(subpages_list)}] ESCANEANDO: {page} ---{RESET}")
                res = scan_single_page(page, timeout=args.timeout, js_fetch_limit=args.js_fetch_limit, silent=not args.verbose)
                subpages_data[page] = {"status": res.get("status"), "score": res.get("score"), "level": res.get("level")}

        final_report = {
            "target": url,
            "timestamp": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            "root_status": root.get("status"),
            "root_score": root.get("score"),
            "root_level": root.get("level"),
            "root_action": root.get("action"),
            "root_findings": root.get("findings"),
            "response_time": root.get("response_time", 0),
            "tls_data": root.get("tls_data"),
            "virustotal": root.get("virustotal"),
            "email_sender": email_result,
            "subpages": subpages_data
        }

        if args.json: export_json(final_report, args.json)
        if args.markdown: export_markdown(final_report, args.markdown)
        if args.html: export_html(final_report, args.html)

        # -- Mensagem final ------------------------------------------------
        report_path = args.html if args.html else "N/A"
        sep = f"{BLUE}{'=' * 60}{RESET}"
        print(f"\n{sep}")
        print(f"  {BOLD}{GREEN}Scan concluido.{RESET}")
        if report_path != "N/A":
            print(f"  {'RELATORIO':<10}: {report_path}")
        print(sep)
        # -----------------------------------------------------------------

        # Pergunta se o utilizador quer continuar — só aceita S ou N
        while True:
            try:
                resp = input(f"\n{BOLD}{YELLOW}Deseja analisar outra URL? (S/N): {RESET}").strip().lower()
                if resp == 's':
                    current_url = None
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
                elif resp == 'n':
                    print(f"\n{DIM}Encerrando o scanner. Ate logo.{RESET}\n")
                    sys.exit(0)
                else:
                    warn("Digite apenas S para continuar ou N para sair.")
            except KeyboardInterrupt:
                print(f"\n{DIM}Interrompido pelo utilizador.{RESET}\n")
                sys.exit(0)

    return 0

if __name__ == "__main__":
    sys.exit(main())