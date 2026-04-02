# -*- coding: utf-8 -*-
"""
Ferramentas de Rede
Autor: Kleberson Pastori
"""

import os
import re
import sys
from datetime import datetime
from typing import Optional

from PySide6.QtCore import Qt, QProcess
from PySide6.QtGui import QTextCursor, QColor, QIcon
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLineEdit, QPushButton, QTextEdit, QLabel, QMessageBox, QStatusBar, QFrame
)

# --- Constantes e Estilos ---
APP_TITLE   = "Ferramentas de Rede"
APP_VERSION = "2.5"
IS_WINDOWS  = os.name == "nt"

ACCENT, ACCENT_DARK = "#2563EB", "#1D4ED8"
RED, GREEN = "#DC2626", "#16A34A"
GRAY_100, GRAY_200, GRAY_400, GRAY_700, GRAY_900 = "#F3F4F6", "#E5E7EB", "#9CA3AF", "#374151", "#111827"
WHITE = "#FFFFFF"

STYLESHEET = f"""
QMainWindow, QWidget {{ background-color: {WHITE}; color: {GRAY_900}; font-family: 'Segoe UI', sans-serif; font-size: 13px; }}
QLineEdit {{ background-color: {WHITE}; border: 1.5px solid {GRAY_200}; border-radius: 8px; padding: 7px 12px; }}
QLineEdit:focus {{ border-color: {ACCENT}; }}
QLabel {{ color: {GRAY_700}; font-size: 12px; font-weight: 600; }}

/* Título Centralizado e Azul */
QLabel#app-title {{ 
    font-size: 26px; 
    font-weight: 800; 
    color: {ACCENT}; 
    letter-spacing: -1px;
}}
QLabel#app-subtitle {{ 
    font-size: 13px; 
    font-weight: 400; 
    color: {GRAY_400}; 
}}

QPushButton {{ background-color: {GRAY_100}; color: {GRAY_700}; border: 1.5px solid {GRAY_200}; border-radius: 8px; padding: 8px 14px; font-weight: 600; }}
QPushButton:hover {{ background-color: {ACCENT}; color: {WHITE}; border-color: {ACCENT}; }}

/* Botões Específicos */
QPushButton#btn-exit {{ color: {RED}; }}
QPushButton#btn-exit:hover {{ background-color: {RED}; color: {WHITE}; }}
QPushButton#btn-stop {{ color: {WHITE}; background-color: {RED}; border-color: {RED}; }}
QPushButton#btn-stop:hover {{ background-color: "#B91C1C"; }}

QTextEdit {{ background-color: {GRAY_100}; border: 1.5px solid {GRAY_200}; border-radius: 10px; padding: 10px; font-family: 'Consolas'; font-size: 12px; }}
QStatusBar {{ background-color: {GRAY_100}; color: {GRAY_400}; font-size: 11px; border-top: 1px solid {GRAY_200}; }}
"""

def timestamp() -> str: return datetime.now().strftime("%H:%M:%S")

def validate_ip(ip: str) -> bool:
    if not re.fullmatch(r"(\d{1,3}\.){3}\d{1,3}", ip): return False
    return all(0 <= int(o) <= 255 for o in ip.split("."))

def validate_port(port: str) -> bool: return port.isdigit() and 1 <= int(port) <= 65535

class FieldRow(QWidget):
    def __init__(self, label: str, placeholder: str):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        lbl = QLabel(label); lbl.setFixedWidth(60)
        lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.edit = QLineEdit(); self.edit.setPlaceholderText(placeholder)
        layout.addWidget(lbl); layout.addWidget(self.edit)

class NetworkGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_TITLE)
        
        # Ícone da janela principal
        icon_path = os.path.join(os.path.dirname(__file__), "EthernetCable_icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        self.setMinimumSize(960, 700)
        self.setStyleSheet(STYLESHEET)

        self._proc = QProcess(self)
        self._proc.readyReadStandardOutput.connect(self._on_stdout)
        self._proc.finished.connect(self._on_finished)

        root = QWidget()
        self.setCentralWidget(root)
        outer = QVBoxLayout(root)
        outer.setContentsMargins(24, 20, 24, 16)
        outer.setSpacing(15)

        # Header Centralizado em Azul
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        title = QLabel(APP_TITLE); title.setObjectName("app-title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle = QLabel(f"Infra & Security  ·  v{APP_VERSION}  ·  by Kleberson Pastori")
        subtitle.setObjectName("app-subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        outer.addWidget(header_widget)

        # Inputs
        row_f = QHBoxLayout()
        self._f_ip = FieldRow("IP", "Ex: 192.168.1.1")
        self._f_dom = FieldRow("Domínio", "Ex: google.com")
        self._f_port = FieldRow("Porta", "Ex: 443")
        row_f.addWidget(self._f_ip); row_f.addWidget(self._f_dom); row_f.addWidget(self._f_port)
        outer.addLayout(row_f)

        outer.addWidget(self._line())

        # Grade de Comandos (Simples para Complexos)
        grid = QGridLayout(); grid.setSpacing(8)
        commands = [
            ("HOSTNAME", self._do_hostname), ("IPCONFIG /ALL", self._do_ipconfig),
            ("ROUTE PRINT", self._do_route), ("NETSTAT -AN", self._do_netstat),
            ("ARP -A", self._do_arp), ("GPRESULT /R", self._do_gpresult),
            ("PING", self._do_ping), ("NSLOOKUP", self._do_nslookup),
            ("TRACERT", self._do_tracert), ("REVERSE DNS (IP)", self._do_reverse_dns),
            ("TEST-PORTA (PS)", self._do_telnet), ("CONEXÃO RDP", self._do_rdp),
            ("ABRIR CMD", self._do_cmd)
        ]

        for i, (label, slot) in enumerate(commands):
            btn = QPushButton(label); btn.clicked.connect(slot)
            btn.setMinimumHeight(38)
            grid.addWidget(btn, i // 5, i % 5)
        
        outer.addLayout(grid)
        outer.addWidget(self._line())
        
        self._console = QTextEdit(); self._console.setReadOnly(True)
        outer.addWidget(self._console, stretch=1)

        # Footer
        footer = QHBoxLayout()
        
        # Botões da esquerda
        btn_stop = QPushButton("PARAR")
        btn_stop.setObjectName("btn-stop")
        btn_stop.setMinimumWidth(120)
        btn_stop.clicked.connect(self._stop_process)
        
        btn_clear = QPushButton("Limpar Console")
        btn_clear.clicked.connect(self._console.clear)
        
        # Botão da direita
        btn_exit = QPushButton("Sair")
        btn_exit.setObjectName("btn-exit")
        btn_exit.clicked.connect(self.close)

        footer.addWidget(btn_stop)
        footer.addWidget(btn_clear)
        footer.addStretch()
        footer.addWidget(btn_exit)
        outer.addLayout(footer)

    def _line(self):
        l = QFrame(); l.setFrameShape(QFrame.Shape.HLine); l.setFrameShadow(QFrame.Shadow.Sunken)
        return l

    def _log(self, msg, color=GRAY_900):
        cursor = self._console.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        fmt = cursor.charFormat(); fmt.setForeground(QColor(color))
        cursor.insertText(f"[{timestamp()}] {msg}\n", fmt)
        self._console.moveCursor(QTextCursor.MoveOperation.End)

    def _run(self, cmd, detached=False):
        if not IS_WINDOWS: return
        if self._proc.state() == QProcess.ProcessState.Running:
            self._log("AVISO: Comando em execução. Clique em PARAR antes.", RED)
            return
        self._log(f"─" * 60, GREEN)
        self._log(f"$ {cmd}", ACCENT)
        if detached: QProcess.startDetached("cmd.exe", ["/c", cmd])
        else: self._proc.start("cmd.exe", ["/c", cmd])

    def _on_stdout(self):
        data = self._proc.readAllStandardOutput().data().decode("cp850", errors="replace")
        self._console.insertPlainText(data)
        self._console.moveCursor(QTextCursor.MoveOperation.End)

    def _on_finished(self, code):
        self._log(f"Processo finalizado (Código: {code})", GRAY_400)

    def _stop_process(self):
        """Encerra o comando atual e toda a sua árvore de processos."""
        if self._proc.state() == QProcess.ProcessState.Running:
            pid = self._proc.processId()
            # Encerra o cmd e os filhos (tracert, ping, etc)
            os.system(f"taskkill /F /T /PID {pid}")
            self._proc.terminate()
            self._log("!! COMANDO INTERROMPIDO PELO USUÁRIO !!", RED)
        else:
            self._log("Nenhum processo ativo para parar.", GRAY_400)

    # Ações
    def _do_hostname(self): self._run("hostname")
    def _do_ipconfig(self): self._run("ipconfig /all")
    def _do_route(self): self._run("route print")
    def _do_netstat(self): self._run("netstat -an")
    def _do_arp(self): self._run("arp -a")
    def _do_gpresult(self): self._run("gpresult /R")
    
    def _do_ping(self):
        alvo = self._f_dom.edit.text().strip() or self._f_ip.edit.text().strip()
        if alvo: self._run(f"ping {alvo}")
        else: QMessageBox.warning(self, "Erro", "Informe IP ou Domínio")

    def _do_nslookup(self):
        dom = self._f_dom.edit.text().strip()
        if dom: self._run(f"nslookup {dom}")
        else: QMessageBox.warning(self, "Erro", "Informe um Domínio")

    def _do_tracert(self):
        alvo = self._f_dom.edit.text().strip() or self._f_ip.edit.text().strip()
        if alvo: self._run(f"tracert {alvo}")
        else: QMessageBox.warning(self, "Erro", "Informe IP ou Domínio")

    def _do_reverse_dns(self):
        ip = self._f_ip.edit.text().strip()
        if validate_ip(ip): self._run(f"ping -a {ip}")
        else: QMessageBox.warning(self, "Erro", "Informe um IP válido")

    def _do_telnet(self):
        ip, port = self._f_ip.edit.text().strip(), self._f_port.edit.text().strip()
        if validate_ip(ip) and validate_port(port):
            self._run(f'powershell "Test-NetConnection {ip} -Port {port}"')
        else: QMessageBox.warning(self, "Erro", "IP e Porta necessários")

    def _do_rdp(self): self._run("start mstsc.exe", True)
    def _do_cmd(self): self._run("start cmd.exe", True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = NetworkGUI()
    win.show()
    sys.exit(app.exec())