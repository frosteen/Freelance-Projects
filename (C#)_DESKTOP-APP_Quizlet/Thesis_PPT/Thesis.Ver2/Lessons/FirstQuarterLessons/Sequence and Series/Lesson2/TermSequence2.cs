using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace Thesis.Ver2.Lessons.FirstQuarterLessons.Sequence_and_Series.Lesson2
{
    public partial class TermSequence2 : UserControl
    {
        public TermSequence2()
        {
            InitializeComponent();
        }

        private void TermSequence2_Load(object sender, EventArgs e)
        {

        }

        private void buttonBack_Click(object sender, EventArgs e)
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

        private void pictureBox1_Click(object sender, EventArgs e)
        {

        }

        private void label2_Click(object sender, EventArgs e)
        {

        }

        private void pictureBox2_Click(object sender, EventArgs e)
        {

        }

        private void panel5_Paint(object sender, PaintEventArgs e)
        {

        }

        private void panel6_Paint(object sender, PaintEventArgs e)
        {

        }

        private void label7_Click(object sender, EventArgs e)
        {

        }

        private void buttonNext_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("TermSequence3"))
            {
                TermSequence3 TS3 = new TermSequence3();
                TS3.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(TS3);
            }
            Form1.Instance.PnlContainer.Controls["TermSequence3"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }
    }
}
