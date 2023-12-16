using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace Thesis.Ver2.Lessons.FirstQuarterLessons.Lesson1
{
    public partial class ASPage4 : UserControl
    {
        public ASPage4()
        {
            InitializeComponent();
        }

        private void label2_Click(object sender, EventArgs e)
        {

        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void buttonBack_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("ASPage3"))
            {
                ASPage3 P3 = new ASPage3();
                P3.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(P3);
            }
            Form1.Instance.PnlContainer.Controls["ASPage3"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }

        private void panel4_Paint(object sender, PaintEventArgs e)
        {

        }

        private void pictureBox1_Click(object sender, EventArgs e)
        {

        }

        private void label2_Click_1(object sender, EventArgs e)
        {

        }

        private void buttonNext_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("ASPage5"))
            {
                ASPage5 P5 = new ASPage5();
                P5.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(P5);
            }
            Form1.Instance.PnlContainer.Controls["ASPage5"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }
    }
}
