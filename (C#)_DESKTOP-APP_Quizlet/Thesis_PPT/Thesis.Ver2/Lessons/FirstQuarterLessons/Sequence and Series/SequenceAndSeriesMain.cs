using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;
using Thesis.Ver2.Lessons.FirstQuarterLessons.Sequence_and_Series.Lesson_3;
using Thesis.Ver2.Lessons.FirstQuarterLessons.Sequence_and_Series.Lesson1;
using Thesis.Ver2.Lessons.FirstQuarterLessons.Sequence_and_Series.Lesson2;

namespace Thesis.Ver2.Lessons.FirstQuarterLessons.Sequence_and_Series
{
    public partial class SequenceAndSeriesMain : UserControl
    {
        public SequenceAndSeriesMain()
        {
            InitializeComponent();
        }

        private void bluntBorderBtn1_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("Sequence1"))
            {
                Sequence1 S1 = new Sequence1();
                S1.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(S1);
            }
            Form1.Instance.PnlContainer.Controls["Sequence1"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
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

        private void bluntBorderBtn3_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("TermSequence1"))
            {
                TermSequence1 TS1 = new TermSequence1();
                TS1.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(TS1);
            }
            Form1.Instance.PnlContainer.Controls["TermSequence1"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }

        private void panel1_Paint(object sender, PaintEventArgs e)
        {

        }

        private void bluntBorderBtn4_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("FtntSequence"))
            {
                FtntSequence Ftnt1 = new FtntSequence();
                Ftnt1.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(Ftnt1);
            }
            Form1.Instance.PnlContainer.Controls["FtntSequence"].BringToFront();
            Form1.Instance.btnBack.Visible = false;

        }
    }
}
