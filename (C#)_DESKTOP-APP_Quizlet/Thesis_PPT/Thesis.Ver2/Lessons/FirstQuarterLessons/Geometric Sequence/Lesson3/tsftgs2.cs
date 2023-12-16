using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace Thesis.Ver2.Lessons.FirstQuarterLessons.Geometric_Sequence.Lesson3
{
    public partial class tsftgs2 : UserControl
    {
        public tsftgs2()
        {
            InitializeComponent();
        }

        private void buttonBack_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("tsftgs1"))
            {
                tsftgs1 TsftGS1 = new tsftgs1();
                TsftGS1.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(TsftGS1);
            }
            Form1.Instance.PnlContainer.Controls["tsftgs1"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void buttonNext_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("tsftgs3"))
            {
                tsftgs3 TsftGS3 = new tsftgs3();
                TsftGS3.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(TsftGS3);
            }
            Form1.Instance.PnlContainer.Controls["tsftgs3"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }
    }
}
