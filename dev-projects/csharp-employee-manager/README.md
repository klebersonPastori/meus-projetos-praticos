# 📦 Nexus Dynamics --- Controle de Logística Industrial

O **Nexus Dynamics** é uma aplicação desktop de alta performance
desenvolvida em **C#**, projetada para otimizar o fluxo de distribuição
de benefícios (como cestas de Natal e alimentos) em ambientes
industriais e logísticos.

O sistema prioriza **rastreabilidade completa**, **eficiência
operacional** e uma **experiência de usuário (UX) fluida** em terminais
de consulta rápida.

------------------------------------------------------------------------

## ✨ Principais Funcionalidades

-   🌙 **Interface Dark Mode**\
    UI moderna e intuitiva, reduzindo fadiga visual em ambientes de uso
    contínuo.

-   🔐 **Controle de Acesso**\
    Tela de login administrativo para proteção de funções críticas
    (registro e exportação).

-   ⚡ **Validação em Tempo Real**\
    Prevenção de duplicidade de retiradas com feedback visual:

    -   🟢 Liberado para retirada\
    -   🟠 Retirada já realizada

-   💾 **Persistência de Dados**\
    Armazenamento leve e eficiente utilizando arquivos **JSON**,
    garantindo portabilidade.

-   📊 **Exportação de Relatórios**\
    Geração de arquivos **CSV** com seleção de diretório via interface
    (SaveFileDialog).

------------------------------------------------------------------------

## 🚀 Como Executar

### 👨‍💻 Para Desenvolvedores

1.  Clone o repositório:

    ``` bash
    git clone https://github.com/klebersonPastori/meus-projetos-praticos.git
    ```

2.  Abra o arquivo: Nexus_1.\_0.sln

3.  Utilize o Visual Studio 2022 ou superior

4.  Certifique-se de que os arquivos abaixo estejam na pasta de saída
    (/bin/Debug ou /bin/Release):

    -   logo.png
    -   favicon.ico
    -   funcionarios.json

5.  Execute o projeto: F5

------------------------------------------------------------------------

### 🖥️ Para Usuários (Instalação)

O sistema disponibiliza um instalador `.msi` que:

-   Instala automaticamente as dependências do .NET 6
-   Cria atalhos personalizados (Desktop e Menu Iniciar)
-   Aplica o ícone oficial da aplicação

------------------------------------------------------------------------

## 🔐 Compliance e LGPD

O projeto foi desenvolvido seguindo princípios de **Privacy by Design**,
alinhado à **LGPD (Lei nº 13.709/2018)**:

-   🔒 **Tratamento de Dados**\
    Armazenamento local, sem envio automático para serviços externos

-   🧾 **Auditoria e Rastreabilidade**\
    Cada retirada gera um timestamp imutável

-   🧪 **Dados de Teste**\
    A empresa e arquivo funcionarios.json contém apenas dados fictícios para
    demonstração

------------------------------------------------------------------------

## 🛠️ Tecnologias Utilizadas

-   C# (.NET 6)
-   Windows Forms / Desktop UI
-   JSON (persistência de dados)
-   CSV (exportação de relatórios)

------------------------------------------------------------------------

## 👨‍💻 Autor

**Kleberson Pastori**\
Software Engineering Student @ Estácio\


Este projeto faz parte do meu portfólio profissional, com foco em
desenvolvimento em C#, lógica de negócios, UX/UI e deploy de software.
