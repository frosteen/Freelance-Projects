using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;
using Thesis.Ver2.Lessons.FirstQuarterLessons.Geometric_Sequence.Lesson1;
using Thesis.Ver2.Lessons.FirstQuarterLessons.Geometric_Sequence.Lesson2;
using Thesis.Ver2.Lessons.FirstQuarterLessons.Geometric_Sequence.Lesson3;

namespace Thesis.Ver2.Lessons.FirstQuarterLessons.Geometric_Sequence
{
    public partial class GeometricSequenceMain : UserControl
    {
        public GeometricSequenceMain()
        {
            InitializeComponent();
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

        private void bluntBorderBtn1_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("GS1"))
            {
                GS1 GeoS1 = new GS1();
                GeoS1.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(GeoS1);
            }
            Form1.Instance.PnlContainer.Controls["GS1"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }

        private void bluntBorderBtn3_Click(object sender, EventArgs e)
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

        private void GeometricSequenceMain_Load(object sender, EventArgs e)
        {

        }

        private void bluntBorderBtn4_Click(object sender, EventArgs e)
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
