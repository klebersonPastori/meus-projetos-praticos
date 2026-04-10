#!/bin/bash

clear

#banner em ASCII Art
cat << "EOF"
    ____             __  ____             
   / __ \___ _   __ / / / __ \____  _____ 
  / / / / _ \ | / // / / / / / __ \/ ___/ 
 / /_/ /  __/ |/ // / / /_/ / /_/ (__  )  
/_____/\___/|___//_/  \____/ .___/____/   
                          /_/

        [ MySQL Automated Setup ]          
===========================================
EOF

echo ""
echo "Iniciando instalador do banco de dados MySQL..."
echo ""

# 1. Verificando se o usuário é root
if [ "$EUID" -ne 0 ]; then
  echo "[-] Permissão negada. Por favor, execute este script como root (ex: sudo ./seu_script.sh)"
  exit 1
else
  echo "[+] Root detectado. Prosseguindo..."
fi

# 2. Comando de instalação
echo "[+] Baixando e instalando pacotes..."
apt install mysql-client-core -y

echo "[+] MySQL instalado com êxito."
echo "[+] Iniciando automação para cadastrar usuários..."

# 3. Injetando os comandos SQL direto no MySQL
mysql -u root <<EOF
CREATE DATABASE IF NOT EXISTS login;

USE login;

CREATE TABLE IF NOT EXISTS Login (
    id_usuario INT, 
    Nome VARCHAR(50), 
    Sobrenome VARCHAR(50), 
    Email VARCHAR(50), 
    Senha VARCHAR(20)
);

INSERT INTO Login (id_usuario, Nome, Sobrenome, Email, Senha) 
VALUES (1, 'Kleberson', 'Pastori', 'kleber-pastori@hotmail.com', 'senha1234');

SHOW TABLES;
SELECT * FROM Login;
EOF

echo ""
echo "==========================================="
echo "[✔] Automação finalizada com sucesso!"