using System;
using System.Drawing;
using System.IO;
using System.Windows.Forms;
using Helper;

namespace LijaucoDentist
{
    public partial class SettingsUI : Form
    {
        Point lastClick;
        Form parentForm;

        public SettingsUI(Form _parentForm)
        {
            InitializeComponent();

            string username = Program.database.SELECT("AUTHENTICATION", "Type='Username'", null)[0]["Value"];
            string password = Program.database.SELECT("AUTHENTICATION","Type='Password'", null)[0]["Value"];
            textBoxUsername.Text = username;
            textBoxPassword.Text = password;
            parentForm = _parentForm;
            parentForm.Opacity = 0;
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

        private void buttonMinimize_Click(object sender, EventArgs e)
        {
            this.WindowState = FormWindowState.Minimized;
        }

        private void buttonClose_Click(object sender, EventArgs e)
        {
            Application.Exit();
        }

        private void buttonSave_Click(object sender, EventArgs e)
        {
            if (textBoxUsername.Text != ""
                && textBoxPassword.Text != "")
            {
                Program.database.INSERT("AUTHENTICATION", new string[] { "Type", "Value" },
                    new string[] { "Username", textBoxUsername.Text });
                Program.database.INSERT("AUTHENTICATION", new string[] { "Type", "Value" },
                    new string[] { "Password", textBoxPassword.Text });
                ThreadLib.Create(()=> {
                    ThreadLib.SetProperty(this, labelNotes, "Text", "*Password changed\nsuccessfully.");
                    ThreadLib.SetProperty(this, labelNotes, "Visible", true);
                    System.Threading.Thread.Sleep(2000);
                    ThreadLib.SetProperty(this, labelNotes, "Visible", false);
                });
            }
            else
            {
                ThreadLib.Create(() => {
                    ThreadLib.SetProperty(this, labelNotes, "Text", "*Some fields are missing.");
                    ThreadLib.SetProperty(this, labelNotes, "Visible", true);
                    System.Threading.Thread.Sleep(2000);
                    ThreadLib.SetProperty(this, labelNotes, "Visible", false);
                });
            }
        }

        private void buttonBack_Click(object sender, EventArgs e)
        {
            labelTitle.Focus();
            this.Close();
        }

        private void SettingsUI_FormClosed(object sender, FormClosedEventArgs e)
        {
            parentForm.Opacity = 1;
        }

        private void buttonSave_Enter(object sender, EventArgs e)
        {
            labelTitle.Focus();
        }

        private void buttonMinimize_Enter(object sender, EventArgs e)
        {
            labelTitle.Focus();
        }

        private void buttonReset_Click(object sender, EventArgs e)
        {

        }
    }
}
