using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace Thesis.Ver2.Lessons.FirstQuarterLessons.Polynomials.Lesson1
{
    public partial class IEP2 : UserControl
    {
        public IEP2()
        {
            InitializeComponent();
        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void buttonBack_Click(object sender, EventArgs e)
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

        private void label3_Click(object sender, EventArgs e)
        {

        }

        private void buttonNext_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("IEP3"))
            {
                IEP3 ieps3 = new IEP3();
                ieps3.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(ieps3);
            }
            Form1.Instance.PnlContainer.Controls["IEP3"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }
    }
}
