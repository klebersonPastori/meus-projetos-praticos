# 🏃‍♂️ HAWKINS RUNNER — 8bit Game 🧇

Um mini-jogo de navegador no estilo *endless runner* (corrida infinita) inspirado no sombrio universo de **Stranger Things**. O objetivo é fugir dos monstros do Mundo Invertido, pulando obstáculos e sobrevivendo o maior tempo possível para escapar do Vecna e alcançar a pontuação máxima!

## 📝 Estrutura do Projeto

O jogo foi construído inteiramente com tecnologias web nativas (Vanilla), sem o uso de bibliotecas externas ou *engines* de jogos prontas. Ele é dividido em três arquivos principais:

* **👾 Marcação e Elementos (`index.html`):** Define a estrutura do jogo, incluindo o HUD (pontuação e dicas), as telas modais (Instruções e Game Over), a integração de trilha sonora em 8-bits (`<audio>`) e a renderização do personagem principal, que foi desenhado diretamente via código usando um `<svg>` vetorial.
* **🎨 Imersão Visual (`styles.css`):** Responsável por toda a identidade estética do jogo. O grande destaque é a atmosfera do "Mundo Invertido", criada através de variáveis CSS e animações complexas (`@keyframes`) que geram partículas de cinzas caindo na tela e efeitos visuais imersivos de relâmpagos (utilizando SVG dinâmico e `mix-blend-mode`).
* **⚙️ Motor e Física (`game.js`):** O "cérebro" da aplicação. Ele gerencia o *loop* do jogo utilizando `requestAnimationFrame`, calcula a física do pulo do personagem (gravidade vs. força de pulo), processa a detecção matemática de colisões (hitbox) e injeta inimigos aleatórios. Além disso, possui um sistema de **dificuldade dinâmica** que acelera o surgimento de monstros à medida que o tempo passa.

## 💻 Tecnologias Utilizadas

* **HTML5:** Semântica estrutural, gráficos vetoriais SVG e tags multimídia.
* **CSS3:** *Grid/Flexbox*, estilização *pixel-art*, pseudo-elementos e animações em loop.
* **JavaScript (ES6+):** Manipulação de DOM avançada, cálculos matemáticos dinâmicos, controle de áudio e mapeamento de eventos (teclado, clique e toque).

## 🎮 Como Jogar

Como o projeto é totalmente *Front-end*, não há necessidade de instalar dependências ou rodar servidores locais para testar:

1.  Faça o clone ou o download dos arquivos deste repositório.
2.  Abra o arquivo `index.html` diretamente em qualquer navegador moderno de sua preferência (Chrome, Edge, Firefox).
3.  Clique na tela ou pressione a barra de **ESPAÇO** para iniciar a partida.
4.  Pressione **ESPAÇO** ou dê um **CLIQUE/TOQUE** na tela para pular e desviar dos inimigos.

---
*Desenvolvido por Kleberson Pastori* 🎸