# 🧮 Python Simple Calculator (CLI)

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![Interface](https://img.shields.io/badge/interface-CLI-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Uma calculadora de bolso direto no seu terminal! Este projeto é uma CLI (Command Line Interface) leve, direta e sempre disponível para operações aritméticas básicas. 

O script conta com um menu interativo, validação robusta de entradas do usuário e uma interface estilizada com saída colorida e um banner em ASCII renderizado com a biblioteca [pyfiglet](https://github.com/pwaller/pyfiglet).

## 🧭 Sumário
* [Recursos](#-recursos)
* [Pré-requisitos](#-pré-requisitos)
* [Instalação](#-instalação)
* [Como Usar](#️-como-usar)
* [Estrutura do Projeto](#-estrutura-do-projeto)
* [Tratamento de Erros](#-tratamento-de-erros)
* [Roadmap](#️-roadmap)
* [Licença](#-licença)

## ✅ Recursos

* **Menu Interativo:** Loop principal contínuo para realizar múltiplas operações sem precisar reiniciar o script.
* **Validação de Entrada:** Tratamento rigoroso de exceções com mensagens de erro claras para o usuário.
* **Proteção Matemática:** Prevenção contra travamentos por divisão por zero.
* **Limpeza de Tela (*Cross-platform*):** Função nativa que identifica o sistema operacional limpa o console adequadamente (`cls` no Windows, `clear` no Linux/macOS).
* **UI no Terminal:** Saída formatada e colorida utilizando *ANSI escape codes*.

## 🔧 Pré-requisitos

* **Python:** 3.8 ou superior.
* **Gerenciador de pacotes:** `pip` configurado no PATH.

## 📦 Instalação

Clone o repositório e instale a dependência necessária para a renderização do título:

```bash
# Baixe os arquivos do projeto
git clone [https://github.com/SEU-USUARIO/SEU-REPO.git](https://github.com/SEU-USUARIO/SEU-REPO.git)
cd SEU-REPO

# Instale a dependência de fonte ASCII
pip install pyfiglet
# ou
pip install -r requirements.txt

▶️ Como Usar
Execute o script principal diretamente pelo terminal:

Bash
python "Calculadora _simples.py"
Menu Esperado:

Plaintext
1) ➕ Somar
2) ➖ Subtrair
3) ✖️ Multiplicar
4) ➗ Dividir
5) 🧹 Limpar console
0) ❌ Sair
➡️ Escolha uma opção:
Exemplo de Execução (Soma):

Plaintext
Escolha uma opção: 1
Insira o primeiro número: 10
Insira o segundo número: 5
Resultado: 10.0 + 5.0 = 15.0
📁 Estrutura do Projeto
Plaintext
.
├── Calculadora _simples.py   # Ponto de entrada (Menu interativo + operações lógicas)
└── requirements.txt          # Lista de dependências externas (pyfiglet)
Principais Funções Internas:

menu(): Gerencia o loop principal de interação com o usuário.

somar(), subtrair(), multiplicar(), dividir(): Isolam a lógica matemática com blocos try/except para capturar ValueError.

limpar_tela(): Mantém a interface do terminal limpa de forma portátil entre diferentes sistemas operacionais.

🧯 Tratamento de Erros Comuns
O aplicativo foi construído para ser resiliente a erros de digitação e operações inválidas:

Entrada Inválida (ValueError): Se o usuário digitar letras ou símbolos em vez de números, o programa captura a exceção, não "quebra" e exibe: ❌ Entrada inválida: digite apenas números.

Divisão por Zero (ZeroDivisionError): Intercepta operações matematicamente impossíveis, exibe a mensagem Não é possível dividir por zero. e retorna ao menu principal.

Interrupção pelo Usuário (KeyboardInterrupt): Caso o usuário pressione Ctrl+C, o app finaliza graciosamente com a mensagem Encerrado pelo usuário.

🗺️ Roadmap (Melhorias Futuras)
[ ] Implementar Testes Unitários utilizando o framework pytest.

[ ] Adicionar suporte a execução via argumentos CLI (ex.: python calc.py --op soma --a 10 --b 5).

[ ] Empacotamento do projeto via setuptools para permitir instalação global com pip install -e ..

[ ] Criar um log de histórico com as últimas operações realizadas.

[ ] Internacionalização de idiomas (Suporte a pt-BR / en-US).

📄 Licença e Autor
Este projeto está licenciado sob a MIT License © 2026 Kleberson Pastori.


No seu *Roadmap*, você mencionou a implementação de testes unitários com o `pytest`. Essa é uma habilidade valiosíssima e muito cobrada em processos seletivos para desenvolvimento. 

Você gostaria que eu escrevesse o arquivo de testes (`test_calculadora.py`) validando as fu
