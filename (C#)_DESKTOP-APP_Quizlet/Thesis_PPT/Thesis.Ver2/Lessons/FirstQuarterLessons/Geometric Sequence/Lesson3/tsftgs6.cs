using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace Thesis.Ver2.Lessons.FirstQuarterLessons.Geometric_Sequence.Lesson3
{
    public partial class tsftgs6 : UserControl
    {
        public tsftgs6()
        {
            InitializeComponent();
        }

        private void buttonBack_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("tsftgs5"))
            {
                tsftgs5 TsftGS5 = new tsftgs5();
                TsftGS5.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(TsftGS5);
            }
            Form1.Instance.PnlContainer.Controls["tsftgs5"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }

        private void label2_Click(object sender, EventArgs e)
        {

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
    }
}
