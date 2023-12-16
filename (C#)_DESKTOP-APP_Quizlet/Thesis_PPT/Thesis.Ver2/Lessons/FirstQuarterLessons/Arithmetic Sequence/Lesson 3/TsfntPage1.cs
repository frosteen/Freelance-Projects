using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;
using Thesis.Ver2.Lessons.FirstQuarterLessons.Arithmetic_Sequence;

namespace Thesis.Ver2.Lessons.FirstQuarterLessons.Lesson_3
{
    public partial class TsfntPage1 : UserControl
    {
        public TsfntPage1()
        {
            InitializeComponent();
        }

        private void label5_Click(object sender, EventArgs e)
        {

        }

        private void buttonBack_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("ArithmeticMain"))
            {
                ArithmeticMain AM = new ArithmeticMain();
                AM.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(AM);
            }
            Form1.Instance.PnlContainer.Controls["ArithmeticMain"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }

        private void buttonNext_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("TsnftPage2"))
            {
                TsnftPage2 P2 = new TsnftPage2();
                P2.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(P2);
            }
            Form1.Instance.PnlContainer.Controls["TsnftPage2"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }
    }
}
