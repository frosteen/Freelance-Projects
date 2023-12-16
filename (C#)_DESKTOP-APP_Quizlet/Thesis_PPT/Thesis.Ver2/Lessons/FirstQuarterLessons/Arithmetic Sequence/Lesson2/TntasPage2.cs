using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace Thesis.Ver2.Lessons.FirstQuarterLessons.Lesson2
{
    public partial class TntasPage2 : UserControl
    {
        public TntasPage2()
        {
            InitializeComponent();
        }

        private void panel1_Paint(object sender, PaintEventArgs e)
        {

        }

        private void buttonBack_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("TntasPage1"))
            {
                TntasPage1 P1 = new TntasPage1();
                P1.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(P1);
            }
            Form1.Instance.PnlContainer.Controls["TntasPage1"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }

        private void buttonNext_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("TntasPage3"))
            {
                TntasPage3 P3 = new TntasPage3();
                P3.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(P3);
            }
            Form1.Instance.PnlContainer.Controls["TntasPage3"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }
    }
}
