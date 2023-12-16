using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;
using Thesis.Ver2._3_Main_Forms;
using Thesis.Ver2.Lessons.FirstQuarterLessons.Arithmetic_Sequence;
using Thesis.Ver2.Lessons.FirstQuarterLessons.Geometric_Sequence;
using Thesis.Ver2.Lessons.FirstQuarterLessons.Lesson_3;
using Thesis.Ver2.Lessons.FirstQuarterLessons.Lesson1;
using Thesis.Ver2.Lessons.FirstQuarterLessons.Lesson2;
using Thesis.Ver2.Lessons.FirstQuarterLessons.Polynomials;
using Thesis.Ver2.Lessons.FirstQuarterLessons.Sequence_and_Series;

namespace Thesis.Ver2.Lessons
{
    public partial class FirstQuarter : UserControl
    {

        


        public FirstQuarter()
        {
            InitializeComponent();
        }

        private void FirstQuarter_Load(object sender, EventArgs e)
        {
            
        }

        private void bluntBorderBtn8_Click(object sender, EventArgs e)
        {

        }

        private void buttonBack_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("LessonScreen"))
            {
                LessonScreen LS = new LessonScreen();
                LS.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(LS);
            }
            Form1.Instance.PnlContainer.Controls["LessonScreen"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }

        private void bluntBorderBtn1_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("ArithmeticMain"))
            {
                ArithmeticMain AM = new ArithmeticMain();
                AM.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(AM);
            }
            Form1.Instance.PnlContainer.Controls["ArithmeticMain"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }

        

        private void bluntBorderBtn6_Click(object sender, EventArgs e)
        {

        }

        private void bluntBorderBtn3_Click(object sender, EventArgs e)
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

        private void bluntBorderBtn4_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("GeometricSequenceMain"))
            {
                GeometricSequenceMain GeoSmain = new GeometricSequenceMain();
                GeoSmain.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(GeoSmain);
            }
            Form1.Instance.PnlContainer.Controls["GeometricSequenceMain"].BringToFront();
            Form1.Instance.btnBack.Visible = false;

        }

        private void bluntBorderBtn5_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("Polynomialsmain"))
            {
                Polynomialsmain SPmain = new Polynomialsmain();
                SPmain.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(SPmain);
            }
            Form1.Instance.PnlContainer.Controls["Polynomialsmain"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }
    }
}
