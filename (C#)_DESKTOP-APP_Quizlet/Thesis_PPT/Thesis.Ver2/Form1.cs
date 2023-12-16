using System;
using System.Windows.Forms;
using System.Runtime.InteropServices;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Thesis.Ver2._3_Main_Forms;

// Required library for QuestionScreen
using Thesis.Ver2.QuestionScreen;

namespace Thesis.Ver2
{
    public partial class Form1 : Form
    {
       

        static Form1 _obj;
        private bool mouseDown;
        private Point lastLocation;

        public static Form1 Instance
        {
            get
            {
                if(_obj == null)
                {
                    _obj = new Form1();
                }
                return _obj;
            }


        }


        public Panel PnlContainer
        {
            get { return PanelContainer; }
            set { PanelContainer = value; }
        }

        public Button btnBack
        {
            get { return BackButton; }
            set { BackButton = value; }
        }

        public Form1()
        {          
            InitializeComponent();
           

            
        }


        private void tableLayoutPanel1_Paint(object sender, PaintEventArgs e)
        {

        }

        private void Form1_Load(object sender, EventArgs e)
        {
            BackButton.Visible = false;
            _obj = this;

            HomeScreen HS = new HomeScreen();
            HS.Dock = DockStyle.Fill;
            PanelContainer.Controls.Add(HS);
        }

        private void BackButton_Click(object sender, EventArgs e)
        {
            PanelContainer.Controls["HomeScreen"].BringToFront();
            BackButton.Visible = false;
        }

        private void HomeBtn_Click(object sender, EventArgs e)
        {
            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("HomeScreen"))
            {
                HomeScreen HS = new HomeScreen();
                HS.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(HS);
            }
            Form1.Instance.PnlContainer.Controls["HomeScreen"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }

        private void pictureBox1_Click(object sender, EventArgs e)
        {

        }

        private void LessonBtn_Click(object sender, EventArgs e)
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

        private void ChallengeBtn_Click(object sender, EventArgs e)
        {

            if (!Form1.Instance.PnlContainer.Controls.ContainsKey("ChallengeScreen"))
            {
                QuestionBank qs = new QuestionBank("Geometric Sequence");
                QuestionScreen.QuestionScreen CS = new QuestionScreen.QuestionScreen(qs);
                CS.Dock = DockStyle.Fill;
                Form1.Instance.PnlContainer.Controls.Add(CS);
            }
            Form1.Instance.PnlContainer.Controls["ChallengeScreen"].BringToFront();
            Form1.Instance.btnBack.Visible = false;
        }

        private void panel1_Paint(object sender, PaintEventArgs e)
        {

        }

        private void PanelContainer_Paint(object sender, PaintEventArgs e)
        {

        }

        private void bluntBorderBtn1_Click(object sender, EventArgs e)
        {
            this.Close();

        }

        private void Form1_FormClosing(object sender, FormClosingEventArgs e)
        {
            if (e.CloseReason == CloseReason.UserClosing)
            {
                DialogResult result = MessageBox.Show("Do you really want to exit?", "Dialog Title", MessageBoxButtons.YesNo);
                if (result == DialogResult.Yes)
                {
                    Environment.Exit(0);
                }
                else
                {
                    e.Cancel = true;
                }
            }
            else
            {
                e.Cancel = true;
            }
        }

        private void bluntBorderBtn2_Click(object sender, EventArgs e)
        {
            if (this.WindowState == FormWindowState.Normal)
            {
                this.WindowState = FormWindowState.Maximized;
            }
            else
            {
                this.WindowState = FormWindowState.Normal;
            }
        }

        private void bluntBorderBtn3_Click(object sender, EventArgs e)
        {
            WindowState = FormWindowState.Minimized;
        }

        private void Form1_MouseDown(object sender, MouseEventArgs e)
        {
            if (e.Button == MouseButtons.Left)
            {
                mouseDown = true;
                lastLocation = e.Location;
            }
        }

        private void Form1_MouseMove(object sender, MouseEventArgs e)
        {
            if (mouseDown)
            {
                this.Location = new Point(
                    (this.Location.X - lastLocation.X) + e.X, (this.Location.Y - lastLocation.Y) + e.Y);

                this.Update();
            }
        }

        private void Form1_MouseUp(object sender, MouseEventArgs e)
        {
            mouseDown = false;
        }

        private void panel1_MouseDown(object sender, MouseEventArgs e)
        {
            if (e.Button == MouseButtons.Left)
            {
                mouseDown = true;
                lastLocation = e.Location;
            }
        }

        private void panel1_MouseMove(object sender, MouseEventArgs e)
        {
            if (mouseDown)
            {
                this.Location = new Point(
                    (this.Location.X - lastLocation.X) + e.X, (this.Location.Y - lastLocation.Y) + e.Y);

                this.Update();
            }
        }

        private void panel1_MouseUp(object sender, MouseEventArgs e)
        {
            mouseDown = false;
        }

     
    }

   
}
