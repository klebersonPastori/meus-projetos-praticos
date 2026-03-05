# 🛡️ Portfólio Profissional: Cibersegurança & Nuvem ☁️

Este repositório contém o código-fonte do meu portfólio interativo de apresentação profissional. Desenvolvido no formato *Single Page Application* (SPA), o site tem como objetivo centralizar minhas experiências, projetos e habilidades técnicas como Estagiário de Cibersegurança (com foco em Segurança em Nuvem, Automação com Python e DevSecOps).

## 🚀 Destaques e Funcionalidades

* 🌐 **Sistema Bilíngue Dinâmico:** Um seletor de idiomas (Inglês / Português) controlado por JavaScript que altera todo o conteúdo da página instantaneamente, sem necessidade de recarregamento. O conteúdo é gerenciado através de atributos personalizados de dados (`data-en` e `data-pt`).
* 🎨 **Design Moderno (Glassmorphism):** Interface construída com o tema escuro (*Dark Mode*), utilizando fundos translúcidos (`backdrop-filter: blur`), bordas suaves e acentos de cores vibrantes (neon/cyan) que remetem ao universo da tecnologia e segurança.
* ✨ **Experiência de Usuário (UI/UX):** * **Barra de Progresso:** Um indicador fixo no topo da tela que acompanha a rolagem da página (scroll).
  * **Scroll-Reveal:** Animações suaves em que as seções de experiência e projetos aparecem gradualmente (*fade-in* e *slide-up*) à medida que o usuário desce a página.
* 📱 **Totalmente Responsivo:** O layout (baseado em Flexbox) adapta-se perfeitamente a qualquer tamanho de tela, garantindo legibilidade tanto em monitores ultrawide quanto em smartphones.
* 🔗 **Acesso Rápido e Contato:** Integração de botões para download direto do Currículo em PDF, links para as aplicações hospedadas na AWS S3 (jogos de navegador) e um botão flutuante (*FAB - Floating Action Button*) para contato direto via WhatsApp.

## 💻 Tecnologias Utilizadas

* **HTML5:** Estrutura semântica e atributos customizados de dados (`data-attributes`) para o controle de tradução.
* **CSS3:** Variáveis globais (`:root`), efeitos de *glassmorphism*, gradientes radiais para o fundo, animações de transição e *media queries* para responsividade.
* **JavaScript (Vanilla):** * Lógica de cálculo matemático do *scroll* para a barra de progresso.
  * *Event Listeners* (`window.addEventListener`) para detectar a posição dos elementos e engatilhar as animações de *reveal*.
  * Lógica de substituição de conteúdo no DOM para a troca de idiomas.
* **Recursos Externos:** Fontes do *Google Fonts* (Poppins) e ícones do *FontAwesome*.

## 🛠️ Como visualizar

Como o site foi construído inteiramente no *Front-end* (sem uso de frameworks pesados ou pré-processadores), a visualização é direta:

1. Clone ou faça o download deste repositório.
2. Certifique-se de ter o arquivo do seu currículo na pasta `assets/CV_Kleberson.pdf` e a sua foto de perfil em `assets/img/foto.png`.
3. Abra o arquivo `index.html` em qualquer navegador web moderno.

---
*Desenvolvido por Kleberson Pastori* 🔐