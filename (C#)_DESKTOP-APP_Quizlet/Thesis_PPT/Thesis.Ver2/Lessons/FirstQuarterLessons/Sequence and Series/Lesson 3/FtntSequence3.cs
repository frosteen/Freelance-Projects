using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace Thesis.Ver2.Lessons.FirstQuarterLessons.Sequence_and_Series.Lesson_3
{
    public partial class FtntSequence3 : UserControl
    {
        public FtntSequence3()
        {
            InitializeComponent();
        }

        private void buttonBack_Click(object sender, EventArgs e)
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

        private void label2_Click(object sender, EventArgs e)
        {

        }

        private void pictureBox1_Click(object sender, EventArgs e)
        {

        }

        private void label3_Click(object sender, EventArgs e)
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

        private void FtntSequence3_Load(object sender, EventArgs e)
        {

        }
    }
}
