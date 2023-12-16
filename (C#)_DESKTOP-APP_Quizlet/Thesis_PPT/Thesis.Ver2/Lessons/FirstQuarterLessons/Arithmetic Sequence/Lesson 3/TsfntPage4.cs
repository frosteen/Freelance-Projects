using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace Thesis.Ver2.Lessons.FirstQuarterLessons.Lesson_3
{
    public partial class TsfntPage4 : UserControl
    {
        public TsfntPage4()
        {
            InitializeComponent();
        }

        private void buttonBack_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("TsfntPage3"))
            {
                TsfntPage3 P3 = new TsfntPage3();
                P3.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(P3);
            }
            Form1.Instance.PnlContainer.Controls["TsfntPage3"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void buttonNext_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("TsfntPage5"))
            {
                TsfntPage5 P5 = new TsfntPage5();
                P5.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(P5);
            }
            Form1.Instance.PnlContainer.Controls["TsfntPage5"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }
    }
}
