# 🏢 Laboratório Prático: Active Directory na AWS 

> **Autor:** Kleberson Pastori  
> **Domínio:** `SEU-DOMINIO.LOCAL`  
> **Plataforma:** AWS EC2 + Windows Server 

## 📋 Visão Geral
Este repositório documenta a implementação de um laboratório completo de **Active Directory (AD)** utilizando instâncias EC2 na **AWS**. O projeto simula um ambiente corporativo real, configurando um servidor Windows como Controlador de Domínio (Domain Controller) e realizando a integração (join) de uma máquina cliente.

## 🛠️ Tecnologias e Recursos Utilizados
* **Nuvem:** Amazon Web Services (AWS EC2)
* **Sistema Operacional:** Windows Server (Domain Controller) e Windows 10/11 (Client)
* **Serviços:** Active Directory Domain Services (AD DS), DNS Server
* **Protocolos:** Kerberos, LDAP, IPv4

## 🎯 Objetivos do Laboratório
O projeto foi desenvolvido para validar as seguintes competências práticas:
1. **Provisionamento de Infraestrutura:** Criação e configuração de instâncias EC2 e Security Groups na AWS.
2. **Promoção a Domain Controller:** Instalação do AD DS e configuração da floresta e domínio.
3. **Serviços de Rede:** Configuração de DNS interno para resolução de nomes do domínio.
4. **Gestão de Identidades (IAM):** Criação de Unidades Organizacionais (OUs) e usuários via Active Directory Users and Computers (ADUC).
5. **Ingresso de Máquinas:** Configuração de rede na máquina cliente e execução do "Join" no domínio.
6. **Validação de Autenticação:** Login bem-sucedido na máquina cliente utilizando credenciais gerenciadas pelo domínio.

## 🛡️ Relevância para Cibersegurança (SOC / Blue Team)
A compreensão profunda do Active Directory é fundamental para operações de Defesa Cibernética. Este laboratório proporciona a base prática para entender como os ataques ocorrem e como detectá-los, abordando:

* **Análise de Logs do Windows (Event Viewer):** Compreensão prática de eventos críticos de autenticação, como `Event ID 4624` (Logon bem-sucedido), `4625` (Falha de Logon) e `4768` (Ticket Kerberos solicitado).
* **Superfície de Ataque do AD:** Visão interna de como protocolos como Kerberos e LDAP operam, facilitando o estudo de técnicas como *Pass-the-Hash*, *Kerberoasting* e *DCSync*.
* **Controle de Acesso:** Administração de privilégios e políticas de grupo (GPOs) para aplicar o princípio do menor privilégio.

## 🚀 Como este ambiente foi construído
*(Opcional: Você pode adicionar aqui um breve passo a passo ou capturas de tela do Server Manager, da tela de Join ou do Event Viewer mostrando o login do usuário)*

---
*Projeto desenvolvido para aprimoramento prático em Infraestrutura e Segurança da Informação.*
