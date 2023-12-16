using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace Thesis.Ver2.Lessons.FirstQuarterLessons.Lesson_3
{
    public partial class TsfntPage5 : UserControl
    {
        public TsfntPage5()
        {
            InitializeComponent();
        }

        private void buttonBack_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("TsfntPage4"))
            {
                TsfntPage4 P4 = new TsfntPage4();
                P4.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(P4);
            }
            Form1.Instance.PnlContainer.Controls["TsfntPage4"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void buttonNext_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("TsfntPage6"))
            {
                TsfntPage6 P6 = new TsfntPage6();
                P6.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(P6);
            }
            Form1.Instance.PnlContainer.Controls["TsfntPage6"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }
    }
}
