using System;
using System.Collections.Generic;
using System.Drawing;
using System.Globalization;
using System.Text;
using System.Windows.Forms;

namespace LijaucoDentist
{
    public partial class CustomersEditUI : Form
    {
        Point lastClick;
        DatabaseUI parentUI;
        string id;

        public CustomersEditUI(DatabaseUI _parentUI, string _id)
        {
            InitializeComponent();
            parentUI = _parentUI;
            id = _id;
            labelID.Text = id;
            button1_Click(null, null);
            getDataInDatabase();
        }

        private void getDataInDatabase()
        {
            var result = Program.database.SELECT("PATIENTS", "ID='"+id+"'", null)[0];
            foreach (TabPage page in tabControl1.TabPages)
            {
                if (page.Text == "Information")
                {
                    foreach (Control cntrl in page.Controls)
                    {
                        if (cntrl is TextBox)
                        {
                            foreach (var v in result)
                            {
                                if (v.Key == Helper.Str.Replace(cntrl.Name, "textBox", ""))
                                {
                                    cntrl.Text = v.Value;
                                }
                            }
                        }
                    }
                }
                if (page.Text == "History")
                {
                    foreach (Control cntrl in page.Controls)
                    {
                        if (cntrl is TextBox)
                        {
                            foreach (var v in result)
                            {
                                if (v.Key == cntrl.Name)
                                {
                                    cntrl.Text = v.Value;
                                }
                            }
                        }
                        if (cntrl is Panel)
                        {
                            foreach (Control cntrl1 in ((Panel)cntrl).Controls)
                            {
                                if (cntrl1 is RadioButton)
                                {
                                    foreach (var v in result)
                                    {
                                        if (v.Key == cntrl.Name)
                                        {
                                            if (v.Value == cntrl1.Text)
                                            {
                                                ((RadioButton)cntrl1).Checked = true;
                                            }
                                        }
                                    }
                                }
                                if (cntrl1 is CheckBox)
                                {
                                    foreach (var v in result)
                                    {
                                        if (v.Key == cntrl.Name)
                                        {
                                            string[] bes = Helper.Str.Split(v.Value, new string[] { "|" });
                                            foreach (var v2 in bes)
                                            {
                                                if (((CheckBox)cntrl1).Text == v2)
                                                {
                                                    ((CheckBox)cntrl1).Checked = true;
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                        if (cntrl is CheckedListBox)
                        {
                            foreach (var v in result)
                            {
                                if (v.Key == cntrl.Name)
                                {
                                    string[] bes = Helper.Str.Split(v.Value, new string[] { "|" });
                                    foreach (var v2 in bes)
                                    {
                                        for (int i = 0; i < ((CheckedListBox)cntrl).Items.Count; i++)
                                        {
                                            if ((string)((CheckedListBox)cntrl).Items[i] == v2)
                                            {
                                                ((CheckedListBox)cntrl).SetItemChecked(i, true);
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
                if (page.Text == "Dental Record Chart")
                {
                    foreach (Control cntrl in page.Controls)
                    {
                        if (cntrl is TextBox)
                        {
                            string[] bes = Helper.Str.Split(result["Teeth"], new string[] { "|" });
                            foreach (var v in bes)
                            {
                                string[] teethValue = Helper.Str.Split(v, new string[] { "(", ")" });
                                if (cntrl.Name == teethValue[1])
                                {
                                    if (teethValue[0] == "none")
                                    {
                                        cntrl.Text = "";
                                    }
                                    else
                                    {
                                        cntrl.Text = teethValue[0];
                                    }
                                }
                            }
                        }
                    }
                }
            }
            Console.WriteLine(result["Birthday"]);
            try
            {
                textBoxBirthday.Text = DateTime.ParseExact(result["Birthday"], "MM/dd/yyyy", null).ToString();
            }
            catch
            {
                
            }
            textBoxAge.Text = result["Age"];
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

        private void buttonMinimize_Enter(object sender, EventArgs e)
        {
            labelTitle.Focus();
        }

        private void buttonSubmit_Enter(object sender, EventArgs e)
        {
            labelTitle.Focus();
        }

        private void buttonSubmit_Click(object sender, EventArgs e)
        {
            string txtBday = textBoxBirthday.Text;
            if (textBoxName.Text != "" && txtBday != "")
            {
                if (DateTime.TryParseExact(txtBday, "MM/dd/yyyy", null,
                           DateTimeStyles.None, out DateTime bdayResult) == true)
                {
                    string currentSeq = id;
                    List<string> columnNames = new List<string> { "ID" };
                    List<string> values = new List<string> { currentSeq };
                    foreach (TabPage page in tabControl1.TabPages)
                    {
                        if (page.Text == "Information")
                        {
                            foreach (Control cntrl in page.Controls)
                            {
                                if (cntrl is DateTimePicker)
                                {
                                    //Program.database.INSERT("PATIENTS", new string[] { "ID", Helper.Str.Replace(cntrl.Name, "textBox", "") },
                                    //new string[] { currentSeq, bdayResult.ToString("MM/dd/yyyy") });
                                    columnNames.Add(Helper.Str.Replace(cntrl.Name, "textBox", ""));
                                    values.Add(bdayResult.ToString("MM/dd/yyyy"));
                                    //Program.database.INSERT("PATIENTS", new string[] { "ID", "Age" },
                                    //  new string[] { currentSeq, (DateTime.Now.Year - bdayResult.Year).ToString() });
                                    columnNames.Add("Age");
                                    string dateToPut = (DateTime.Now.Year - bdayResult.Year).ToString();
                                    values.Add(dateToPut);
                                    textBoxAge.Text = dateToPut;
                                }
                                if (cntrl is TextBox)
                                {
                                    //Program.database.INSERT("PATIENTS", new string[] { "ID", Helper.Str.Replace(cntrl.Name, "textBox", "") },
                                    //  new string[] { currentSeq, cntrl.Text });
                                    if (cntrl.Name != "textBoxAge")
                                    {
                                        columnNames.Add(Helper.Str.Replace(cntrl.Name, "textBox", ""));
                                        values.Add(cntrl.Text);
                                    }
                                }
                            }
                        }
                        if (page.Text == "History")
                        {
                            foreach (Control cntrl in page.Controls)
                            {
                                if (cntrl is TextBox)
                                {
                                    //Program.database.INSERT("PATIENTS", new string[] { "ID", cntrl.Name },
                                    //  new string[] { currentSeq, cntrl.Text });
                                    columnNames.Add(cntrl.Name);
                                    values.Add(cntrl.Text);
                                }
                                if (cntrl is Panel)
                                {
                                    string modifiedChecks = "";
                                    bool isCheck = false;
                                    foreach (Control cntrl1 in ((Panel)cntrl).Controls)
                                    {
                                        if (cntrl1 is RadioButton)
                                        {
                                            if (((RadioButton)cntrl1).Checked == true)
                                            {
                                                //Program.database.INSERT("PATIENTS", new string[] { "ID", cntrl.Name },
                                                //  new string[] { currentSeq, cntrl1.Text });
                                                columnNames.Add(cntrl.Name);
                                                values.Add(cntrl1.Text);
                                            }
                                        }
                                        if (cntrl1 is CheckBox)
                                        {
                                            if (((CheckBox)cntrl1).Checked == true)
                                            {
                                                modifiedChecks += cntrl1.Text + "|";
                                            }
                                            isCheck = true;
                                        }
                                    }
                                    if (isCheck == true)
                                    {
                                        if (modifiedChecks != "")
                                        {
                                            modifiedChecks = modifiedChecks.Remove(modifiedChecks.Length - 1);
                                        }
                                        //Program.database.INSERT("PATIENTS", new string[] { "ID", cntrl.Name },
                                        //  new string[] { currentSeq, modifiedChecks });
                                        columnNames.Add(cntrl.Name);
                                        values.Add(modifiedChecks);
                                        isCheck = false;
                                    }
                                }
                                if (cntrl is CheckedListBox)
                                {
                                    string modifiedChecks = "";
                                    foreach (var v in ((CheckedListBox)cntrl).CheckedItems)
                                    {
                                        modifiedChecks += v.ToString() + "|";
                                    }
                                    if (modifiedChecks != "")
                                    {
                                        modifiedChecks = modifiedChecks.Remove(modifiedChecks.Length - 1);
                                    }
                                    //Program.database.INSERT("PATIENTS", new string[] { "ID", cntrl.Name },
                                    //  new string[] { currentSeq, modifiedChecks });
                                    columnNames.Add(cntrl.Name);
                                    values.Add(modifiedChecks);
                                }
                            }
                        }
                        if (page.Text == "Dental Record Chart")
                        {
                            string modifiedText = "";
                            StringBuilder sb = new StringBuilder();
                            foreach (Control cntrl in page.Controls)
                            {
                                if (cntrl is TextBox)
                                {
                                    if (cntrl.Text == "")
                                    {
                                        sb.Append("none(" + cntrl.Name + ")");
                                        sb.Append("|");
                                    }
                                    else
                                    {
                                        sb.Append(cntrl.Text + "(" + cntrl.Name + ")");
                                        sb.Append("|");
                                    }
                                }
                            }
                            modifiedText = sb.ToString();
                            modifiedText = modifiedText.Remove(modifiedText.Length - 1);
                            //Program.database.INSERT("PATIENTS", new string[] { "ID", "Teeth" },
                            //  new string[] { currentSeq, modifiedText });
                            columnNames.Add("Teeth");
                            values.Add(modifiedText);
                        }
                    }
                    Program.database.INSERT("PATIENTS", columnNames.ToArray(),
                      values.ToArray());
                    Helper.Msg.Information("Patient information successfully saved.", "Success");
                    parentUI.buttonSearch_Click(sender, e);
                }
                else
                {
                    Helper.Msg.Information("Invalid date format.", "Information");
                }
            }
            else
            {
                Helper.Msg.Information("Some required fields (*) are missing.", "Information");
            }
        }

        private void buttonBack_Click(object sender, EventArgs e)
        {
            this.Close();
        }

        private void createControl(string recordid, string date)
        {
            DentalRecordsControlUI f = new DentalRecordsControlUI(recordid, date, this);
            Helper.ThreadLib.ControlsAdd(this, flowLayoutPanel1, f);
        }

        public void button1_Click(object sender, EventArgs e)
        {
            labelTreatmentRecords.Text = Program.database.SELECT("RECORDS", "ID='" + id + "'", null).Count.ToString();
            var res = Program.database.SELECT("RECORDS", "ID='" + id + "' AND Date LIKE '%" + textBoxDate.Text + "%'", "RecordID DESC");
            Helper.ThreadLib.ControlsClear(this, flowLayoutPanel1);
            int i = 0;
            foreach (var v in res)
            {
                if (i < 100)
                {
                    createControl(v["RecordID"], v["Date"]);
                }
                else
                {
                    break;
                }
                i += 1;
            }
        }

        private void button2_Click(object sender, EventArgs e)
        {
            Form f = new ViewLegendsUI();
            f.Show();
        }

        private void textBoxBirthday_Leave(object sender, EventArgs e)
        {
            textBoxAge.Text = (DateTime.Now.Year - textBoxBirthday.Value.Year).ToString();
        }
    }
}
