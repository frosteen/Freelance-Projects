using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;
using Thesis.Ver2.Lessons.FirstQuarterLessons.Polynomials.Lesson1;

namespace Thesis.Ver2.Lessons.FirstQuarterLessons.Polynomials
{
    public partial class Polynomialsmain : UserControl
    {
        public Polynomialsmain()
        {
            InitializeComponent();
        }

        private void bluntBorderBtn1_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("IEP1"))
            {
                IEP1 ieps1 = new IEP1();
                ieps1.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(ieps1);
            }
            Form1.Instance.PnlContainer.Controls["IEP1"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }

        private void buttonBack_Click(object sender, EventArgs e)
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
