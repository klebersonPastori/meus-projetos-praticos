# Incident Report Analysis: DDoS ICMP Flood

[cite_start]Este repositório contém a análise de um incidente de segurança cibernética focado em um ataque de Negação de Serviço Distribuída (DDoS)[cite: 4, 8]. [cite_start]O projeto documenta um plano de trabalho prático e a resposta a um incidente[cite: 3]. [cite_start]Este documento foi desenvolvido como parte do Google Cybersecurity Professional Certificate da Coursera[cite: 1].

## 📄 Visão Geral do Cenário

[cite_start]A análise foca na empresa KAI MOTORS [cite: 2][cite_start], uma empresa de médio porte que sofreu uma interrupção em seus serviços[cite: 5, 8]. 

* [cite_start]O SOC (Security Operations Center) reportou que todos os serviços de rede pararam de responder repentinamente[cite: 8].
* [cite_start]A interrupção foi causada por uma inundação de pacotes ICMP (ICMP flood), gerando um ataque DDoS[cite: 8].
* [cite_start]A empresa conta com ferramentas de segurança previamente estabelecidas, como Firewall, SIEM e um SOC[cite: 6].
* [cite_start]A equipe de cibersegurança respondeu bloqueando o ataque e desligando temporariamente os serviços não críticos para priorizar a restauração dos essenciais[cite: 8].

## 🛡️ Estrutura de Resposta a Incidentes (NIST CSF)

A análise do evento e o plano de mitigação foram estruturados seguindo os pilares do framework de cibersegurança:

* [cite_start]**Identify (Identificar):** Atores maliciosos alvejaram a empresa com um ataque de ICMP flood, o que afetou toda a rede interna[cite: 8]. [cite_start]Todos os recursos críticos de rede precisaram ser protegidos e restaurados para um estado totalmente operacional[cite: 8].
* [cite_start]**Protect (Proteger):** Foi implementada uma nova regra de firewall para limitar a taxa de pacotes ICMP recebidos[cite: 8]. [cite_start]Em conjunto, um sistema IDS/IPS foi utilizado para filtrar o tráfego ICMP com base em características suspeitas[cite: 8].
* [cite_start]**Detect (Detectar):** A equipe configurou a verificação de endereço IP de origem no firewall para checar a presença de IPs forjados nos pacotes ICMP de entrada[cite: 8]. [cite_start]Também foi implementado um software de monitoramento de rede para detectar padrões de tráfego anormais[cite: 8].
* [cite_start]**Respond (Responder):** Para eventos de segurança futuros, a equipe isolará os sistemas afetados para prevenir maiores interrupções na rede[cite: 12]. [cite_start]A restauração de sistemas e serviços críticos impactados pelo incidente será priorizada[cite: 13]. [cite_start]Posteriormente, os logs de rede serão analisados para identificar atividades suspeitas ou anormais[cite: 14]. [cite_start]Todos os incidentes serão reportados ao supervisor, gerente e ao SOC[cite: 15].
* [cite_start]**Recover (Recuperar):** Para se recuperar do ataque DDoS, o acesso aos serviços de rede deve ser restaurado ao seu estado operacional normal[cite: 16]. [cite_start]No futuro, ataques externos de ICMP flood poderão ser bloqueados diretamente no firewall[cite: 17]. [cite_start]Durante a fase de mitigação, serviços não críticos devem ser desligados temporariamente para reduzir o tráfego interno[cite: 18]. [cite_start]Uma vez que a inundação de pacotes ICMP tenha diminuído, os sistemas e serviços não críticos podem ser religados com segurança[cite: 19].

## 👨‍💻 Autor

[cite_start]**Kleberson Pastori** [cite: 21, 22]
