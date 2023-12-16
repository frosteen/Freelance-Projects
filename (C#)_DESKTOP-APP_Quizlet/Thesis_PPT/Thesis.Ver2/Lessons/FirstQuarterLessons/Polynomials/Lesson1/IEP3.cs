using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace Thesis.Ver2.Lessons.FirstQuarterLessons.Polynomials.Lesson1
{
    public partial class IEP3 : UserControl
    {
        public IEP3()
        {
            InitializeComponent();
        }

        private void IEP3_Load(object sender, EventArgs e)
        {

        }

        private void buttonBack_Click(object sender, EventArgs e)
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

     

        private void label3_Click(object sender, EventArgs e)
        {

        }

        private void buttonNext_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("IEP4"))
            {
                IEP4 ieps4 = new IEP4();
                ieps4.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(ieps4);
            }
            Form1.Instance.PnlContainer.Controls["IEP4"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }
    }
}
