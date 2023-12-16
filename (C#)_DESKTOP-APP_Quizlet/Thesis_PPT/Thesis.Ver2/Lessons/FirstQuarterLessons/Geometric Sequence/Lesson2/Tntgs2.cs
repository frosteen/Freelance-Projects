using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace Thesis.Ver2.Lessons.FirstQuarterLessons.Geometric_Sequence.Lesson2
{
    public partial class Tntgs2 : UserControl
    {
        public Tntgs2()
        {
            InitializeComponent();
        }

        private void buttonNext_Click(object sender, EventArgs e)
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

        private void buttonBack_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("Tntgs1"))
            {
                Tntgs1 TntGS1 = new Tntgs1();
                TntGS1.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(TntGS1);
            }
            Form1.Instance.PnlContainer.Controls["Tntgs1"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }

        private void label1_Click(object sender, EventArgs e)
        {

        }
    }
}
