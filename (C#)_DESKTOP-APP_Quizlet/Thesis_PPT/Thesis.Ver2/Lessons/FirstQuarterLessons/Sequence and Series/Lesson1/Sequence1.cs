using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace Thesis.Ver2.Lessons.FirstQuarterLessons.Sequence_and_Series.Lesson1
{
    public partial class Sequence1 : UserControl
    {
        public Sequence1()
        {
            InitializeComponent();
        }

        private void buttonBack_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("SequenceAndSeriesMain"))
            {
                SequenceAndSeriesMain SAS = new SequenceAndSeriesMain();
                SAS.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(SAS);
            }
            Form1.Instance.PnlContainer.Controls["SequenceAndSeriesMain"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }

        private void buttonNext_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("Sequence2"))
            {
                Sequence2 S2 = new Sequence2();
                S2.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(S2);
            }
            Form1.Instance.PnlContainer.Controls["Sequence2"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }
    }
}
