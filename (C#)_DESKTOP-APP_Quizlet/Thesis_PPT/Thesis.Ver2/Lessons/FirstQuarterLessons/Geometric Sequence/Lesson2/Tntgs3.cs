using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace Thesis.Ver2.Lessons.FirstQuarterLessons.Geometric_Sequence.Lesson2
{
    public partial class Tntgs3 : UserControl
    {
        public Tntgs3()
        {
            InitializeComponent();
        }

        private void buttonBack_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("Tntgs2"))
            {
                Tntgs2 TntGS2 = new Tntgs2();
                TntGS2.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(TntGS2);
            }
            Form1.Instance.PnlContainer.Controls["Tntgs2"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }

        private void buttonNext_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("Tntgs4"))
            {
                Tntgs4 TntGS4 = new Tntgs4();
                TntGS4.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(TntGS4);
            }
            Form1.Instance.PnlContainer.Controls["Tntgs4"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }
    }
}
