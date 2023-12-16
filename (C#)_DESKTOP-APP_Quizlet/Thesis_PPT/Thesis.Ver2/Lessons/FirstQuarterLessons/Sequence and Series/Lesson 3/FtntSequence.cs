using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace Thesis.Ver2.Lessons.FirstQuarterLessons.Sequence_and_Series.Lesson_3
{
    public partial class FtntSequence : UserControl
    {
        public FtntSequence()
        {
            InitializeComponent();
        }

        private void buttonNext_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("FtntSequence2"))
            {
                FtntSequence2 Ftnt2 = new FtntSequence2();
                Ftnt2.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(Ftnt2);
            }
            Form1.Instance.PnlContainer.Controls["FtntSequence2"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
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
    }
}
