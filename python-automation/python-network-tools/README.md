# 🛠️ Python Network Tools (GUI)

![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)
![Framework](https://img.shields.io/badge/PySide6-GUI-brightgreen.svg)
![OS](https://img.shields.io/badge/OS-Windows-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Aplicativo desktop desenvolvido em **Python + PySide6** que atua como um
painel centralizado para execução e diagnóstico de comandos de rede no
Windows.

A ferramenta elimina a necessidade de uso direto do Prompt de Comando,
permitindo executar operações críticas de rede e segurança através de
uma interface gráfica moderna, com saída detalhada em tempo real.

------------------------------------------------------------------------

## ✨ Principais Funcionalidades

-   Interface moderna e responsiva
-   Execução assíncrona (QProcess)
-   Console com timestamp e logs organizados
-   Botão de parada de processos (taskkill)
-   Validação de IP e portas
-   Execução segura (1 comando por vez)
-   Atalhos para CMD e RDP

------------------------------------------------------------------------

## 🧰 Comandos Disponíveis

PING, IPCONFIG, HOSTNAME, TRACERT, NSLOOKUP, NETSTAT, ARP, ROUTE,
GPRESULT, REVERSE DNS, TEST-NETCONNECTION, RDP, CMD

------------------------------------------------------------------------

## ⚙️ Arquitetura

Python + PySide6 + QProcess\
Console com QTextEdit\
Encoding cp850

------------------------------------------------------------------------

## 💻 Requisitos

Windows 10+\
Python 3.9+\
PySide6

------------------------------------------------------------------------

## ▶️ Execução via .bat

Arquivo: Run_Python_Program.bat

Configurar:

set PYTHON_EXE=C:`\Python314`{=tex}`\pythonw`{=tex}.exe

Executar com duplo clique.

------------------------------------------------------------------------

## 👨‍💻 Autor

Kleberson Pastori\
Engenharia de Software \| Cibersegurança
