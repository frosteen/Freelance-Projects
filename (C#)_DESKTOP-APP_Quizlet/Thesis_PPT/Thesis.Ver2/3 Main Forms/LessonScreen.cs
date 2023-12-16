using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;
using Thesis.Ver2.Lessons;

namespace Thesis.Ver2._3_Main_Forms
{
    public partial class LessonScreen : UserControl
    {
        public LessonScreen()
        {
            InitializeComponent();
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

        private void LessonScreen_Load(object sender, EventArgs e)
        {

        }

        private void bluntBorderBtn4_Click(object sender, EventArgs e)
        {

        }
    }
}
