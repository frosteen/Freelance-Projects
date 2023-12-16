using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;
using Thesis.Ver2.Lessons.FirstQuarterLessons.Lesson_3;

namespace Thesis.Ver2.Lessons.FirstQuarterLessons.Lesson2
{
    public partial class TntasPage6 : UserControl
    {
        public TntasPage6()
        {
            InitializeComponent();
        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void TntasPage6_Load(object sender, EventArgs e)
        {

        }

        private void buttonBack_Click(object sender, EventArgs e)
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

        private void bluntBorderBtn1_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("FirstQuarter"))
            {
                FirstQuarter FS = new FirstQuarter();
                FS.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(FS);
            }
            Form1.Instance.PnlContainer.Controls["FirstQuarter"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }

        private void bluntBorderBtn2_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("TsfntPage1"))
            {
                TsfntPage1 P1 = new TsfntPage1();
                P1.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(P1);
            }
            Form1.Instance.PnlContainer.Controls["TsfntPage1"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }
    }
}
