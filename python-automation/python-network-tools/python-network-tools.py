# -*- coding: utf-8 -*-
"""
AutoEver - Ferramentas de Rede
Autor: Kleberson Pastori
"""

import os
import re
import sys
from datetime import datetime

from PySide6.QtCore import Qt, QProcess
from PySide6.QtGui import QTextCursor, QFont, QColor
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QPushButton, QTextEdit, QLabel, QMessageBox, QStatusBar
)

IS_WINDOWS = os.name == 'nt'
DIVISOR_LEN = 80  # tamanho da linha divisória

def agora():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def validar_ip(ip: str) -> bool:
    """Valida formato IPv4 e faixa 0..255."""
    padrao = r'^(?:\d{1,3}\.){3}\d{1,3}$'
    if not re.match(padrao, ip):
        return False
    try:
        return all(0 <= int(x) <= 255 for x in ip.split('.'))
    except ValueError:
        return False

def validar_porta(porta: str) -> bool:
    return porta.isdigit() and 1 <= int(porta) <= 65535

class NetworkGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Comandos de Rede - AutoeEver")
        self.resize(900, 560)

        # Status bar
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("Pronto")

        # Processo
        self.proc = QProcess(self)
        self.proc.readyReadStandardOutput.connect(self.on_stdout)
        self.proc.readyReadStandardError.connect(self.on_stderr)
        self.proc.finished.connect(self.on_finished)
        self.proc.errorOccurred.connect(self.on_error)

        # --- Área central ---
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        # Cabeçalho
        header = QLabel("Console de comandos de rede")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(header)

        # Formulário
        form = QFormLayout()
        self.input_ip = QLineEdit(); self.input_ip.setPlaceholderText("Ex.: 8.8.8.8")
        self.input_dom = QLineEdit(); self.input_dom.setPlaceholderText("Ex.: google.com")
        self.input_porta = QLineEdit(); self.input_porta.setPlaceholderText("Ex.: 443")
        form.addRow("IP:", self.input_ip)
        form.addRow("Domínio:", self.input_dom)
        form.addRow("Porta:", self.input_porta)
        main_layout.addLayout(form)

        # Botões (linha 1)
        btns_1 = QHBoxLayout()
        self.btn_ping = QPushButton("PING")
        self.btn_ipconfig = QPushButton("IPCONFIG /ALL")
        self.btn_hostname = QPushButton("HOSTNAME")
        self.btn_tracert = QPushButton("TRACERT")
        self.btn_telnet = QPushButton("TELNET (Test-NetConnection)")
        self.btn_nslookup = QPushButton("NSLOOKUP")
        for b in (self.btn_ping, self.btn_ipconfig, self.btn_hostname,
                  self.btn_tracert, self.btn_telnet, self.btn_nslookup):
            btns_1.addWidget(b)
        main_layout.addLayout(btns_1)

        # Botões (linha 2)
        btns_2 = QHBoxLayout()
        self.btn_netstat = QPushButton("NETSTAT -AN")
        self.btn_arp = QPushButton("ARP -A")
        self.btn_route = QPushButton("ROUTE PRINT")
        self.btn_gpresult = QPushButton("GPRESULT /R")
        self.btn_cmd = QPushButton("Abrir CMD")
        self.btn_rdp = QPushButton("Abrir conexão RDP")
        for b in (self.btn_netstat, self.btn_arp, self.btn_route,
                  self.btn_gpresult, self.btn_cmd, self.btn_rdp):
            btns_2.addWidget(b)
        main_layout.addLayout(btns_2)

        # Console (texto simples)
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setPlaceholderText("Saída dos comandos aparecerá aqui")
        font = QFont()
        font.setPointSize(11)  # tamanho da fonte
        # font.setFamily("Consolas")  # opcional: monoespaçada
        self.console.setFont(font)
        main_layout.addWidget(self.console)

        # Ações secundárias
        secondary = QHBoxLayout()
        self.btn_limpar = QPushButton("Limpar Console")
        self.btn_about = QPushButton("Sobre")
        self.btn_sair = QPushButton("Sair")
        secondary.addWidget(self.btn_limpar)
        secondary.addWidget(self.btn_about)
        secondary.addStretch()
        secondary.addWidget(self.btn_sair)
        main_layout.addLayout(secondary)

        # Conectar sinais
        self.btn_ping.clicked.connect(self.do_ping)
        self.btn_ipconfig.clicked.connect(self.do_ipconfig)
        self.btn_hostname.clicked.connect(self.do_hostname)
        self.btn_tracert.clicked.connect(self.do_tracert)
        self.btn_telnet.clicked.connect(self.do_telnet)
        self.btn_nslookup.clicked.connect(self.do_nslookup)
        self.btn_netstat.clicked.connect(self.do_netstat)
        self.btn_arp.clicked.connect(self.do_arp)
        self.btn_route.clicked.connect(self.do_route)
        self.btn_gpresult.clicked.connect(self.do_gpresult)
        self.btn_cmd.clicked.connect(self.do_cmd)
        self.btn_rdp.clicked.connect(self.do_rdp)
        self.btn_limpar.clicked.connect(self.console.clear)
        self.btn_about.clicked.connect(self.show_about)
        self.btn_sair.clicked.connect(self.close)

    # --- Helpers de console ---
    def _divisor_verde(self):
        """Insere uma linha divisória verde usando texto."""
        cursor = self.console.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        # Configura a cor verde no formato do texto
        fmt = cursor.charFormat()
        fmt.setForeground(QColor("#66A266"))  # verde
        # Linha de traços box-drawing (fica bem visível)
        cursor.insertText("─" * DIVISOR_LEN + "\n", fmt)
        self.console.setTextCursor(cursor)

    def log(self, msg: str):
        self.console.append(f"[{agora()}] {msg}")
        self.console.moveCursor(QTextCursor.MoveOperation.End)

    def log_err(self, msg: str):
        self.console.append(f"[{agora()}] ERRO: {msg}")
        self.console.moveCursor(QTextCursor.MoveOperation.End)

    def run_cmd(self, cmd: str, interactive=False):
        """Executa comando via cmd.exe /c no Windows."""
        if not IS_WINDOWS:
            QMessageBox.critical(self, "Erro", "Aplicativo preparado para Windows.")
            return
        if self.proc.state() != QProcess.NotRunning:
            self.log_err("Já existe um comando em execução. Aguarde finalizar.")
            return

        # Linha verde separando início (antes de executar)
        self._divisor_verde()

        if interactive:
            self.log(f"Executando (externo): {cmd}")
            QProcess.startDetached("cmd.exe", ["/c", cmd])
            # Linha verde também ao final de abertura externa
            self._divisor_verde()
            return

        self.log(f"$ {cmd}")
        self.status.showMessage(f"Executando: {cmd}")
        self.proc.start("cmd.exe", ["/c", cmd])

    # --- Saída do processo ---
    def on_stdout(self):
        data = self.proc.readAllStandardOutput().data().decode("utf-8", errors="ignore")
        if data:
            self.console.append(data.rstrip())
            self.console.moveCursor(QTextCursor.MoveOperation.End)

    def on_stderr(self):
        data = self.proc.readAllStandardError().data().decode("utf-8", errors="ignore")
        if data:
            for line in data.splitlines():
                self.console.append(f"STDERR: {line}")
            self.console.moveCursor(QTextCursor.MoveOperation.End)

    def on_finished(self, code, status):
        self.status.showMessage(f"Finalizado (código={code}, status={status}).")
        self.log(f"Comando finalizado com código {code}")
        # Linha verde separando fim
        self._divisor_verde()

    def on_error(self, error):
        self.log_err(f"Erro ao iniciar processo: {error}")
        self.status.showMessage("Erro ao iniciar processo.")
        # Linha verde mesmo em erro
        self._divisor_verde()

    # --- Ações ---
    def do_ping(self):
        alvo = self.input_dom.text().strip() or self.input_ip.text().strip()
        if not alvo:
            QMessageBox.warning(self, "Atenção", "Informe um IP ou domínio.")
            return
        if validar_ip(alvo) or "." in alvo:
            self.run_cmd(f"ping {alvo}")
        else:
            QMessageBox.warning(self, "Atenção", "IP/Domínio inválido.")

    def do_ipconfig(self):
        self.run_cmd("ipconfig /all")

    def do_hostname(self):
        ip = self.input_ip.text().strip()
        if not ip:
            self.run_cmd("hostname")
            return
        if validar_ip(ip) or "." in ip:
            self.run_cmd(f"ping -a {ip}")
        else:
            QMessageBox.warning(self, "Atenção", "IP inválido.")

    def do_tracert(self):
        destino = self.input_dom.text().strip() or self.input_ip.text().strip()
        if not destino:
            QMessageBox.warning(self, "Atenção", "Informe um IP ou domínio.")
            return
        if validar_ip(destino) or "." in destino:
            self.run_cmd(f"tracert {destino}")
        else:
            QMessageBox.warning(self, "Atenção", "IP/Domínio inválido.")

    def do_telnet(self):
        """Verifica porta usando PowerShell Test-NetConnection (sem precisar do Telnet)."""
        ip = self.input_ip.text().strip()
        porta = self.input_porta.text().strip()
        if not (validar_ip(ip) and validar_porta(porta)):
            QMessageBox.warning(self, "Atenção", "IP ou porta inválidos.")
            return

        ps_cmd = (
            f"powershell -NoProfile -ExecutionPolicy Bypass "
            f"-Command \"Test-NetConnection {ip} -Port {porta} | "
            f"Format-List -Property ComputerName,RemoteAddress,RemotePort,TcpTestSucceeded\""
        )
        self.run_cmd(ps_cmd)

    def do_nslookup(self):
        dominio = self.input_dom.text().strip()
        if not dominio:
            QMessageBox.warning(self, "Atenção", "Informe um domínio.")
            return
        self.run_cmd(f"nslookup {dominio}")

    def do_netstat(self):
        self.run_cmd("netstat -an")

    def do_arp(self):
        self.run_cmd("arp -a")

    def do_route(self):
        self.run_cmd("route print")

    def do_gpresult(self):
        self.run_cmd("gpresult /R")

    def do_cmd(self):
        self.run_cmd("start cmd.exe", interactive=True)

    def do_rdp(self):
        self.run_cmd("start mstsc.exe", interactive=True)

    def show_about(self):
        QMessageBox.information(
            self,
            "Sobre",
            "Automação de rede em Python(PySide6). By Kleberson Pastori 😃 😄 😁 🖥 🖧",
        )

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("AutoEver - Ferramentas de Rede")
    gui = NetworkGUI()
    gui.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

