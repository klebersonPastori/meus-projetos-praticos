# 🚀 Python Startup Task Runner

![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)
![OS](https://img.shields.io/badge/OS-Windows-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Um script simples e eficiente em Python para automatizar a abertura de aplicativos essenciais do dia a dia no Windows (Microsoft Edge, Outlook e Microsoft Teams). O script exibe mensagens de status com cores diretamente no terminal, acompanhando o progresso da inicialização.

## ✨ Funcionalidades

* 🌐 **Abre o Microsoft Edge** automaticamente.
* 📧 **Abre o Outlook** (Office 2016/365).
* 💬 **Abre o Microsoft Teams** utilizando o protocolo nativo `ms-teams:`.
* 🎨 **Feedback Visual:** Mensagens coloridas no terminal indicando o status de cada aplicação.
* ⏱️ **Controle de Fluxo:** Pausas controladas (`sleep`) para garantir uma abertura sequencial e não sobrecarregar o sistema.

## 🧰 Tecnologias e Dependências

* **Sistema Operacional:** Windows 10/11
* **Linguagem:** Python 3.x
* **Módulos Nativos:** `os`, `time`

> **Nota:** Nenhuma dependência externa (como bibliotecas do `pip`) é necessária para a versão básica.

## 📂 Estrutura do Repositório

```text
.
├── Inicializar_apps.py   # Script principal
├── README.md             # Documentação do projeto
└── LICENSE               # Licença MIT
