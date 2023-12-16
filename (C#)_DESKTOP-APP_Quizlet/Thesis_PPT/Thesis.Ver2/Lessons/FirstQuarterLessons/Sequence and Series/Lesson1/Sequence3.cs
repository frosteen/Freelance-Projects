using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;
using Thesis.Ver2.Lessons.FirstQuarterLessons.Sequence_and_Series.Lesson2;

namespace Thesis.Ver2.Lessons.FirstQuarterLessons.Sequence_and_Series.Lesson1
{
    public partial class Sequence3 : UserControl
    {
        public Sequence3()
        {
            InitializeComponent();
        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void buttonBack_Click(object sender, EventArgs e)
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

        private void pictureBox1_Click(object sender, EventArgs e)
        {

        }

        private void label4_Click(object sender, EventArgs e)
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

        private void bluntBorderBtn2_Click(object sender, EventArgs e)
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
    }
}
