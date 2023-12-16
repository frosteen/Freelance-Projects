using System;
using System.Drawing;
using System.Windows.Forms;

namespace LijaucoDentist
{
    public partial class DatabaseUI : Form
    {
        Point lastClick;
        Form parentForm;

        public DatabaseUI(Form _parentForm)
        {
            InitializeComponent();
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

        private void buttonBack_Click(object sender, EventArgs e)
        {
            labelTitle.Focus();
            this.Close();
        }

        private void SettingsUI_FormClosed(object sender, FormClosedEventArgs e)
        {
            parentForm.Opacity = 1;
        }

        private void buttonBack_Enter(object sender, EventArgs e)
        {
            labelTitle.Focus();
        }

        private void createControl(string id, string name, string age)
        {
            PatientsControlUI f = new PatientsControlUI(id, name, age, this);
            Helper.ThreadLib.ControlsAdd(this, panelPatients, f);
        }

        public async void buttonSearch_Click(object sender, EventArgs e)
        {
            try
            {
                labelPatients.Text = Program.database.SELECT("PATIENTS", null, "ID DESC").Count.ToString();
                var res = Program.database.SELECT("PATIENTS", "Name LIKE '%" + textBoxSearch.Text + "%'", "ID DESC");
                buttonSearch.Visible = false;
                textBoxSearch.Enabled = false;
                pictureBoxLoading.Visible = true;
                pictureBoxLoading.BringToFront();
                await System.Threading.Tasks.Task.Run(() => {
                    Helper.ThreadLib.ControlsClear(this, panelPatients);
                    int cntr = 0;
                    foreach (var v in res)
                    {
                        if (cntr < 50)
                        {
                            createControl(v["ID"], v["Name"], v["Age"]);
                            cntr += 1;
                        }
                        else
                        {
                            break;
                        }
                        System.Threading.Thread.Sleep(10);
                    }
                });
                pictureBoxLoading.Visible = false;
                textBoxSearch.Enabled = true;
                buttonSearch.Visible = true;
            }
            catch
            {

            }
        }

        private void buttonRegister_Click(object sender, EventArgs e)
        {
            this.Opacity = LoginUI.opacity;
            new CustomersUI(this).ShowDialog();
            this.Opacity = 1;
        }

        private void DatabaseUI_Load(object sender, EventArgs e)
        {
            buttonSearch_Click(sender, e);
        }

        private void label2_Click(object sender, EventArgs e)
        {

        }
    }
}
