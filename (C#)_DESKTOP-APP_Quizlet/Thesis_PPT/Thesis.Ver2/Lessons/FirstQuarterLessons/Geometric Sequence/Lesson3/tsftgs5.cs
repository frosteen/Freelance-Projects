using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace Thesis.Ver2.Lessons.FirstQuarterLessons.Geometric_Sequence.Lesson3
{
    public partial class tsftgs5 : UserControl
    {
        public tsftgs5()
        {
            InitializeComponent();
        }

        private void buttonBack_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("tsftgs4"))
            {
                tsftgs4 TsftGS4 = new tsftgs4();
                TsftGS4.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(TsftGS4);
            }
            Form1.Instance.PnlContainer.Controls["tsftgs4"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }

        private void buttonNext_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("tsftgs6"))
            {
                tsftgs6 TsftGS6 = new tsftgs6();
                TsftGS6.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(TsftGS6);
            }
            Form1.Instance.PnlContainer.Controls["tsftgs6"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }

        private void label3_Click(object sender, EventArgs e)
        {

        }
    }
}
