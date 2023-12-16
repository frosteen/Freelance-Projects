using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace Thesis.Ver2.Lessons.FirstQuarterLessons.Sequence_and_Series.Lesson_3
{
    public partial class FtntSequence2 : UserControl
    {
        public FtntSequence2()
        {
            InitializeComponent();
        }

        private void label4_Click(object sender, EventArgs e)
        {

        }

        private void buttonBack_Click(object sender, EventArgs e)
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

        private void label5_Click(object sender, EventArgs e)
        {

        }

        private void label7_Click(object sender, EventArgs e)
        {

        }

        private void panel1_Paint(object sender, PaintEventArgs e)
        {

        }

        private void label9_Click(object sender, EventArgs e)
        {

        }

        private void buttonNext_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("FtntSequence3"))
            {
                FtntSequence3 Ftnt3 = new FtntSequence3();
                Ftnt3.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(Ftnt3);
            }
            Form1.Instance.PnlContainer.Controls["FtntSequence3"].BringToFront();
            Form1.Instance.btnBack.Visible = false;

        }
    }
}
