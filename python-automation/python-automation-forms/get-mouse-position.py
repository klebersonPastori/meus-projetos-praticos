import time
import pyautogui

#pegar posição da tela (mouse)
time.sleep(5)
print(pyautogui.position())

#rolar até o topo
pyautogui.scroll(2000)