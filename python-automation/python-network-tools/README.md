# 🛠️ Python Network Tools (GUI)

![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)
![Framework](https://img.shields.io/badge/PySide6-GUI-brightgreen.svg)
![OS](https://img.shields.io/badge/OS-Windows-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

> Ferramenta desktop profissional para diagnóstico de rede e operações
> de cibersegurança com interface gráfica moderna.

------------------------------------------------------------------------

## 🚀 Visão Geral

O **Python Network Tools** é um painel centralizado para execução de
comandos de rede no Windows, focado em produtividade, análise rápida e
uso em ambientes corporativos.

Elimina a dependência de terminal manual e organiza os resultados com
logs estruturados e leitura otimizada.

------------------------------------------------------------------------

## 🖥️ Interface (Preview)

> 📌 Recomendado adicionar um GIF aqui futuramente:

    assets/demo.png

------------------------------------------------------------------------

## ✨ Features

-   Interface moderna (UI/UX clean)
-   Execução assíncrona com QProcess
-   Console com timestamp e logs estruturados
-   Interrupção forçada de processos (taskkill)
-   Validação de IP e portas
-   Execução segura (anti-concorrência)
-   Atalhos para CMD e RDP

------------------------------------------------------------------------

## 🧰 Comandos

  Categoria       Comando
  --------------- ------------------------------
  Conectividade   PING
  Configuração    IPCONFIG /ALL
  Sistema         HOSTNAME
  Roteamento      TRACERT / ROUTE PRINT
  DNS             NSLOOKUP / Reverse DNS
  Segurança       NETSTAT / TEST-NETCONNECTION
  Rede local      ARP -A
  Domínio         GPRESULT

------------------------------------------------------------------------

## ⚙️ Arquitetura

-   Python
-   PySide6 (QMainWindow)
-   QProcess (execução assíncrona)
-   QTextEdit (console)
-   Encoding cp850

------------------------------------------------------------------------

## ▶️ Execução

``` bash
pip install PySide6
python python-network-tools.py
```

------------------------------------------------------------------------

## ⚡ Execução via .bat

``` bat
set PYTHON_EXE=C:\Python314\pythonw.exe
```

✔ Executa sem abrir terminal\
✔ Ideal para usuários finais

------------------------------------------------------------------------

## 📦 Estrutura do Projeto

    📁 project/
     ┣ 📄 python-network-tools.py
     ┣ 📄 Run_Python_Program.bat
     ┗ 📁 assets/

------------------------------------------------------------------------

## 🎯 Casos de Uso

-   SOC / Blue Team
-   Help Desk
-   Infraestrutura
-   Estudo de redes

------------------------------------------------------------------------

## 🧠 Diferenciais

-   Foco em uso real (não apenas acadêmico)
-   Interface amigável para operação rápida
-   Aplicável em ambiente corporativo
-   Base para evolução DevSecOps

------------------------------------------------------------------------

## 🗺️ Roadmap

-   [ ] Dark Mode
-   [ ] Exportação de logs
-   [ ] Histórico de comandos
-   [ ] Versão .exe
-   [ ] Multiplataforma

------------------------------------------------------------------------

## 👨‍💻 Autor

**Kleberson Pastori**\
Software Engineering \| Cybersecurity

------------------------------------------------------------------------

## ⭐ Contribuição

Sinta-se livre para abrir PRs ou sugestões.
