# 🛡️ Cyber Malicious File Risk Analyzer (CLI)

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![Interface](https://img.shields.io/badge/interface-CLI-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Um scanner simples, rápido e visual de diretórios locais via linha de comando (CLI). O script percorre pastas do sistema e lista arquivos que possuem extensões frequentemente utilizadas como vetores de ataque ou scripts maliciosos (ex: `.exe`, `.bat`, `.ps1`, `.vbs`, `.dll`, `.cmd`).

O projeto conta com uma interface amigável no terminal, exibindo um banner em ASCII, mensagens coloridas para alertas e um resumo final da varredura.

## 🔍 O que a ferramenta faz

* Percorre recursivamente as pastas definidas no código-fonte.
* Identifica extensões suspeitas utilizando a estrutura de dados `set` para uma busca de complexidade $O(1)$, garantindo alta performance.
* Trata exceções e erros comuns (como falta de permissão de leitura ou diretórios inexistentes).
* Exibe a contagem total de arquivos suspeitos encontrados ao final da execução.

## ✅ Requisitos

* **Python:** 3.8 ou superior.
* **Gerenciador de pacotes:** `pip`.

**Dependências Python:**
```text
pyfiglet>=0.8.post1

📦 Instalação
Abra o seu terminal e execute os comandos abaixo para clonar o repositório e preparar o ambiente:

Bash
# 1. Clone o repositório
git clone [https://github.com/SEU-USUARIO/SEU-REPO.git](https://github.com/SEU-USUARIO/SEU-REPO.git)
cd SEU-REPO

# 2. Crie um ambiente virtual (Recomendado)
python -m venv .venv

# 3. Ative o ambiente virtual
# No Windows:
.venv\Scripts\activate
# No Linux/macOS:
source .venv/bin/activate

# 4. Instale as dependências
pip install -r requirements.txt
(Caso prefira rodar sem o arquivo de requisitos, basta executar pip install pyfiglet).

🛠️ Configuração
Antes de rodar, abra o arquivo Analise_potencial_risco_extensao_Python.py e edite os caminhos-alvo no topo do script para refletir o seu usuário e sistema operacional.

Ajuste de Diretórios (Exemplo Windows):

Python
PASTA  = r"C:\Users\<SEU_USUARIO>\Downloads"
PASTA1 = r"C:\Users\<SEU_USUARIO>\Documents"
PASTA2 = r"C:\Users\<SEU_USUARIO>\Desktop"
(Se estiver rodando em ambiente Linux, lembre-se de alterar os caminhos para o padrão Unix, como /home/usuario/Downloads).

Ajuste de Extensões Monitoradas:
Para adicionar ou remover extensões do radar do scanner, edite o conjunto (set) abaixo:

Python
EXT_SUSPEITAS = {".exe", ".bat", ".ps1", ".vbs", ".dll", ".cmd"}
▶️ Uso
Com o ambiente ativado e configurado, execute o script:

Bash
python Analise_potencial_risco_extensao_Python.py
Saída Esperada:

Plaintext
🔍 Verificando arquivos suspeitos em: C:\Users\<USUARIO>\Downloads
🔍 Verificando arquivos suspeitos em: C:\Users\<USUARIO>\Documents
🔍 Verificando arquivos suspeitos em: C:\Users\<USUARIO>\Desktop
________________________________________________________________________________

⚠️ Arquivo(s) potencialmente perigoso encontrado em 'DOWNLOADS': setup.exe
⚠️ Arquivo(s) potencialmente perigoso encontrado em 'DESKTOP': script.ps1
________________________________________________________________________________

Resumo: 2 arquivo(s) potencialmente perigoso(s) encontrado(s).
📄 Estrutura do Repositório
Plaintext
.
├── Analise_potencial_risco_extensao_Python.py  # Script principal do scanner
└── requirements.txt                            # Dependências (pyfiglet)
🚧 Limitações e Observações
Não é um antivírus: A ferramenta funciona exclusivamente baseada em extensões de arquivos, ela não realiza análise de conteúdo, assinatura, comportamento ou hash.

Falsos Positivos: É normal e esperado que arquivos totalmente legítimos sejam sinalizados apenas por possuírem extensões como .exe ou .dll.

Permissões: A varredura em diretórios restritos do sistema raiz pode exigir execução com privilégios elevados (Administrador/Root).

🗺️ Roadmap (Melhorias Futuras)
[ ] Implementar leitura de pastas via argumentos CLI (--paths) utilizando a biblioteca argparse.

[ ] Adicionar suporte à exportação de relatórios em .csv ou .json.

[ ] Mover a configuração de extensões para um arquivo externo config.yaml.

[ ] Criar logs estruturados e níveis de verbosidade (ex: -v, --quiet).

[ ] Configurar um Pipeline de CI simples com Lint e testes automatizados.

📜 Licença e Autor
Este projeto está licenciado sob a MIT License © 2026 Kleberson Pastori.
