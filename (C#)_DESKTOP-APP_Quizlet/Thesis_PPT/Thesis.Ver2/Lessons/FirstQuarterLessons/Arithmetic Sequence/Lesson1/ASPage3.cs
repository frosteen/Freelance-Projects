using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace Thesis.Ver2.Lessons.FirstQuarterLessons.Lesson1
{
    public partial class ASPage3 : UserControl
    {
        public ASPage3()
        {
            InitializeComponent();
        }

        private void buttonBack_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("ASPage2"))
            {
                ASPage2 P2 = new ASPage2();
                P2.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(P2);
            }
            Form1.Instance.PnlContainer.Controls["ASPage2"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }

        private void pictureBox1_Click(object sender, EventArgs e)
        {

        }

        private void label4_Click(object sender, EventArgs e)
        {

        }

        private void panel1_Paint(object sender, PaintEventArgs e)
        {

        }

        private void buttonNext_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("ASPage4"))
            {
                ASPage4 P4 = new ASPage4();
                P4.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(P4);
            }
            Form1.Instance.PnlContainer.Controls["ASPage4"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }

        private void panel11_Paint(object sender, PaintEventArgs e)
        {

        }

        private void label12_Click(object sender, EventArgs e)
        {

        }
    }
}
