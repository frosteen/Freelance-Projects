using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace Thesis.Ver2.Lessons.FirstQuarterLessons.Sequence_and_Series.Lesson1
{
    public partial class Sequence2 : UserControl
    {
        public Sequence2()
        {
            InitializeComponent();
        }

        private void Sequence2_Load(object sender, EventArgs e)
        {

        }

        private void pictureBox1_Click(object sender, EventArgs e)
        {

        }

        private void buttonBack_Click(object sender, EventArgs e)
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

        private void pictureBox2_Click(object sender, EventArgs e)
        {
            
        }

        private void label3_Click(object sender, EventArgs e)
        {

        }

        private void buttonNext_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("Sequence3"))
            {
                Sequence3 S3 = new Sequence3();
                S3.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(S3);
            }
            Form1.Instance.PnlContainer.Controls["Sequence3"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }
    }
}
