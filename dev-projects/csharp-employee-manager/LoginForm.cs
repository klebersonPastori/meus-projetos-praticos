using System;
using System.Drawing;
using System.Windows.Forms;
using System.IO;

namespace Nexus_1._0
{
    public class LoginForm : Form
    {
        private TextBox txtSenha = default!;
        private Button btnEntrar = default!;
        private Button btnCancelar = default!;
        private Label lblTitulo = default!;
        private Label lblSenha = default!;

        private const string SENHA_ADMIN = "admin123";

        public LoginForm()
        {
            InitializeComponent();
        }

        private void InitializeComponent()
        {
            this.lblTitulo = new Label();
            this.lblSenha = new Label();
            this.txtSenha = new TextBox();
            this.btnEntrar = new Button();
            this.btnCancelar = new Button();
            this.SuspendLayout();

            // --- Configurações da Janela ---
            this.Text = "NEXUS - Login no Sistema";
            this.ClientSize = new Size(350, 250);
            this.BackColor = Color.FromArgb(30, 30, 35); // Mesmo fundo do Form1
            this.FormBorderStyle = FormBorderStyle.FixedDialog;
            this.MaximizeBox = false;
            this.MinimizeBox = false;
            this.StartPosition = FormStartPosition.CenterParent;
            this.TopMost = true;

            // Ícone da Janela (mesma lógica do principal)
            string iconPath = Path.Combine(Application.StartupPath, "favicon.ico");
            if (File.Exists(iconPath)) this.Icon = new Icon(iconPath);

            // --- lblTitulo ---
            lblTitulo.Text = "LOGIN";
            lblTitulo.Font = new Font("Segoe UI", 14F, FontStyle.Bold);
            lblTitulo.ForeColor = Color.White;
            lblTitulo.Location = new Point(0, 30);
            lblTitulo.Size = new Size(350, 30);
            lblTitulo.TextAlign = ContentAlignment.MiddleCenter;

            // --- lblSenha (Instrução) ---
            lblSenha.Text = "DIGITE A SENHA DE ACESSO:";
            lblSenha.Font = new Font("Segoe UI", 9F);
            lblSenha.ForeColor = Color.DarkGray;
            lblSenha.Location = new Point(0, 80);
            lblSenha.Size = new Size(350, 20);
            lblSenha.TextAlign = ContentAlignment.MiddleCenter;

            // --- txtSenha ---
            txtSenha.PasswordChar = '●';
            txtSenha.Font = new Font("Segoe UI", 16F, FontStyle.Bold);
            txtSenha.BackColor = Color.FromArgb(45, 45, 50);
            txtSenha.ForeColor = Color.Cyan;
            txtSenha.BorderStyle = BorderStyle.FixedSingle;
            txtSenha.Location = new Point(75, 110);
            txtSenha.Size = new Size(200, 40);
            txtSenha.TextAlign = HorizontalAlignment.Center;

            // --- btnEntrar ---
            btnEntrar.Text = "ENTRAR";
            btnEntrar.Font = new Font("Segoe UI", 10F, FontStyle.Bold);
            btnEntrar.FlatStyle = FlatStyle.Flat;
            btnEntrar.BackColor = Color.FromArgb(0, 120, 215); // Azul padrão Nexus
            btnEntrar.ForeColor = Color.White;
            btnEntrar.Cursor = Cursors.Hand;
            btnEntrar.Location = new Point(75, 175);
            btnEntrar.Size = new Size(95, 35);
            btnEntrar.Click += btnEntrar_Click;

            // --- btnCancelar ---
            btnCancelar.Text = "SAIR";
            btnCancelar.Font = new Font("Segoe UI", 10F, FontStyle.Regular);
            btnCancelar.FlatStyle = FlatStyle.Flat;
            btnCancelar.BackColor = Color.Transparent;
            btnCancelar.ForeColor = Color.Gray;
            btnCancelar.Cursor = Cursors.Hand;
            btnCancelar.Location = new Point(180, 175);
            btnCancelar.Size = new Size(95, 35);
            btnCancelar.Click += btnCancelar_Click;

            // --- Finalização ---
            this.AcceptButton = btnEntrar;
            this.CancelButton = btnCancelar;
            this.Controls.AddRange(new Control[] { lblTitulo, lblSenha, txtSenha, btnEntrar, btnCancelar });

            this.ResumeLayout(false);
            this.PerformLayout();
        }

        private void btnEntrar_Click(object? sender, EventArgs e)
        {
            if (txtSenha.Text == SENHA_ADMIN)
            {
                this.DialogResult = DialogResult.OK;
                this.Close();
            }
            else
            {
                MessageBox.Show("Senha incorreta. Verifique os dados e tente novamente.", "NEXUS - Acesso Negado",
                    MessageBoxButtons.OK, MessageBoxIcon.Warning);
                txtSenha.Clear();
                txtSenha.Focus();
            }
        }

        private void btnCancelar_Click(object? sender, EventArgs e)
        {
            this.DialogResult = DialogResult.Cancel;
            this.Close();
        }
    }
}