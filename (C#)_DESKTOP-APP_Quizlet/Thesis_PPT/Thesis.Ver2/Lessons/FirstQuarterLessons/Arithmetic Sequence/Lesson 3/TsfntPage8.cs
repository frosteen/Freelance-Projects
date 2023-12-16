using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace Thesis.Ver2.Lessons.FirstQuarterLessons.Lesson_3
{
    public partial class TsfntPage8 : UserControl
    {
        public TsfntPage8()
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

        private void buttonBack_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("TsfntPage7"))
            {
                TsfntPage7 P7 = new TsfntPage7();
                P7.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(P7);
            }
            Form1.Instance.PnlContainer.Controls["TsfntPage7"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }

        private void buttonNext_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("TsfntPage8"))
            {
                TsfntPage8 P8 = new TsfntPage8();
                P8.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(P8);
            }
            Form1.Instance.PnlContainer.Controls["TsfntPage7"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }
    }
}
