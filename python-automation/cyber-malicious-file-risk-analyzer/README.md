cyber-malicious-file-risk-analyzer (CLI)

Scanner simples de diretórios locais que lista arquivos com extensões potencialmente perigosas (.exe, .bat, .ps1, .vbs, .dll, .cmd). 
Exibe banner em ASCII, mensagens coloridas e um resumo final.

🔍 O que faz

Percorre recursivamente pastas definidas no código.
Identifica extensões suspeitas usando um set para busca O(1).
Trata erros comuns (permissão e diretório inexistente).
Mostra contagem total de arquivos encontrados.

✅ Requisitos

*Python 3.8+
*pip instalado

Dependências Python
Plain Textpyfiglet>=0.8.post1Show more lines
📦 Instalação
Plain Textgit clone https://github.com/<seu-usuario>/<seu-repo>.gitcd <seu-repo># (Opcional) ambiente virtualpython -m venv .venv# Windows.venv\Scripts\activate# Linux/macOSsource .venv/bin/activatepip install -r requirements.txt``Show more lines

Se não usar requirements.txt: pip install pyfiglet

🛠️ Configuração

Edite os caminhos-alvo no topo do arquivo para refletir seu usuário/sistema:
PythonPASTA  = r"C:\Users\<SEU_USUARIO>\Downloads"PASTA1 = r"C:\Users\<SEU_USUARIO>\Documents"PASTA2 = r"C:\Users\<SEU_USUARIO>\Desktop"Show more lines

Para alterar as extensões monitoradas:
PythonEXT_SUSPEITAS = {".exe", ".bat", ".ps1", ".vbs", ".dll", ".cmd"}``Show more lines

▶️ Uso
Execute o script:
Shell# Windows / Linux / macOSpython Analise_potencial_risco_extensao_Python.pyShow more lines
Saída esperada (exemplo):
🔍 Verificando arquivos suspeitos em: C:\Users\<USUARIO>\Downloads
🔍 Verificando arquivos suspeitos em: C:\Users\<USUARIO>\Documents
🔍 Verificando arquivos suspeitos em: C:\Users\<USUARIO>\Desktop
____________________________________________________________________________________________________
⚠️ Arquivo(s) potencialmente perigoso encontrado em 'DOWNLOADS': setup.exe
⚠️ Arquivo(s) potencialmente perigoso encontrado em 'DESKTOP': script.ps1
____________________________________________________________________________________________________

Resumo: 2 arquivo(s) potencialmente perigoso(s) encontrado(s).

📄 Estrutura
.
├── Analise_potencial_risco_extensao_Python.py  # script principal (scanner)
└── requirements.txt                             # dependências (pyfiglet)

🚧 Limitações e observações

Não é um antivírus: apenas sinaliza por extensão; não faz análise de conteúdo.
Falsos positivos: arquivos legítimos podem ser marcados pela extensão.
Permissões: alguns diretórios podem exigir privilégios elevados.
Plataforma: caminhos padrão estão voltados a Windows; ajuste para Linux/macOS conforme necessário.

🗺️ Roadmap (idéas rápidas)

 Ler pastas via argumentos CLI (--paths), com argparse.
 Exportar relatório em CSV/JSON.
 Configurar extensões via arquivo config.yaml.
 Logs estruturados e nível de verbosidade (-v, --quiet).
 Pipeline de CI com lint/teste.
 
 📜 Licença
MIT License © 2026 Kleberson Pastori