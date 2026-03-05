\# 🏢 Active Directory na AWS – Domain Controller + Usuários + Join de Máquina



> Autor: \*\*Kleberson Pastori\*\*  

> Domínio: \*\*SEU-DOMINIO.LOCAL\*\*  

> Plataforma: \*\*AWS EC2 + Windows Server (Domain Controller)\*\*



Um laboratório completo de \*\*Active Directory\*\* implementado em uma VM Windows Server na \*\*AWS\*\*, incluindo:

\- Promoção a \*\*Domain Controller\*\*

\- \*\*DNS interno\*\* do domínio

\- Criação de \*\*usuários no ADUC\*\*

\- \*\*Join\*\* de máquina cliente ao domínio

\- Login com credenciais de domínio (validação Kerberos/LDAP)



O projeto demonstra habilidades práticas de \*\*Infra Windows\*\*, \*\*Redes\*\*, \*\*Segurança\*\* e \*\*Administração de Domínio\*\* — essenciais para \*\*SOC / Blue Team\*\*.



---



\## 📸 Demonstração



| Etapa | Print |

|------|------|

| Usuário criado no ADUC | !\[ADUC usuário](docs/aduc-usuario.png) |

| Propriedades da conta no AD | !\[Propriedades de conta](docs/aduc-propriedades-conta.png) |

| VM DC na AWS (detalhes/overlay) | !\[EC2 DC](docs/aws-ec2-dc.png) |

| Join de máquina ao domínio | !\[Join domínio](docs/join-dominio.png) |

| Login com credenciais do domínio | !\[Logon](docs/logon-dominio.png) |



> \*\*Dica:\*\* mantenha os arquivos exatamente com esses nomes em `/docs`.  

> Se preferir, me envie os prints e eu padronizo os nomes/legendagem.



---



\## 🏗️ Arquitetura

