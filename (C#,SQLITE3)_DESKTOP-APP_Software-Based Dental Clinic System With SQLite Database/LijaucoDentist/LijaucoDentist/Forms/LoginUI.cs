using Helper;
using System;
using System.Drawing;
using System.Media;
using System.Windows.Forms;

namespace LijaucoDentist
{
    public partial class LoginUI : Form
    {
        public static double opacity = 0;
        bool access = false;
        Form UI;
        Point lastClick;

        public LoginUI(Form _UI, bool _access)
        {
            InitializeComponent();
            UI = _UI;
            for (int i = Application.OpenForms.Count - 1; i >= 0; i--)
            {
                Application.OpenForms[i].Opacity = opacity;
            }
            access = _access;
        }

        //PANEL CONFIGURATIONS
        private void buttonClose_Click(object sender, EventArgs e)
        {
            this.Close();
        }

        private void buttonMinimize_Click(object sender, EventArgs e)
        {
            this.WindowState = FormWindowState.Minimized;
        }

        private void panelTitle_MouseDown(object sender, MouseEventArgs e)
        {
            lastClick = e.Location;
        }

        private void panelTitle_MouseMove(object sender, MouseEventArgs e)
        {
            if (e.Button == MouseButtons.Left)
            {
                this.Left += e.X - lastClick.X;
                this.Top += e.Y - lastClick.Y;
            }
        }

        int attempts = 2;

        private void buttonLogin_Click(object sender, EventArgs e)
        {
            if (textBoxUsername.Text != "" && textBoxPassword.Text != "")
            {
                string username = Program.database.SELECT("AUTHENTICATION", "Type='Username'", null)[0]["Value"];
                string password = Program.database.SELECT("AUTHENTICATION", "Type='Password'", null)[0]["Value"];
                if (username.ToString() == textBoxUsername.Text.ToString()
                    && password.ToString() == textBoxPassword.Text.ToString())
                {
                    if (access)
                    {
                        Application.Exit();
                        System.Threading.ThreadStart tref = new System.Threading.ThreadStart(() => {
                            Application.Run(UI);
                        });
                        System.Threading.Thread t = new System.Threading.Thread(tref);
                        t.SetApartmentState(System.Threading.ApartmentState.STA);
                        t.Start();
                    }
                    else
                    {
                        for (int i = Application.OpenForms.Count - 1; i >= 0; i--)
                        {
                            Application.OpenForms[i].Opacity = 0;
                        }
                        Form form = new SettingsUI(UI);
                        form.Location = new Point(UI.Location.X + UI.Width / 2 - form.Width / 2, UI.Location.Y + UI.Height);
                        form.ShowDialog();
                        this.Close();
                    }
                }
                else
                {
                    if (attempts != 0)
                    {
                        new System.Threading.Thread(() => {
                            ThreadLib.SetProperty(this, labelNotes, "Text", "*Wrong username and password.\n*You have " + attempts + " attempt/s.");
                            ThreadLib.SetProperty(this, labelNotes, "Visible", true);
                            ThreadLib.SetProperty(this, textBoxUsername, "Text", "");
                            ThreadLib.SetProperty(this, textBoxPassword, "Text", "");
                            attempts -= 1;
                            System.Threading.Thread.Sleep(5000);
                            ThreadLib.SetProperty(this, labelNotes, "Visible", false);
                        }).Start();
                    }
                    else
                    {
                        new System.Threading.Thread(() => {
                            for (int i = 10; i > 0; i--)
                            {
                                ThreadLib.SetProperty(this, buttonLogin, "Visible", false);
                                ThreadLib.SetProperty(this, labelNotes, "Visible", true);
                                ThreadLib.SetProperty(this, labelNotes, "Text", 
                                    "*Password attempts have exceeded.\n*Closing application in " + i + "s");
                                System.Threading.Thread.Sleep(1000);
                            }
                            Application.Exit();
                        }).Start();
                    }
                }
            }
            else
            {
                new System.Threading.Thread(() => {
                    ThreadLib.SetProperty(this, labelNotes, "Text", "*Some fields are empty.");
                    ThreadLib.SetProperty(this, labelNotes, "Visible", true);
                    System.Threading.Thread.Sleep(2000);
                    ThreadLib.SetProperty(this, labelNotes, "Visible", false);
                }).Start();
            }
        }

        private void textBoxPassword_Enter(object sender, EventArgs e)
        {
            this.textBoxPassword.Clear();
        }

        private void buttonLogin_Enter(object sender, EventArgs e)
        {
            labelTitle.Focus();
        }

        private void LoginUI_FormClosed(object sender, FormClosedEventArgs e)
        {
            for (int i = Application.OpenForms.Count - 1; i >= 0; i--)
            {
                Application.OpenForms[i].Opacity = 1;
            }
        }

        private void buttonMinimize_Enter(object sender, EventArgs e)
        {
            labelTitle.Focus();
        }
    }
}
