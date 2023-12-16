using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;
using Thesis.Ver2.Lessons.FirstQuarterLessons.Geometric_Sequence.Lesson3;

namespace Thesis.Ver2.Lessons.FirstQuarterLessons.Geometric_Sequence.Lesson2
{
    public partial class Tntgs6 : UserControl
    {
        public Tntgs6()
        {
            InitializeComponent();
        }

        private void buttonBack_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("Tntgs5"))
            {
                Tntgs5 TntGS5 = new Tntgs5();
                TntGS5.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(TntGS5);
            }
            Form1.Instance.PnlContainer.Controls["Tntgs5"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
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

        private void bluntBorderBtn2_Click(object sender, EventArgs e)
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
    }
}
