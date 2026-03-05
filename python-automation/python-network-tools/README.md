# 🛠️ Python Network Tools (GUI)

![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)
![Framework](https://img.shields.io/badge/PySide6-GUI-brightgreen.svg)
![OS](https://img.shields.io/badge/OS-Windows-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Um aplicativo desktop desenvolvido em Python com a biblioteca **PySide6** que funciona como um painel central visual para execução e diagnóstico de comandos de rede no Windows. 

Em vez de digitar comandos manualmente no Prompt de Comando, o usuário executa tarefas essenciais de rede e cibersegurança através de uma interface simples e intuitiva, com a saída exibida em um console integrado. É um verdadeiro "canivete suíço" para a administração de redes.

## ✨ Principais Funcionalidades

* **Interface Gráfica (GUI):** Simples, responsiva e intuitiva.
* **Execução Nativa:** Roda comandos nativos do Windows diretamente pelo app.
* **Console Interno Inteligente:** Exibe a saída dos comandos com timestamp (data e hora) e separadores visuais para facilitar a leitura.
* **Validação de Entrada:** Validação automática de endereços IPv4 e portas TCP (1 a 65535).
* **Atalhos Externos:** Botões rápidos para abrir o Prompt de Comando (CMD) e a Conexão de Área de Trabalho Remota (RDP / mstsc).

## 🧰 Comandos de Rede Disponíveis

| Comando | Descrição | Uso Prático / SOC |
| :--- | :--- | :--- |
| **`PING`** | Testa a conectividade com um IP ou domínio. | Verificar se um servidor ou host está ativo e respondendo. |
| **`IPCONFIG /ALL`** | Exibe as configurações completas de rede. | Obter detalhes de IP, Gateway, DNS, DHCP e adaptadores físicos. |
| **`HOSTNAME`** | Mostra o nome do computador local. | Com um IP informado, tenta resolução reversa (`ping -a`). |
| **`TRACERT`** | Mostra a rota dos pacotes até o destino. | Identificar gargalos, falhas de rota ou bloqueios de firewall. |
| **`TEST-NETCONNECTION`** | Testa se uma porta TCP está acessível. | Verificar se portas específicas (ex: 443, 3389) estão abertas sem precisar do Telnet. |
| **`NSLOOKUP`** | Realiza consultas DNS. | Validar a resolução de nomes de domínio e apontamentos de servidores. |
| **`NETSTAT -AN`** | Lista todas as conexões e portas ativas. | Essencial em cibersegurança para caça a ameaças e análise de portas expostas. |
| **`ARP -A`** | Exibe a tabela ARP local. | Mapear a relação entre endereços IP e endereços físicos (MAC). |
| **`ROUTE PRINT`** | Mostra a tabela de rotas do sistema. | Analisar como o tráfego de rede está sendo direcionado. |
| **`GPRESULT /R`** | Lista as políticas de grupo (GPOs). | Verificar quais políticas de domínio estão sendo aplicadas à máquina. |

## ⚙️ Arquitetura e Decisões Técnicas

* **Linguagem:** Python
* **Interface:** PySide6 (`QMainWindow`)
* **Execução Assíncrona:** A execução dos comandos de rede utiliza o módulo `QProcess`. Isso garante que a interface gráfica não congele (freeze) enquanto um comando demorado (como um `tracert`) está rodando em segundo plano.
* **Saída de Dados:** Console utilizando `QTextEdit` em modo somente leitura.

## 💻 Requisitos do Sistema

* **Sistema Operacional:** Windows 10 ou superior (Projeto otimizado para ambiente Microsoft).
* **Software:** Python 3.9+
* **Dependências:** `PySide6`

## 🎯 Casos de Uso

* Analistas Blue Team e operadores de SOC.
* Equipes de Suporte Técnico e Help Desk.
* Estudantes de Redes e Cibersegurança.
* Ambientes corporativos para troubleshooting rápido.

## 🗺️ Roadmap (Melhorias Futuras)

- [ ] Implementar Tema Escuro (Dark Mode).
- [ ] Exportação de logs de resultados para arquivo `.txt`.
- [ ] Inclusão de novos comandos avançados de rede.
- [ ] Aprimorar o tratamento de erros e exceções.
- [ ] Criar um instalador estável executável (`.exe`).
- [ ] Adaptar o código para uma versão multiplataforma no futuro (Linux/macOS).

## 👨‍💻 Sobre o Autor

**Kleberson Pastori** *Estudante de Engenharia de Software | Estagiário em Cibersegurança na AutoEver Brasil*

Foco de estudo e atuação: Blue Team, SOC, Segurança Defensiva e Automação de Tarefas. Projeto desenvolvido para aprendizado, uso prático diário e composição de portfólio profissional.

