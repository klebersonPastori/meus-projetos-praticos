#!/bin/bash
clear

# Define as cores
CYAN='\033[1;36m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
NC='\033[0m' 

echo -e "${CYAN}"
echo " ╔════════════════════════════════════════════════════╗"
echo " ║                                                    ║"
echo " ║        [!] INICIANDO AUTOMAÇÃO DE AMBIENTE         ║"
echo " ║                                                    ║"
echo " ╚════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Verifica se o usuário é root (EUID 0)
if [ "$EUID" -ne 0 ]; then
  echo -e "${YELLOW}[!] Por favor, execute este script como root (ex: sudo $0)${NC}"
  exit 1
fi

echo -e "${YELLOW}[*] Checando permissões e preparando o sistema...${NC}"
sleep 1
echo -e "${GREEN}[+] Tudo pronto. Executando rotina!${NC}"
echo "------------------------------------------------------"
echo ""


echo "Criando Grupos..."

groupadd GRP_ADM
groupadd GRP_VEN
groupadd GRP_SEC

echo "Grupos criados."

echo "Criando Pastas e definindo permissões dos Grupos..."

mkdir /adm
mkdir /ven
mkdir /sec

chown root:GRP_ADM /adm
chown root:GRP_VEN /ven
chown root:GRP_SEC /sec

chmod 770 /adm
chmod 770 /ven
chmod 770 /sec

echo "Permissões dos Grupos definidas."

echo "Criando pasta PÚBLICA..."

mkdir /publica
chmod 777 /publica/

echo "Pasta PÚBLICA criada com permissão total para todos."

echo "Criando Usuarios ADM, definindo grupos, permissões e senhas..."

useradd carlos -c "adm" -s /bin/bash -G GRP_ADM -m -p $(openssl passwd -6 senha123)
useradd maria -c "adm" -s /bin/bash -G GRP_ADM -m -p $(openssl passwd -6 senha123)
useradd joao -c "adm" -s /bin/bash -G GRP_ADM -m -p $(openssl passwd -6 senha123)

echo "Grupo e usuarios ADM criados com sucesso!"

echo "Criando Usuarios VEN, definindo grupos, permissões e senhas..."

useradd debora -c "ven" -s /bin/bash -G GRP_VEN -m -p $(openssl passwd -6 senha123)
useradd sebastiana -c "ven" -s /bin/bash -G GRP_VEN -m -p $(openssl passwd -6 senha123)
useradd roberto -c "ven" -s /bin/bash -G GRP_VEN -m -p $(openssl passwd -6 senha123)

echo "Grupo e usuarios VEN criados com sucesso!"

echo "Criando Usuarios SEC, definindo grupos, permissões e senhas..."

useradd jose -c "sec" -s /bin/bash -G GRP_SEC -m -p $(openssl passwd -6 senha123)
useradd amanda -c "sec" -s /bin/bash -G GRP_SEC -m -p $(openssl passwd -6 senha123)
useradd rogerio -c "sec" -s /bin/bash -G GRP_SEC -m -p $(openssl passwd -6 senha123)

echo "Grupo e usuarios SEC criados com sucesso!"

exit