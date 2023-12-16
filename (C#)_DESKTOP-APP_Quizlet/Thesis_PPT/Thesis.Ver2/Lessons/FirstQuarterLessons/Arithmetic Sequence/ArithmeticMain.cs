using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;
using Thesis.Ver2._3_Main_Forms;
using Thesis.Ver2.Lessons.FirstQuarterLessons.Lesson_3;
using Thesis.Ver2.Lessons.FirstQuarterLessons.Lesson1;
using Thesis.Ver2.Lessons.FirstQuarterLessons.Lesson2;

namespace Thesis.Ver2.Lessons.FirstQuarterLessons.Arithmetic_Sequence
{
    public partial class ArithmeticMain : UserControl
    {
        public ArithmeticMain()
        {
            InitializeComponent();
        }

        private void bluntBorderBtn1_Click(object sender, EventArgs e)
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

        private void bluntBorderBtn3_Click(object sender, EventArgs e)
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

        private void bluntBorderBtn4_Click(object sender, EventArgs e)
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

        private void buttonBack_Click(object sender, EventArgs e)
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
    }
}
