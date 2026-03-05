import os
import sys
import pyfiglet

#Título em ASCII através da biblioteca importada
title = pyfiglet.figlet_format("Calculadora simples em Python", font="small")
print(title)
        
#creditos do criador
print("\033[36mBY Kleberson pastori\033[0m\n")

# Funções para "segurar" o programa
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

#Operações aritmeticas básicas
def somar():
    try:
        num1 = float(input("Insira o primeiro número: "))
        num2 = float(input("Insira o segundo número: "))
        print(f"\033[32mResultado: {num1} + {num2} = {num1 + num2}\033[0m")
        print("-\n"*1)
    except ValueError:
        print("\033[31m❌ Entrada inválida: digite apenas números.\033[0m")
        print("-"*35)
        print(" ")

def subtrair():
    try:
        num1 = float(input("Insira o primeiro número: "))
        num2 = float(input("Insira o segundo número: "))
        print(f"\033[32mResultado: {num1} - {num2} = {num1 - num2}\033[0m")
        print("-\n"*1)
    except ValueError:
        print("\033[31m❌ Entrada inválida: digite apenas números.\033[0m")
        print("-"*35)
        print(" ")

def multiplicar():
    try:
        num1 = float(input("Insira o primeiro número: "))
        num2 = float(input("Insira o segundo número: "))
        print(f"\033[32mResultado: {num1} * {num2} = {num1 * num2}\033[0m")
        print("-\n"*1)
    except ValueError:
        print("\033[31m❌ Entrada inválida: digite apenas números.\033[0m")
        print("-"*35)
        print(" ")

def dividir():
    try:
        num1 = float(input("Insira o primeiro número: "))
        num2 = float(input("Insira o segundo número: "))
        if num2 == 0:
            print("\033[31mNão é possível dividir por zero.\033[0m")
            print(" "*35)
            print(" ")
        else:
            print(f"\033[32mResultado: {num1} / {num2} = {num1 / num2}\033[0m")
            print("-\n"*1)
    except ValueError:
        print("\033[31m❌ Entrada inválida: digite apenas números.\033[0m")
        print("-"*35)
        print(" ")

#- Menu principal -
def menu():
    while True:
        
        print("1) ➕ Somar")
        print("2) ➖ Subtrair")
        print("3) ✖️ Multiplicar")
        print("4) ➗ Dividir")
        print("5) 🧹 Limpar console")
        print("0) ❌ para Sair➡️")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            somar()
            
        elif opcao == "2":
            subtrair()
            
        elif opcao == "3":
            multiplicar()
            
        elif opcao == "4":
            dividir()
            
        elif opcao == "0":
            print("\033[32mSaindo... até mais!\033[0m")
            break
        elif opcao == "5":
            limpar_tela ()
        else:
            print("\033[31m❌ Opção inválida! Tente novamente.\033[0m")
            print("-"*35)
            print(" ")
            
#chama a função na raiz para o menu
if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\n\033[36mEncerrado pelo usuário❕\033[0m")
        sys.exit(0)