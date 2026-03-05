import os
import pyfiglet
import shutil
import time

# Nome do programa em ASCII + COR
cols = shutil.get_terminal_size().columns
texto = pyfiglet.figlet_format("Verificador de arquivos potencialmente maliciosos", font="mini")
vermelho = "\033[33m"  # (na verdade é amarelo - 33)
reset = "\033[0m"

for linha in texto.splitlines():
    print((vermelho + linha + reset).center(cols))

# Extensões que potencialmente podem ser perigosas
EXT_SUSPEITAS = {".exe", ".bat", ".ps1", ".vbs", ".dll", ".cmd"}  # set para busca mais rápida

# Pastas com caminho padrão a serem analisadas (trocar)
PASTA  = r"C:\Users\Downloads"
PASTA1 = r"C:\Users\Documents"
PASTA2 = r"C:\Users\Desktop"

# Função para varrer recursivamente e listar suspeitos
def listar_suspeitos_recursivo(pasta, rotulo):
    encontrados = 0

    if not os.path.exists(pasta):
        print(f"\033[33m[AVISO] Pasta não encontrada: {pasta}\033[0m")
        return 0

    try:
        for raiz, _, arquivos in os.walk(pasta):
            for arquivo in arquivos:
                ext = os.path.splitext(arquivo)[1].lower()
                if ext in EXT_SUSPEITAS:
                    caminho_rel = os.path.relpath(os.path.join(raiz, arquivo), pasta)
                    print(f"\033[31m⚠️ Arquivo(s) potencialmente perigoso encontrado em '{rotulo}': {caminho_rel}\033[0m")
                    encontrados += 1
    except PermissionError:
        print(f"\033[33m[AVISO] Sem permissão para ler: {pasta}\033[0m")

    return encontrados

print("\n")
print(f"🔍 Verificando arquivos suspeitos em: {PASTA}")
print(f"🔍 Verificando arquivos suspeitos em: {PASTA1}")
print(f"🔍 Verificando arquivos suspeitos em: {PASTA2}")
print("_" * 110)
time.sleep(4)

# Varredura recursiva nas três pastas
total = 0
total += listar_suspeitos_recursivo(PASTA,  "DOWNLOADS")
total += listar_suspeitos_recursivo(PASTA1, "DOCUMENTS")
total += listar_suspeitos_recursivo(PASTA2, "DESKTOP")

print("_" * 110)

# Mensagem final
if total == 0:
    print("\n\033[32m✅ Nenhum arquivo suspeito foi encontrado!\033[0m\n")
else:
    print(f"\n\033[33mResumo: {total} arquivo(s) potencialmente perigoso(s) encontrado(s).\033[0m\n")

print("By Kleberson Pastori")
input("Aperte ENTER para sair...")