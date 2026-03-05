
class Heroi {
    /**
     * @param {string} nome - O nome do herói.
     * @param {number} idade - A idade do herói.
     * @param {string} tipo - O tipo do herói (guerreiro, mago, monge, ninja).
     */
    constructor(nome, idade, tipo) {
        this.nome = nome;
        this.idade = idade;
        this.tipo = tipo;
    }

    atacar() {
        let ataque = "";
        switch (this.tipo) {
            case "mago":
                ataque = "usou magia";
                break;
            case "guerreiro":
                ataque = "usou espada";
                break;
            case "monge":
                ataque = "usou artes marciais";
                break;
            case "ninja":
                ataque = "usou shuriken";
                break;
            default:
                ataque = "usou um ataque indefinido";
        }

        
        console.log(`o ${this.tipo} atacou usando ${ataque}`);
    }
}
//instâncias (objetos) da classe Heroi
const heroiMago = new Heroi("Gandalf", 150, "mago");
const heroiGuerreiro = new Heroi("Aragorn", 35, "guerreiro");
const heroiMonge = new Heroi("Lee", 28, "monge");
const heroiNinja = new Heroi("Hanzo", 30, "ninja");

heroiMago.atacar();
heroiGuerreiro.atacar();
heroiMonge.atacar();
heroiNinja.atacar();