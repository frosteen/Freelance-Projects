using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace Thesis.Ver2.Lessons.FirstQuarterLessons.Geometric_Sequence.Lesson1
{
    public partial class GS2 : UserControl
    {
        public GS2()
        {
            InitializeComponent();
        }

        private void buttonNext_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("GS3"))
            {
                GS3 GeoS3 = new GS3();
                GeoS3.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(GeoS3);
            }
            Form1.Instance.PnlContainer.Controls["GS3"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }

        private void buttonBack_Click(object sender, EventArgs e)
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
    }
}
