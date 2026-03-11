import pyautogui
import time

pyautogui.PAUSE = 1.2
time.sleep(5)

pyautogui.press("win")
pyautogui.write("firefox")
time.sleep(3)
pyautogui.press("enter")
time.sleep(3)
pyautogui.click(x=419, y=60)
pyautogui.write("https://dlp.hashtagtreinamentos.com/python/intensivao/login")
pyautogui.press("enter")

time.sleep(5)

pyautogui.click(x=724, y=375)
pyautogui.write("kleber-pastori@hotmail.com")
pyautogui.press("tab")
pyautogui.write("senhatop12345")
pyautogui.click(x=964, y=536)
time.sleep(3)

import pandas as pd

tabela = pd.read_csv("produtos.csv")
print(tabela)

for linha in tabela.index:
    pyautogui.click(713, y=256)
    codigo = tabela.loc[linha, "codigo"]

    pyautogui.write(str(codigo))
    pyautogui.press("tab")
    pyautogui.write(str(tabela.loc[linha, "marca"]))
    pyautogui.press("tab")
    pyautogui.write(str(tabela.loc[linha, "tipo"]))
    pyautogui.press("tab")
    pyautogui.write(str(tabela.loc[linha, "categoria"]))
    pyautogui.press("tab")
    pyautogui.write(str(tabela.loc[linha, "preco_unitario"]))
    pyautogui.press("tab")
    pyautogui.write(str(tabela.loc[linha, "custo"]))
    pyautogui.press("tab")

    obs = tabela.loc[linha, "obs"]
    if not pd.isna(obs):
        pyautogui.write(str(tabela.loc[linha, "obs"]))

    pyautogui.press("tab")
    pyautogui.press("enter")
    pyautogui.scroll(5000)

