using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace Thesis.Ver2.Lessons.FirstQuarterLessons.Geometric_Sequence.Lesson3
{
    public partial class tsftgs1 : UserControl
    {
        public tsftgs1()
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
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("tsftgs2"))
            {
                tsftgs2 TsftGS2 = new tsftgs2();
                TsftGS2.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(TsftGS2);
            }
            Form1.Instance.PnlContainer.Controls["tsftgs2"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }
    }
}
