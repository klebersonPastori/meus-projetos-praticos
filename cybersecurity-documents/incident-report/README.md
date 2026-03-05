# Incident Report Analysis: DDoS ICMP Flood

Este repositório contém a análise de um incidente de segurança cibernética focado em um ataque de Negação de Serviço Distribuída (DDoS). O projeto documenta um plano de trabalho prático e a resposta a um incidente. Este documento foi desenvolvido como parte do Google Cybersecurity Professional Certificate da Coursera.

## 📄 Visão Geral do Cenário

A análise foca na empresa KAI MOTORS, uma empresa de médio porte que sofreu uma interrupção em seus serviços.

* O SOC (Security Operations Center) reportou que todos os serviços de rede pararam de responder repentinamente.
* A interrupção foi causada por uma inundação de pacotes ICMP (ICMP flood), gerando um ataque DDoS.
* A empresa conta com ferramentas de segurança previamente estabelecidas, como Firewall, SIEM e um SOC.
* A equipe de cibersegurança respondeu bloqueando o ataque e desligando temporariamente os serviços não críticos para priorizar a restauração dos essenciais.

## 🛡️ Estrutura de Resposta a Incidentes (NIST CSF)

A análise do evento e o plano de mitigação foram estruturados seguindo os pilares do framework de cibersegurança:

**Identify (Identificar):** Atores maliciosos alvejaram a empresa com um ataque de ICMP flood, o que afetou toda a rede interna. Todos os recursos críticos de rede precisaram ser protegidos e restaurados para um estado totalmente operacional.
**Protect (Proteger):** Foi implementada uma nova regra de firewall para limitar a taxa de pacotes ICMP recebidos. Em conjunto, um sistema IDS/IPS foi utilizado para filtrar o tráfego ICMP com base em características suspeitas.
**Detect (Detectar):** A equipe configurou a verificação de endereço IP de origem no firewall para checar a presença de IPs forjados nos pacotes ICMP de entrada. Também foi implementado um software de monitoramento de rede para detectar padrões de tráfego anormais.
**Respond (Responder):** Para eventos de segurança futuros, a equipe isolará os sistemas afetados para prevenir maiores interrupções na rede. A restauração de sistemas e serviços críticos impactados pelo incidente será priorizada. Posteriormente, os logs de rede serão analisados para identificar atividades suspeitas ou anormais. Todos os incidentes serão reportados ao supervisor, gerente e ao SOC.
**Recover (Recuperar):** Para se recuperar do ataque DDoS, o acesso aos serviços de rede deve ser restaurado ao seu estado operacional normal. No futuro, ataques externos de ICMP flood poderão ser bloqueados diretamente no firewall. Durante a fase de mitigação, serviços não críticos devem ser desligados temporariamente para reduzir o tráfego interno. Uma vez que a inundação de pacotes ICMP tenha diminuído, os sistemas e serviços não críticos podem ser religados com segurança.

## 👨‍💻 Autor **Kleberson Pastori**
