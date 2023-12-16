using System;
using System.Drawing;
using System.Windows.Forms;

namespace LijaucoDentist
{
    public partial class AdminUI : Form
    {

        public AdminUI()
        {
            InitializeComponent();
            this.Location = new Point(Screen.PrimaryScreen.WorkingArea.Size.Width / 2 - this.Width / 2, 0);
        }

        private void buttonMinimize_Click(object sender, EventArgs e)
        {
            this.WindowState = FormWindowState.Minimized;
        }

        private void buttonClose_Click(object sender, EventArgs e)
        {
            Application.Exit();
        }

        private void buttonSettings_Click(object sender, EventArgs e)
        {
            Form loginUI = new LoginUI(this, false);
            loginUI.StartPosition = FormStartPosition.CenterScreen;
            loginUI.ShowDialog();
        }

        private void buttonDatabase_Click(object sender, EventArgs e)
        {
            Form form = new DatabaseUI(this);
            form.StartPosition = FormStartPosition.CenterScreen;
            form.ShowDialog();
        }

        private void buttonSettings_Enter(object sender, EventArgs e)
        {
            labelTitle.Focus();
        }

        private void buttonMinimize_Enter(object sender, EventArgs e)
        {
            labelTitle.Focus();
        }
    }
}
