using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace Thesis.Ver2.Lessons.FirstQuarterLessons.Lesson_3
{
    public partial class TsnftPage2 : UserControl
    {
        public TsnftPage2()
        {
            InitializeComponent();
        }

        private void panel3_Paint(object sender, PaintEventArgs e)
        {

        }

        private void buttonBack_Click(object sender, EventArgs e)
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

        private void buttonNext_Click(object sender, EventArgs e)
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
    }
}
