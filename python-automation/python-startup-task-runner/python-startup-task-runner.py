from time import sleep
import os

print(''*75)
print('####'*20)
print("\033[92m                          Automatizador de Inicialização\033[0m")
print('####'*20)
print(''*75)

def abrirPrograma():
    sleep(1)
    print('Abrindo navegador padrão...')
    print(''*75)
    print("\033[92mOK!\033[0m")
    print(''*75)
    print(''*75)

def abrirPrograma1():
    sleep(3)
    print('Abrindo Outlook...')
    print(''*75)
    print("\033[92mOK!\033[0m")
    print(''*75)
    print(''*75)

def abrirPrograma2():
    sleep(3)
    print('Abrindo Microsoft Teams...')
    print(''*75)
    print("\033[92mOK!\033[0m")
    print(''*75)
    print(''*75)

abrirPrograma()
os.startfile(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")

abrirPrograma1()
os.startfile(r"C:\Program Files\Microsoft Office\root\Office16\OUTLOOK.EXE")

abrirPrograma2()
os.system("start ms-teams:")

print("\033[94m                         Programas abertos com Sucesso!!!\033[0m")
print('####'*20)
print(''*75)
input('Digite qualquer botão para sair')
