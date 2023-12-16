using System;
using System.Drawing;
using System.Windows.Forms;

namespace LijaucoDentist
{
    public partial class ViewLegendsUI : Form
    {
        Point lastClick;

        public ViewLegendsUI()
        {
            InitializeComponent();
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

        private void buttonMinimize_Click(object sender, EventArgs e)
        {
            this.WindowState = FormWindowState.Minimized;
        }

        private void buttonBack_Click(object sender, EventArgs e)
        {
            labelTitle.Focus();
            this.Close();
        }

        private void buttonBack_Enter(object sender, EventArgs e)
        {
            labelTitle.Focus();
        }
    }
}
