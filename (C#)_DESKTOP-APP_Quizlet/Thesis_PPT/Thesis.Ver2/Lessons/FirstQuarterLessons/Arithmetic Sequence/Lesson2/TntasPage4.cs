using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace Thesis.Ver2.Lessons.FirstQuarterLessons.Lesson2
{
    public partial class TntasPage4 : UserControl
    {
        public TntasPage4()
        {
            InitializeComponent();
        }

        private void label2_Click(object sender, EventArgs e)
        {

        }

        private void buttonNext_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("TntasPage5"))
            {
                TntasPage5 P5 = new TntasPage5();
                P5.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(P5);
            }
            Form1.Instance.PnlContainer.Controls["TntasPage5"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }

        private void buttonBack_Click(object sender, EventArgs e)
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
