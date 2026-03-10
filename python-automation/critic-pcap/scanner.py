#!/usr/bin/env python3
# scanner.py
import argparse, os, json, base64, re, sys
from scapy.all import rdpcap, TCP, UDP, Raw

# ---------- Configurações padrão (para facilitar execução) ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PCAP = os.path.join(BASE_DIR, "demo.pcap")
DEFAULT_OUT  = os.path.join(BASE_DIR, "reports")

SUS_KEYS = [b"password=", b"passwd=", b"pwd=", b"token=", b"secret="]
HTTP_PORT = 80
FTP_PORT  = 21
TELNET_PORT = 23
POP3_PORT = 110
IMAP_PORT = 143
DNS_PORT = 53

def is_http_packet(pkt):
    # Heurística simples: porta 80 e há carga textual começando com métodos HTTP
    if pkt.haslayer(TCP):
        sport, dport = pkt[TCP].sport, pkt[TCP].dport
        if (sport == HTTP_PORT or dport == HTTP_PORT) and pkt.haslayer(Raw):
            payload = pkt[Raw].load
            return payload.startswith((b"GET", b"POST", b"HEAD", b"PUT", b"DELETE", b"OPTIONS", b"HTTP/"))
    return False

def parse_http_findings(payload_bytes, findings):
    # 1) HTTP Basic Authorization
    try:
        headers = payload_bytes.split(b"\r\n")
        for h in headers:
            if h.lower().startswith(b"authorization: basic "):
                b64 = h.split(b" ", 2)[-1].strip()
                try:
                    creds = base64.b64decode(b64).decode(errors="ignore")
                except Exception:
                    creds = "<invalid base64>"
                findings.append({
                    "type": "http_basic_creds",
                    "severity": "high",
                    "detail": f"Credenciais em claro (Basic): {creds}"
                })
                break
    except Exception:
        pass

    # 2) Parâmetros sensíveis em HTTP claro
    low = payload_bytes.lower()
    for key in SUS_KEYS:
        if key in low:
            # Mostrar o trecho (snippet) para contexto
            idx = low.find(key)
            start = max(0, idx - 20)
            end = min(len(low), idx + 80)
            snippet = payload_bytes[start:end].decode(errors="ignore")
            findings.append({
                "type": "http_sensitive_param",
                "severity": "medium",
                "detail": f"Parametro sensível em HTTP: ...{snippet}..."
            })
            break

def is_insecure_proto(pkt):
    if pkt.haslayer(TCP):
        p = pkt[TCP].sport if pkt[TCP].sport in (FTP_PORT, TELNET_PORT, POP3_PORT, IMAP_PORT) else pkt[TCP].dport
        if p in (FTP_PORT, TELNET_PORT, POP3_PORT, IMAP_PORT):
            return p
    return None

def parse_dns_findings(pkt, findings):
    # DNS via porta 53 (heurística leve; não parse completo de camadas)
    # Scapy tem camada DNS, mas muitas vezes basta checar texto bruto (Raw).
    if pkt.haslayer(UDP) and (pkt[UDP].sport == DNS_PORT or pkt[UDP].dport == DNS_PORT):
        if pkt.haslayer(Raw):
            data = pkt[Raw].load
            try:
                # Filtra bytes não-imprimíveis para facilitar regex de domínio
                text = re.sub(r'[^ -~]', '.', data.decode(errors="ignore"))
                # Pegar candidatos com pontos
                candidates = re.findall(r'([a-zA-Z0-9\-_]+(?:\.[a-zA-Z0-9\-_]+){1,})', text)
                for name in candidates:
                    name = name.strip(".")
                    if len(name) >= 60 or name.count(".") >= 6:
                        findings.append({
                            "type": "dns_suspicious",
                            "severity": "low",
                            "detail": f"DNS com nome muito longo/muitos labels: {name}"
                        })
                        break
            except Exception:
                pass

def main():
    ap = argparse.ArgumentParser(
        description="Scanner simples de PCAP para achados críticos (credenciais claras, protocolos inseguros, HTTP sensível, DNS suspeito)"
    )
    ap.add_argument("--pcap", default=DEFAULT_PCAP, help=f"Arquivo .pcap (default: {DEFAULT_PCAP})")
    ap.add_argument("--out",  default=DEFAULT_OUT,  help=f"Diretório de saída (default: {DEFAULT_OUT})")
    args = ap.parse_args()

    # Normaliza caminhos e cria out
    pcap_path = os.path.abspath(args.pcap)
    out_dir   = os.path.abspath(args.out)
    os.makedirs(out_dir, exist_ok=True)

    # Mensagem de status
    print(f"[i] PCAP: {pcap_path}")
    print(f"[i] OUT : {out_dir}")

    if not os.path.exists(pcap_path):
        print(f"[ERRO] Arquivo PCAP não encontrado: {pcap_path}")
        print("       Ajuste o caminho com --pcap ou coloque o demo.pcap na mesma pasta do script.")
        sys.exit(1)

    try:
        packets = rdpcap(pcap_path)
    except Exception as e:
        print(f"[ERRO] Falha ao ler o PCAP: {e}")
        sys.exit(1)

    findings = []
    insecure_seen = set()

    for pkt in packets:
        # Protocolos inseguros
        p = is_insecure_proto(pkt)
        if p and p not in insecure_seen:
            name = {FTP_PORT:"FTP", TELNET_PORT:"Telnet", POP3_PORT:"POP3", IMAP_PORT:"IMAP"}.get(p, f"porta {p}")
            findings.append({
                "type": "insecure_protocol",
                "severity": "high" if p in (TELNET_PORT, FTP_PORT) else "medium",
                "detail": f"Tráfego detectado em protocolo inseguro: {name} (porta {p})"
            })
            insecure_seen.add(p)

        # HTTP claro (credenciais / params sensíveis)
        if is_http_packet(pkt):
            payload = pkt[Raw].load
            parse_http_findings(payload, findings)

        # DNS suspeito
        parse_dns_findings(pkt, findings)

    # Ordena por severidade (high>medium>low)
    sev_order = {"high":0, "medium":1, "low":2}
    findings.sort(key=lambda x: sev_order.get(x["severity"], 3))

    # Salvar JSON
    json_path = os.path.join(out_dir, "achados.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({"pcap": pcap_path, "count": len(findings), "findings": findings}, f, ensure_ascii=False, indent=2)

    # Salvar Markdown
    md_path = os.path.join(out_dir, "achados.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# PCAP-Crítico — Achados\n\n")
        f.write(f"- Arquivo analisado: `{pcap_path}`\n")
        f.write(f"- Total de achados: **{len(findings)}**\n\n")
        for a in findings:
            f.write(f"- **[{a['severity'].upper()}] {a['type']}** — {a['detail']}\n")

    print(f"[OK] Relatórios gerados em:\n- {json_path}\n- {md_path}")

if __name__ == "__main__":
    main()