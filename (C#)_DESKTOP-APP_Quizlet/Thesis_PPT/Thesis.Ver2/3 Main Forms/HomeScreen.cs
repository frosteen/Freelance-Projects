using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace Thesis.Ver2._3_Main_Forms
{
    public partial class HomeScreen : UserControl
    {
        public HomeScreen()
        {
            InitializeComponent();
        }

        private void button4_Click(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {

        }

        private void label2_Click(object sender, EventArgs e)
        {

        }

        private void LessonBtn_Click_1(object sender, EventArgs e)
        {
            if(!Form1.Instance.PnlContainer.Controls.ContainsKey("LessonScreen"))
            {
                LessonScreen LS = new LessonScreen();
                LS.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(LS);
            }
            Form1.Instance.PnlContainer.Controls["LessonScreen"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }

        private void panel1_Paint(object sender, PaintEventArgs e)
        {

        }

        private void HomeScreen_Load(object sender, EventArgs e)
        {

        }
    }
}
