using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;
using Thesis.Ver2.Lessons.FirstQuarterLessons.Sequence_and_Series.Lesson_3;

namespace Thesis.Ver2.Lessons.FirstQuarterLessons.Sequence_and_Series.Lesson2
{
    public partial class TermSequence3 : UserControl
    {
        public TermSequence3()
        {
            InitializeComponent();
        }

        private void pictureBox8_Click(object sender, EventArgs e)
        {

        }

        private void buttonBack_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("TermSequence2"))
            {
                TermSequence2 TS2= new TermSequence2();
                TS2.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(TS2);
            }
            Form1.Instance.PnlContainer.Controls["TermSequence2"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
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

        private void bluntBorderBtn2_Click(object sender, EventArgs e)
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

        private void bluntBorderBtn2_Click_1(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("FtntSequence"))
            {
                FtntSequence Ftnt = new FtntSequence();
                Ftnt.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(Ftnt);
            }
            Form1.Instance.PnlContainer.Controls["FtntSequence"].BringToFront();
            Form1.Instance.btnBack.Visible = false;

        }
    }
}
