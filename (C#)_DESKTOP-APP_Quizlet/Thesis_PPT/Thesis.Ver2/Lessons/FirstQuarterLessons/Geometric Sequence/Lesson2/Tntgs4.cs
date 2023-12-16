using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace Thesis.Ver2.Lessons.FirstQuarterLessons.Geometric_Sequence.Lesson2
{
    public partial class Tntgs4 : UserControl
    {
        public Tntgs4()
        {
            InitializeComponent();
        }

        private void buttonBack_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("Tntgs3"))
            {
                Tntgs3 TntGS3 = new Tntgs3();
                TntGS3.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(TntGS3);
            }
            Form1.Instance.PnlContainer.Controls["Tntgs3"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }

        private void buttonNext_Click(object sender, EventArgs e)
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
    }
}
