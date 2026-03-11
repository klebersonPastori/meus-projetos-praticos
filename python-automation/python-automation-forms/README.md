# 🤖 Automação de Cadastro de Produtos

Projeto de automação com **Python + PyAutoGUI** para preencher formulários web automaticamente a partir de uma planilha CSV.

---

## 📁 Arquivos

| Arquivo | Descrição |
|---|---|
| `python-automation-forms.py` | Script principal — lê o CSV e preenche o formulário |
| `produtos.csv` | Base de dados com os produtos a cadastrar |
| `get-mouse-position.py` | Utilitário para capturar coordenadas do mouse na tela |

---

## ⚙️ Requisitos

- Python 3.x
- Bibliotecas:

```bash
pip install pyautogui pandas
```

---

## ▶️ Como usar

1. **Descubra as coordenadas certas** rodando `get-mouse-position.py` e posicionando o mouse nos campos do formulário.

2. **Ajuste as coordenadas** no script principal se necessário (variáveis `x` e `y` nos `pyautogui.click()`).

3. **Execute o script principal:**

```bash
python python-automation-forms.py
```

> O script abre o Firefox, acessa o sistema de login, autentica e preenche o formulário para cada produto do CSV.

---

## 📋 Estrutura do CSV

```
codigo, marca, tipo, categoria, preco_unitario, custo, obs
```

A coluna `obs` é opcional — o script ignora se estiver vazia.

---

## ⚠️ Observações

- Mantenha o `produtos.csv` na mesma pasta do script.
- Não mova o mouse durante a execução.
- O script aguarda 5 segundos antes de iniciar — use esse tempo para deixar a janela em foco.
