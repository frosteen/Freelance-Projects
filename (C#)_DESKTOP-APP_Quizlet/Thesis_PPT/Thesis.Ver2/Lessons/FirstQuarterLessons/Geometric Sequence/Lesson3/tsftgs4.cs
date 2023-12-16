using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace Thesis.Ver2.Lessons.FirstQuarterLessons.Geometric_Sequence.Lesson3
{
    public partial class tsftgs4 : UserControl
    {
        public tsftgs4()
        {
            InitializeComponent();
        }

        private void pictureBox1_Click(object sender, EventArgs e)
        {

        }

        private void buttonBack_Click(object sender, EventArgs e)
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

        private void buttonNext_Click(object sender, EventArgs e)
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
    }
}
