using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace Thesis.Ver2.Lessons.FirstQuarterLessons.Lesson1
{
    public partial class ASPage2 : UserControl
    {
        public ASPage2()
        {
            InitializeComponent();
        }

        private void buttonBack_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("ASPage1"))
            {
                ASPage1 P1 = new ASPage1();
                P1.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(P1);
            }
            Form1.Instance.PnlContainer.Controls["ASPage1"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }

        private void buttonNext_Click(object sender, EventArgs e)
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

        private void panel1_Paint(object sender, PaintEventArgs e)
        {

        }

        private void label5_Click(object sender, EventArgs e)
        {

        }

        private void label2_Click(object sender, EventArgs e)
        {

        }

        private void panel6_Paint(object sender, PaintEventArgs e)
        {

        }
    }
}
