using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace Thesis.Ver2.Lessons.FirstQuarterLessons.Polynomials.Lesson1
{
    public partial class IEP1 : UserControl
    {
        public IEP1()
        {
            InitializeComponent();
        }

        private void label5_Click(object sender, EventArgs e)
        {

        }

        private void buttonBack_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("Polynomialsmain"))
            {
                Polynomialsmain SPmain = new Polynomialsmain();
                SPmain.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(SPmain);
            }
            Form1.Instance.PnlContainer.Controls["Polynomialsmain"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }

        private void buttonNext_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("IEP2"))
            {
                IEP2 ieps2 = new IEP2();
                ieps2.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(ieps2);
            }
            Form1.Instance.PnlContainer.Controls["IEP2"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }
    }
}
