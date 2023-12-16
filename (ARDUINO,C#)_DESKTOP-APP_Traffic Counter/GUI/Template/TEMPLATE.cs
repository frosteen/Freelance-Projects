using System;
using System.Drawing;
using System.Windows.Forms;

namespace Template
{
    public partial class TEMPLATE : Form
    {
        Point lastClick;

        public TEMPLATE()
        {
            InitializeComponent();
        }

        //PANEL CONFIGURATIONS
        private void buttonClose_Click(object sender, EventArgs e)
        {
            Application.Exit();
        }

        private void buttonMinimize_Click(object sender, EventArgs e)
        {
            this.WindowState = FormWindowState.Minimized;
        }

        private void panelTitle_MouseDown(object sender, MouseEventArgs e)
        {
            lastClick = e.Location;
        }

        private void panelTitle_MouseMove(object sender, MouseEventArgs e)
        {
            if (e.Button == MouseButtons.Left)
            {
                this.Left += e.X - lastClick.X;
                this.Top += e.Y - lastClick.Y;
            }
        }

        private void buttonMinimize_Enter(object sender, EventArgs e)
        {
            labelTitle.Focus();
        }
    }
}
