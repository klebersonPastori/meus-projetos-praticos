# 🎯 Attack: Factory Strike - Local

Um mini-jogo de tiro em primeira pessoa (FPS) no estilo *arcade* e sobrevivência, desenvolvido inteiramente com tecnologias web nativas. O jogador assume o papel de um atirador que precisa se defender de inimigos que surgem aleatoriamente em um cenário industrial, testando seus reflexos, mira e gerenciamento de munição.

## 📝 Sobre o Projeto

O jogo não utiliza motores gráficos tradicionais; em vez disso, ele usa manipulação avançada de DOM e CSS3 para criar uma ilusão de profundidade (pseudo-3D) e JavaScript puro para a lógica do jogo. Destaques da implementação:

* **Imersão e Controles:** A arma acompanha o movimento do mouse na tela (*weapon sway*) e possui animações responsivas de recuo ao atirar e de abaixar ao recarregar. A mira (*crosshair*) e o cursor nativo do mouse são customizados.
* **Sistema de Áudio Inteligente:** O código busca reproduzir arquivos de áudio locais (como os tiros e efeitos especiais de pontuação). Se os arquivos não forem encontrados, o jogo possui um sistema de *fallback* que sintetiza os sons mecanicamente através de código usando a **Web Audio API** (`AudioContext`).
* **Gráficos Híbridos (Fallback):** O cenário e os inimigos são desenhados utilizando CSS puro (formas geométricas, gradientes e sombras). Se a imagem da arma principal não carregar, o jogo aciona automaticamente um desenho vetorial (SVG) da arma para não quebrar a experiência.
* **Mecânicas de Combate:** Cada inimigo surge com uma barra de tempo de reação (5 segundos). Se o jogador não atirar antes do tempo acabar, sofre dano. A dificuldade é dinâmica, aumentando a frequência de surgimento dos inimigos conforme a pontuação sobe.

## 💻 Tecnologias Utilizadas

* **HTML5:** Estruturação da interface, elementos sobrepostos (Overlay) e painel HUD.
* **CSS3:** Variáveis globais (`:root`), animações (`@keyframes`), gradientes e transformações avançadas em 3D (`perspective`, `rotate`, `translate`, `skewX`) para dar profundidade aos elementos bidimensionais.
* **JavaScript (Vanilla):** Controle de estados (vida, balas, pontuação), *loop* do jogo otimizado com `requestAnimationFrame`, geração de inimigos com cálculo de escala e profundidade (Z-index baseada na posição Y), e mapeamento de eventos do mouse.

## 🛠️ Como Jogar

Como o projeto é totalmente *Front-end*, é muito fácil de testar na sua própria máquina:

1. Clone ou baixe os arquivos deste repositório.
2. **Importante:** Para a experiência completa, o ideal é ter as pastas `imgs/` (com `bg.jpg` e `arma.png`) e `audio/` (com `oi.mp3`, `mk.mp3` e `som.mp3`) no mesmo diretório do arquivo principal. Caso não as tenha, o jogo ainda funcionará perfeitamente utilizando os recursos visuais e sonoros gerados por código (*fallbacks*)!
3. Abra o arquivo `game.html` no seu navegador de internet preferido.
4. **Comandos:**
   * **Mover o Mouse:** Controla a mira na tela.
   * **Clique com o Botão Esquerdo:** Atira.
   * **Clique com o Botão Direito:** Recarrega a arma (12 projéteis).

---
*Desenvolvido por Kleberson Pastori* 🔫