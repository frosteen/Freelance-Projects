using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;
using Thesis.Ver2.Lessons.FirstQuarterLessons.Geometric_Sequence.Lesson2;

namespace Thesis.Ver2.Lessons.FirstQuarterLessons.Geometric_Sequence.Lesson1
{
    public partial class GS5 : UserControl
    {
        public GS5()
        {
            InitializeComponent();
        }

        private void label6_Click(object sender, EventArgs e)
        {

        }

        private void buttonBack_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("GS4"))
            {
                GS4 GeoS4 = new GS4();
                GeoS4.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(GeoS4);
            }
            Form1.Instance.PnlContainer.Controls["GS4"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }

        private void GS5_Load(object sender, EventArgs e)
        {

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

        private void bluntBorderBtn1_Click_1(object sender, EventArgs e)
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
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("Tntgs1"))
            {
                Tntgs1 TntGS1 = new Tntgs1();
                TntGS1.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(TntGS1);
            }
            Form1.Instance.PnlContainer.Controls["Tntgs1"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }
    }
}
