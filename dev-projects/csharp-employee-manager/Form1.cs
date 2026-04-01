using System;
using System.Collections.Generic;
using System.Windows.Forms;
using System.IO;
using System.Text.Json;
using System.Drawing;
using System.Linq;

namespace Nexus_1._0
{
    public partial class Form1 : Form
    {
        // --- Modelo de Dados ---
        public class Funcionario
        {
            public string Nome { get; set; } = "";
            public int Cracha { get; set; }
            public string TipoCesta { get; set; } = "";
            public bool Retirou { get; set; }
            public string LogRetirada { get; set; } = "";
        }

        // --- Controles ---
        private List<Funcionario> funcionarios = new();
        private Funcionario? atual = null;

        private Panel pnlCentral;
        private PictureBox pictureBox1;
        private TextBox txtCracha;
        private Button btnBuscar, btnOk, btnExportar;
        private Label lblTitulo, lblCracha, lblInfo;

        public Form1()
        {
            ConfigurarInterface();
            CarregarDados();
        }

        private void ConfigurarInterface()
        {
            // Configurações do Formulário 
            this.Text = "NEXUS - Sistema de Logística";
            this.Size = new Size(600, 750);
            this.StartPosition = FormStartPosition.CenterScreen;
            this.BackColor = Color.FromArgb(30, 30, 35);
            this.FormBorderStyle = FormBorderStyle.FixedSingle;
            this.MaximizeBox = false;
            //ícone da janela
            string iconPath = Path.Combine(Application.StartupPath, "favicon.ico");
            if (File.Exists(iconPath))
            {
                this.Icon = new Icon(iconPath);
            }

            // Painel Central (Contêiner principal)
            pnlCentral = new Panel
            {
                Size = new Size(500, 700),
                Location = new Point(50, 20),
                BackColor = Color.Transparent
            };
            this.Controls.Add(pnlCentral);

            // Configurações da Logo
            int novaLargura = 350;
            int novaAltura = 138;

            pictureBox1 = new PictureBox
            {
                Size = new Size(novaLargura, novaAltura),
                Location = new Point((500 - novaLargura) / 2, 10),
                SizeMode = PictureBoxSizeMode.Zoom,
                BackColor = Color.Transparent
            };

            string logoPath = Path.Combine(Application.StartupPath, "logo.png");
            if (File.Exists(logoPath))
                pictureBox1.Image = Image.FromFile(logoPath);

            // Título — Mais abaixo da logo 
            lblTitulo = new Label
            {
                Text = "CONSULTA CESTA NATAL",
                Font = new Font("Segoe UI", 18, FontStyle.Bold),
                ForeColor = Color.White,
                Size = new Size(500, 40),
                Location = new Point(0, 195),
                TextAlign = ContentAlignment.MiddleCenter
            };

            // Instrução Crachá 
            lblCracha = new Label
            {
                Text = "DIGITE O NÚMERO DO CRACHÁ:",
                Font = new Font("Segoe UI", 10, FontStyle.Regular),
                ForeColor = Color.DarkGray,
                Size = new Size(500, 20),
                Location = new Point(0, 250),
                TextAlign = ContentAlignment.MiddleCenter
            };

            // Campo de Entrada 
            txtCracha = new TextBox
            {
                Font = new Font("Segoe UI", 24, FontStyle.Bold),
                Size = new Size(200, 60),
                Location = new Point(150, 280),
                TextAlign = HorizontalAlignment.Center,
                BackColor = Color.FromArgb(45, 45, 50),
                ForeColor = Color.Cyan,
                BorderStyle = BorderStyle.FixedSingle
            };
            txtCracha.KeyPress += (s, e) => { if (e.KeyChar == (char)13) BuscarFuncionario(); };

            // Botão Buscar 
            btnBuscar = new Button
            {
                Text = "BUSCAR",
                Size = new Size(200, 50),
                Location = new Point(150, 340),
                FlatStyle = FlatStyle.Flat,
                BackColor = Color.FromArgb(0, 120, 215),
                ForeColor = Color.White,
                Font = new Font("Segoe UI", 11, FontStyle.Bold),
                Cursor = Cursors.Hand
            };
            btnBuscar.Click += (s, e) => BuscarFuncionario();

            // Label de Informação/Resultado (Y: 420)
            lblInfo = new Label
            {
                Text = "Aguardando leitura...",
                Font = new Font("Segoe UI", 11, FontStyle.Bold),
                ForeColor = Color.Gray,
                Size = new Size(460, 80),
                Location = new Point(20, 420),
                TextAlign = ContentAlignment.MiddleCenter
            };

            // Botão Confirmar Entrega 
            btnOk = new Button
            {
                Text = "CONFIRMAR ENTREGA",
                Size = new Size(240, 45),
                Location = new Point(130, 520),
                FlatStyle = FlatStyle.Flat,
                BackColor = Color.SpringGreen,
                ForeColor = Color.Black,
                Font = new Font("Segoe UI", 11, FontStyle.Bold),
                Visible = false,
                Cursor = Cursors.Hand
            };
            btnOk.Click += btnOk_Click;

            // Botão Exportar (Rodapé do painel)
            btnExportar = new Button
            {
                Text = "EXPORTAR RELATÓRIO",
                Size = new Size(180, 35),
                Location = new Point(160, 620),
                FlatStyle = FlatStyle.Flat,
                ForeColor = Color.DimGray,
                Font = new Font("Segoe UI", 8),
                Cursor = Cursors.Hand
            };
            btnExportar.Click += btnExportar_Click;

            // Adicionar todos os componentes ao painel central
            pnlCentral.Controls.AddRange(new Control[]
            {
                pictureBox1, lblTitulo, lblCracha,
                txtCracha, btnBuscar, lblInfo, btnOk, btnExportar
            });
        }

        // --- Lógica de Dados ---

        private void CarregarDados()
        {
            string dbPath = Path.Combine(Application.StartupPath, "funcionarios.json");
            if (File.Exists(dbPath))
            {
                try
                {
                    string json = File.ReadAllText(dbPath);
                    funcionarios = JsonSerializer.Deserialize<List<Funcionario>>(json) ?? new List<Funcionario>();
                }
                catch { GerarDadosMock(); }
            }
            else
            {
                GerarDadosMock();
            }
        }

        private void GerarDadosMock()
        {
            funcionarios = new List<Funcionario>
            {
                new Funcionario { Nome = "KLEBERSON (ADMIN)", Cracha = 1, TipoCesta = "KIT PREMIUM", Retirou = false }
            };
            SalvarDados();
        }

        private void SalvarDados()
        {
            string dbPath = Path.Combine(Application.StartupPath, "funcionarios.json");
            File.WriteAllText(dbPath, JsonSerializer.Serialize(funcionarios,
                new JsonSerializerOptions { WriteIndented = true }));
        }

        private void BuscarFuncionario()
        {
            btnOk.Visible = false;
            if (!int.TryParse(txtCracha.Text, out int n))
            {
                AtualizarStatus("Digite um número de crachá válido!", Color.Red);
                return;
            }

            atual = funcionarios.FirstOrDefault(f => f.Cracha == n);

            if (atual == null)
                AtualizarStatus("❌ Funcionário não encontrado!", Color.Red);
            else if (atual.Retirou)
                AtualizarStatus($"⚠ {atual.Nome}\nRetirado em: {atual.LogRetirada}", Color.Orange);
            else
            {
                AtualizarStatus($"✅ {atual.Nome}\n{atual.TipoCesta}", Color.SpringGreen);
                btnOk.Visible = true;
                btnOk.Focus();
            }
        }

        private void AtualizarStatus(string texto, Color cor)
        {
            lblInfo.Text = texto;
            lblInfo.ForeColor = cor;
        }

        private void btnOk_Click(object sender, EventArgs e)
        {
            if (atual == null) return;
            atual.Retirou = true;
            atual.LogRetirada = DateTime.Now.ToString("G");
            SalvarDados();
            AtualizarStatus("RETIRADA REGISTRADA COM SUCESSO!", Color.Cyan);
            btnOk.Visible = false;
            txtCracha.Clear();
            txtCracha.Focus();
        }

        private void btnExportar_Click(object sender, EventArgs e)
        {
            // 1. Configura a janela de salvar arquivo
            using (SaveFileDialog sfd = new SaveFileDialog())
            {
                sfd.Filter = "Arquivo CSV (*.csv)|*.csv";
                sfd.Title = "Exportar Relatório de Cestas";
                sfd.FileName = $"Relatorio_Cestas_{DateTime.Now:dd-MM-yyyy}"; // Nome sugestivo

                // 2. Abre a janela e verifica se o usuário clicou em "Salvar"
                if (sfd.ShowDialog() == DialogResult.OK)
                {
                    try
                    {
                        // 3. Monta o conteúdo do CSV
                        var csv = new List<string> { "Nome;Cracha;Cesta;Data" };
                        csv.AddRange(funcionarios.Select(f =>
                            $"{f.Nome};{f.Cracha};{f.TipoCesta};{(string.IsNullOrEmpty(f.LogRetirada) ? "Pendente" : f.LogRetirada)}"));

                        // 4. Salva no caminho escolhido pelo usuário (sfd.FileName)
                        File.WriteAllLines(sfd.FileName, csv, System.Text.Encoding.UTF8);

                        MessageBox.Show("Relatório exportado com sucesso!", "NEXUS - Exportação",
                            MessageBoxButtons.OK, MessageBoxIcon.Information);
                    }
                    catch (Exception ex)
                    {
                        MessageBox.Show($"Erro ao salvar o arquivo: {ex.Message}", "Erro",
                            MessageBoxButtons.OK, MessageBoxIcon.Error);
                    }
                }
            }
        }
    }
}