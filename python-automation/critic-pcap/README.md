<p align="center">
  <img src="https://img.shields.io/badge/PCAP%20ANALYZER-Blue%20Team%20Automation-00FF9C?style=for-the-badge&logo=hackaday&logoColor=black" />
</p>

<h1 align="center">💻🔍 PCAP Critical Scanner</h1>
<p align="center">
  Detecção automática de riscos em tráfego de rede • Segurança ofensiva e defensiva
</p>

# 🛰️ PCAP Critical Scanner
**Analisador automático de tráfego para achados críticos de segurança (Blue Team)**  
Ferramentas: **Python + Scapy**

Este projeto contém duas ferramentas simples e diretas para ajudar analistas (SOC / Blue Team / Estudantes) a **detectar rapidamente riscos comuns em arquivos PCAP**, incluindo:

- Credenciais transmitidas em claro  
- Protocolos inseguros (FTP, Telnet, POP3 sem TLS)  
- HTTP sem criptografia contendo parâmetros sensíveis  
- Consultas DNS suspeitas indicando possível exfiltração  

---

## 📌 Objetivo do Projeto  

Este repositório foi criado com foco em **aprendizado prático de análise de tráfego** e **automação defensiva**, simulando um cenário real onde um analista precisa validar rapidamente se um tráfego capturado contém indícios de risco.

O projeto demonstra:

- Conhecimentos de **protocolos de rede**  
- Identificação de **pontos fracos reais** encontrados no dia a dia do SOC  
- Capacidade de **automação com Python**  
- Familiaridade com ferramentas como **Wireshark** e **Scapy**  
- Boas práticas de organização e entrega técnica para uso em portfólio  

---

# 🧩 Arquivos principais

### **1. scanner.py**  
Script que **analisa um PCAP** e gera um relatório com achados críticos.

Ele detecta automaticamente:

| Categoria | Descrição |
|----------|-----------|
| Credenciais em claro | HTTP Basic Auth, Telnet, FTP, POP3 |
| Parâmetros sensíveis | Campos como `password=`, `token=`, etc |
| Protocolos inseguros | FTP, Telnet, POP3, IMAP sem TLS |
| DNS suspeito | Domínios extremamente longos ou com muitos labels |

Saídas geradas automaticamente:

- `achados.json`  
- `achados.md`  

---

### **2. pcap-log-generator.py**  
Gerador de um **PCAP 100% válido (Ethernet/IP/TCP/UDP)** contendo tráfego inseguro *didático*, ideal para testes e demonstrações.

Este arquivo gera pacotes como:

- HTTP Basic Auth  
- HTTP com `password=`  
- FTP USER/PASS  
- Telnet com login/senha  
- POP3 sem TLS  
- DNS com nome extremamente longo  

Serve como ambiente de teste seguro e livre de dados reais da empresa.

---

# 📁 Estrutura do Projeto

/
├── scanner.py              # Scanner dos pacotes
├── pcap-log-generator.py   # Gerador de PCAP sintético
├── demo.pcap               # PCAP gerado para testes (seguro)
├── reports/                # Saída dos relatórios
│   ├── achados.json
│   └── achados.md
└── README.md

---

# 🚀 Como Executar

## 1. Instale as dependências
```bash
pip install scapy

2. Gere o arquivo PCAP de teste
Shellpython pcap-log-generator.pyShow more lines
Você verá:
demo.pcap gerado com 7 pacotes!

3. Rode o scanner
Shellpython scanner.pyShow more lines
Saídas geradas em ./reports

✔ Exemplos do que o analisador detecta
🔐 Credenciais em claro
[HIGH] http_basic_creds — Credenciais em claro (Basic): user:password

🛑 Parâmetros sensíveis em HTTP sem TLS
[MEDIUM] http_sensitive_param — ...username=alice&password=Summer2026!...

⚠️ Protocolos inseguros
[HIGH] insecure_protocol — FTP (porta 21)
[HIGH] insecure_protocol — Telnet (porta 23)

🛰️ DNS Suspeito
[LOW] dns_suspicious — domínio muito longo/muitos labels

Autor: Kleberson Pastori – Cybersecurity (Blue Team / SOC)
