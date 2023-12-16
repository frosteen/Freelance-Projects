using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace Thesis.Ver2.Lessons.FirstQuarterLessons.Lesson2
{
    public partial class TntasPage5 : UserControl
    {
        public TntasPage5()
        {
            InitializeComponent();
        }

        private void buttonNext_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("TntasPage6"))
            {
                TntasPage6 P6 = new TntasPage6();
                P6.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(P6);
            }
            Form1.Instance.PnlContainer.Controls["TntasPage6"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }

        private void buttonBack_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("TntasPage4"))
            {
                TntasPage4 P4 = new TntasPage4();
                P4.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(P4);
            }
            Form1.Instance.PnlContainer.Controls["TntasPage4"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }
    }
}
