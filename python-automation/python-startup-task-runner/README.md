python-startup-task-runner

Script simples em Python para abrir automaticamente aplicações do dia a dia no Windows (Microsoft Edge, Outlook e Microsoft Teams), exibindo mensagens de status no terminal.

✨ Funcionalidades

Abre o Microsoft Edge
Abre o Outlook (Office 2016/365)
Abre o Microsoft Teams via protocolo ms-teams:
Mensagens coloridas no terminal indicando o progresso
Pausas controladas com sleep para abertura sequencial

🧰 Tecnologias / Dependências

Sistema Operacional: Windows 10/11
Python: 3.x
Módulos padrão: os, time (sleep)

Nenhuma dependência externa é necessária.



📂 Estrutura do Repositório
.
├─Inicializar_apps.py   # Script principal
├─README.md             # Este document
└─LICENSE(MIT)

▶️ Como usar

Instale o Python 3 (se ainda não tiver) e verifique no terminal:
Shellpython --versionShow more lines

Clone este repositório ou baixe o arquivo:
Shellgit clone https://github.com/<seu-usuario>/<seu-repositorio>.gitcd <seu-repositorio>Show more lines

Execute o script:
Shellpython Inicializar_apps.pyShow more lines

Será exibido um pequeno painel no terminal com o status de cada aplicação aberta.



🔧 Personalização

Os caminhos para os executáveis estão fixos no script. Ajuste conforme a sua instalação:
Python# Microsoft Edgeos.startfile(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")# Outlook (Office16 – ajuste se a sua versão for diferente)os.startfile(r"C:\Program Files\Microsoft Office\root\Office16\OUTLOOK.EXE")# Microsoft Teams pelo protocolo de URLos.system("start ms-teams:")Show more lines
Exemplos de variações comuns

Edge (x64 em pastas padrão)
C:\Program Files\Microsoft\Edge\Application\msedge.exe
Outlook (Office15/2013)
C:\Program Files\Microsoft Office\Office15\OUTLOOK.EXE
Outlook (Click-to-Run 365 pode manter Office16)
C:\Program Files\Microsoft Office\root\Office16\OUTLOOK.EXE


Dica: Para descobrir o caminho exato, clique com o botão direito no atalho do app → Propriedades → Destino.

🚀 Executar na inicialização do Windows (opcional)

Você pode agendar a execução do script ao iniciar o Windows usando o Agendador de Tarefas:

Abra Agendador de Tarefas → Criar Tarefa…
Gatilhos → Ao fazer logon
Ações → Iniciar um programa

Programa/script: python
Adicionar argumentos: C:\caminho\para\Inicializar_apps.py
Iniciar em: C:\caminho\para\o\repositorio


Marque Executar com privilégios mais altos se necessário.


Alternativa: crie um atalho para python Inicializar_apps.py e coloque o atalho na pasta Inicializar (Win+R → shell:startup).

🧪 Teste rápido

Execute o script e verifique se:

Edge abre normalmente;
Outlook inicia (logado);
Teams abre (cliente instalado).


Caso um app não abra, valide:

O caminho no script (os.startfile) está correto?
O aplicativo está instalado?
Há políticas corporativas bloqueando protocolos (para o Teams)?



🧯 Solução de problemas

FileNotFoundError: caminho do executável incorreto → ajuste a string do os.startfile.
Sem saída colorida: alguns terminais podem ignorar códigos ANSI. Use o Prompt/PowerShell padrão ou Windows Terminal.
Teams não abre: verifique se o protocolo ms-teams: está registrado (reinstale o Teams ou use o caminho do executável do Teams como alternativa).

🔐 Nota de segurança

O script não coleta dados nem realiza conexões externas.
Mantenha o repositório sem credenciais ou informações sensíveis.
Se for usar em ambiente corporativo, valide com a equipe de TI/políticas internas.

🗺️ Roadmap (ideias)

 Parametrizar apps via arquivo .ini/.yaml
 Ler lista de apps de um JSON e abrir dinamicamente
 Logs opcionais em arquivo
 Interface simples (Tkinter) para selecionar quais apps abrir
 Versão compilada .exe (PyInstaller)

🤝 Contribuindo
Sinta-se à vontade para abrir Issues e Pull Requests com melhorias, correções ou novas ideias.

📄 Licença

Este projeto está licenciado sob a MIT License.
Confira o arquivo LICENSE para mais detalhes.

🧩 Código-fonte (referência)

O script atual incluso no repositório: