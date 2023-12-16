using System;
using System.Windows.Forms;

namespace LijaucoDentist
{
    public partial class PatientsControlUI : UserControl
    {
        DatabaseUI oldUI;
        public PatientsControlUI(string id, string name, string age, DatabaseUI f)
        {
            InitializeComponent();
            labelID.Text = id;
            labelName.Text = name;
            //labelAge.Text = age;
            oldUI = f;
        }

        private void button1_Enter(object sender, EventArgs e)
        {
            label1.Focus();
        }

        private void button2_Click(object sender, EventArgs e)
        {
            if (Helper.Msg.Question("Are you sure you want to delete this patient information? This will also delete all the treatment records.", "Information") == DialogResult.Yes)
            {
                Program.database.DELETE("PATIENTS", "ID=" + labelID.Text);
                Program.database.DELETE("RECORDS", "ID=" + labelID.Text);
                oldUI.buttonSearch_Click(sender, e);
            }
        }

        private void buttonEdit_Click(object sender, EventArgs e)
        {
            Form f = new CustomersEditUI(oldUI, labelID.Text);
            oldUI.Opacity = LoginUI.opacity;
            f.ShowDialog();
            oldUI.Opacity = 1;
        }

        private void buttonNEW_Click(object sender, EventArgs e)
        {
            if (Helper.Msg.Question("Are you sure you want to create a new dental record?", "Information") == DialogResult.Yes)
            {
                Program.database.INSERT("RECORDS",
                    new string[] { "ID", "Date", "AmountCharged", "AmountPaid", "Balance" },
                    new string[] { labelID.Text, DateTime.Now.ToString("MM/dd/yyyy"), "NONE", "NONE", "0" });
                string currentSeq = Program.database.SELECT("sqlite_sequence", "name='RECORDS'", null)[0]["seq"].ToString();
                Form f = new CategoryUI(labelID.Text, currentSeq);
                oldUI.Opacity = LoginUI.opacity;
                f.ShowDialog();
                oldUI.Opacity = 1;
            }
        }
    }
}
