//Criando projeto DIO-Hroi nivel de experiencia

let nomeDoHeroi = "Madara"
let nivelDeXp = 8888
let nivel;

if (nivelDeXp <= 1000) {
    nivel = "Ferro";
} else if (nivelDeXp >= 1001 && nivelDeXp <=2000){
    nivel="Bronze"
} else if (nivelDeXp >= 2001 && nivelDeXp <=5000){
    nivel="Prata"
} else if (nivelDeXp >= 5001 && nivelDeXp <=7000){
    nivel="Ouro"
} else if (nivelDeXp >= 7001 && nivelDeXp <=8000){
    nivel="Platina"
} else if (nivelDeXp >= 8001 && nivelDeXp <=9000){
    nivel="Ascendente"
} else if (nivelDeXp >= 9001 && nivelDeXp <=10000){
    nivel="Imortal"
} else {// se for maior que 10000
    nivel="Radiante"
}
console.log ("O Heroi de nome " + nomeDoHeroi , "está no nível de " + nivel);