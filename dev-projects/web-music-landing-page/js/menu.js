// Lista nome das músicas
const musicas = [
    "Alive", "Even Flow", "Jeremy", "Porch", 
    "Black", "Deep", "Garden", "Oceans", 
    "Once", "Why Go", "Release"
];

// Seleciona a lista pela classe 
const menu = document.querySelector('.menu-links');

// 1. Cria a parte fixa de cima (Título e Página Inicial)
let conteudoHTML = `
    <li class="menu-title" role="presentation"><i><u>Faixas mais Famosas:</u></i></li>
    <li role="none"><a role="menuitem" href="index.html"><u>Página Inicial</u></a></li>
`;

// 2. Cria as faixas dinamicamente
musicas.forEach((musica, index) => {
    const numeroFaixa = index + 1;
    conteudoHTML += `
    <li role="none"><a role="menuitem" href="faixa${numeroFaixa}.html">Ouvir ${musica}</a></li>`;
});

// 3. Adiciona o link do "Sobre o site" no final
conteudoHTML += `
    <li role="none"><a role="menuitem" href="about.html">Sobre o site</a></li>
`;

// 4. Injeta tudo de uma vez dentro da tag <ul> no HTML
menu.innerHTML = conteudoHTML;