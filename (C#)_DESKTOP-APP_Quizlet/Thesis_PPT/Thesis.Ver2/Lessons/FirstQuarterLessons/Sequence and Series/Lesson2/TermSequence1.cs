using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace Thesis.Ver2.Lessons.FirstQuarterLessons.Sequence_and_Series.Lesson2
{
    public partial class TermSequence1 : UserControl
    {
        public TermSequence1()
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
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("TermSequence2"))
            {
                TermSequence2 TS2 = new TermSequence2();
                TS2.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(TS2);
            }
            Form1.Instance.PnlContainer.Controls["TermSequence2"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }
    }
}
