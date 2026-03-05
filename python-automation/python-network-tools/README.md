=====================================================================
                    FERRAMENTAS DE REDE (GUI)
=====================================================================

Aplicativo desktop desenvolvido em Python com PySide6 para execução
visual de comandos de rede no Windows.

Autor: Kleberson Pastori
Projeto para fins educacionais, profissionais e de portfólio.

---------------------------------------------------------------------
                         VISÃO GERAL
---------------------------------------------------------------------

O python-network-tools – Ferramentas de Rede funciona como um painel central de
diagnóstico de rede.

Ao invés de digitar comandos manualmente no Prompt de Comando, o
usuário executa tarefas comuns de rede através de botões, com a
saída exibida em um console integrado.

>>> Analogia prática:
>>> É como um “canivete suíço” para rede no Windows, reunindo
>>> várias ferramentas em um único lugar.

---------------------------------------------------------------------
                   PRINCIPAIS FUNCIONALIDADES
---------------------------------------------------------------------

✔ Interface gráfica (GUI) simples e intuitiva
✔ Execução de comandos nativos do Windows
✔ Console interno com:
    - Timestamp (data e hora)
    - Separadores visuais entre comandos
✔ Validação de:
    - Endereço IP (IPv4)
    - Porta TCP (1 a 65535)
✔ Abertura de ferramentas externas:
    - Prompt de Comando (CMD)
    - Conexão de Área de Trabalho Remota (RDP)

---------------------------------------------------------------------
                      INTERFACE DO SISTEMA
---------------------------------------------------------------------

Campos de entrada:
- IP       → Ex.: 8.8.8.8
- Domínio  → Ex.: google.com
- Porta    → Ex.: 443

Console:
- Exibe a saída de todos os comandos
- Somente leitura
- Fonte otimizada para visualização

---------------------------------------------------------------------
                      COMANDOS DISPONÍVEIS
---------------------------------------------------------------------

[ PING ]
Testa conectividade com um IP ou domínio.
Uso comum: verificar se um servidor ou site responde.

[ IPCONFIG /ALL ]
Exibe todas as configurações de rede da máquina.
IP, gateway, DNS, DHCP e adaptadores.

[ HOSTNAME ]
Mostra o nome do computador local.
Com IP informado, tenta resolução reversa (ping -a).

[ TRACERT ]
Mostra o caminho que os pacotes percorrem até o destino.
Usado para identificar gargalos ou falhas de rota.

[ TESTE DE PORTA – Test-NetConnection ]
Testa se uma porta TCP está acessível.
Exemplo prático: verificar se a porta 443 (HTTPS) está aberta.
Não depende do Telnet instalado.

[ NSLOOKUP ]
Consulta DNS para resolução de nomes de domínio.

[ NETSTAT -AN ]
Lista conexões ativas e portas em uso.
Muito usado em análises de segurança.

[ ARP -A ]
Exibe a tabela ARP local (IP ↔ MAC).

[ ROUTE PRINT ]
Mostra a tabela de rotas do sistema.

[ GPRESULT /R ]
Lista políticas de grupo (GPOs) aplicadas à máquina.

[ ABRIR CMD ]
Abre o Prompt de Comando externamente.

[ ABRIR RDP ]
Abre o cliente de Conexão Remota (mstsc).

---------------------------------------------------------------------
REQUISITOS DO SISTEMA
---------------------------------------------------------------------

Sistema Operacional:
- Windows 10 ou superior;

Software:
- Python 3.9 ou superior;
- Biblioteca PySide6;

Observação:
Este projeto foi desenvolvido especificamente para Windows.

---------------------------------------------------------------------
ARQUITETURA E DECISÕES TÉCNICAS
---------------------------------------------------------------------

Linguagem:
- Python

Interface:
- PySide6 (QMainWindow)

Execução de comandos:
- QProcess (assíncrono)

Saída:
- QTextEdit em modo somente leitura

>>> Benefício técnico:
>>> O uso do QProcess permite executar comandos do sistema sem
>>> travar a interface gráfica.

---------------------------------------------------------------------
                          CASOS DE USO
---------------------------------------------------------------------

- Suporte técnico e help desk;
- Estudantes de redes e cibersegurança;
- Ambientes corporativos;
- Treinamento e laboratórios;
- Analistas Blue Team / SOC;

---------------------------------------------------------------------
                   MELHORIAS FUTURAS (ROADMAP)
---------------------------------------------------------------------

[ ] Tema escuro;
[ ] Exportação de logs para arquivo .txt;
[ ] Novos comandos de rede;
[ ] Melhor tratamento de erros;
[ ] Versão multiplataforma (futuro);
[ ] Interface instalavel e estavel. 

---------------------------------------------------------------------
LICENÇA
---------------------------------------------------------------------

Defina conforme necessidade (sugestão: MIT License).

---------------------------------------------------------------------
SOBRE O AUTOR
---------------------------------------------------------------------

Kleberson Pastori
Estudante de Engenharia de Software
Estagiário em Cibersegurança na AutoEver Brasil

Foco em:
- Blue Team
- SOC
- Segurança defensiva
- Automação de tarefas de rede

Projeto desenvolvido para aprendizado, uso prático e portfolio profissional.