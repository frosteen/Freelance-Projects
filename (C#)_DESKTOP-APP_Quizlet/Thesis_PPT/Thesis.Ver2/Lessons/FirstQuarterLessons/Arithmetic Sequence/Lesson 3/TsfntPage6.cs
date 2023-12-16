using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace Thesis.Ver2.Lessons.FirstQuarterLessons.Lesson_3
{
    public partial class TsfntPage6 : UserControl
    {
        public TsfntPage6()
        {
            InitializeComponent();
        }

        private void pictureBox2_Click(object sender, EventArgs e)
        {

        }

        private void buttonBack_Click(object sender, EventArgs e)
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

        private void buttonNext_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("TsfntPage7"))
            {
                TsfntPage7 P7 = new TsfntPage7();
                P7.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(P7);
            }
            Form1.Instance.PnlContainer.Controls["TsfntPage7"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }
    }
}
