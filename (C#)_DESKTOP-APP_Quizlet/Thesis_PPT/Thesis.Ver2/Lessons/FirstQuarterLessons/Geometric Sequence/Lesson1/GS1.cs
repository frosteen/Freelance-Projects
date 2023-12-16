using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace Thesis.Ver2.Lessons.FirstQuarterLessons.Geometric_Sequence.Lesson1
{
    public partial class GS1 : UserControl
    {
        public GS1()
        {
            InitializeComponent();
        }

        private void buttonBack_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("GeometricSequenceMain"))
            {
                GeometricSequenceMain GeoSmain = new GeometricSequenceMain();
                GeoSmain.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(GeoSmain);
            }
            Form1.Instance.PnlContainer.Controls["GeometricSequenceMain"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }

        private void buttonNext_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("GS2"))
            {
                GS2 GeoS2 = new GS2();
                GeoS2.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(GeoS2);
            }
            Form1.Instance.PnlContainer.Controls["GS2"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }
    }
}
