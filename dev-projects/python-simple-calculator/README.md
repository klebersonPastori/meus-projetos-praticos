python-simple-calculator

CLI para operações aritméticas básicas (soma, subtração, multiplicação e divisão) com menu interativo e saída colorida em terminal. 
Usa https://github.com/pwaller/pyfiglet para renderizar o título em ASCII.

🧭 Sumário

#-recursos
#-pré-requisitos
#-instalação
#-uso
#-estrutura
#-erros-comuns
#-roadmap
#-licença

✅ Recursos

Menu interativo no terminal (loop principal).
Validação de entrada com mensagens de erro claras.
Proteção para divisão por zero.
Limpeza de tela crossplatform (cls no Windows, clear no Linux/macOS).
Saída colorida via ANSI escape codes.

🔧 Pré-requisitos
*Python 3.8+
*pip configurado


Dica rápida: pense no app como uma “calculadora de bolso no terminal”: leve, direta e sempre disponível.

📦 Instalação
instale direto:
pip install pyfiglet

▶️ Uso
Execute o script principal:
Shellpython "Calculadora _simples.py"Show more lines.

Menu esperado:
1) ➕ Somar
2) ➖ Subtrair
3) ✖️ Multiplicar
4) ➗ Dividir
5) 🧹 Limpar console
0) ❌ para Sair➡️

Exemplo (soma):
Escolha uma opção: 1
Insira o primeiro número: 10
Insira o segundo número: 5
Resultado: 10.0 + 5.0 = 15.0

📁 Estrutura
.
├── Calculadora _simples.py   # ponto de entrada (menu + operações)
└── requirements.txt          # dependências (pyfiglet)

Principais funções

menu(): loop principal de interação.
somar() | subtrair() | multiplicar() | dividir(): operações com try/except para ValueError.
limpar_tela(): limpa o console de forma portátil.


🧯 Erros comuns

Entrada inválida (ValueError)
Digitar letras em vez de números. O programa captura e exibe:
❌ Entrada inválida: digite apenas números.


Divisão por zero
Mensagem clara e retorno ao menu:
Não é possível dividir por zero.


Interrupção pelo usuário (Ctrl+C)
O app finaliza com:
Encerrado pelo usuário


🗺️ Roadmap

 Testes unitários (pytest) para operações.
 Argumentos via CLI (ex.: --op soma --a 10 --b 5).
 Empacotamento (setuptools) para pip install -e ..
 Suporte a histórico de operações.
 Internacionalização (pt-BR/en-US).


📄 Licença
MIT License © 2026 Kleberson Pastori