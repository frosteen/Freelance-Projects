using System;
using System.Collections.Generic;
using System.Drawing;
using System.Globalization;
using System.Text;
using System.Windows.Forms;

namespace LijaucoDentist
{
    public partial class CustomersUI : Form
    {
        Point lastClick;
        DatabaseUI form;

        public CustomersUI(DatabaseUI _form)
        {
            InitializeComponent();
            form = _form;
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
                if (DateTime.TryParseExact(txtBday, "MM/dd/yyyy", CultureInfo.InvariantCulture,
                           DateTimeStyles.None, out DateTime bdayResult) == true)
                {
                    Console.WriteLine(bdayResult);
                    Program.database.INSERT("PATIENTS", new string[] { "Name" },
                        new string[] { "nameCreated" });
                    string currentSeq = Program.database.SELECT("sqlite_sequence", "name='PATIENTS'", null)[0]["seq"].ToString();
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
                                    Console.WriteLine((DateTime.Now.Year - bdayResult.Year).ToString());
                                    values.Add((DateTime.Now.Year - bdayResult.Year).ToString());
                                }
                                if (cntrl is TextBox)
                                {
                                    //Program.database.INSERT("PATIENTS", new string[] { "ID", Helper.Str.Replace(cntrl.Name, "textBox", "") },
                                    //  new string[] { currentSeq, cntrl.Text });
                                    columnNames.Add(Helper.Str.Replace(cntrl.Name, "textBox", ""));
                                    values.Add(cntrl.Text);
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
                                        sb.Append("none("+cntrl.Name+")");
                                        sb.Append("|");
                                    }
                                    else
                                    {
                                        sb.Append(cntrl.Text+ "(" + cntrl.Name + ")");
                                        sb.Append( "|");
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
                    Helper.Msg.Information("Patient information successfully registered.", "Success");
                    this.Close();
                    form.buttonSearch_Click(sender, e);
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

        private void buttonNext_Click(object sender, EventArgs e)
        {
            tabControl1.SelectedIndex += 1;
        }

        private void tabControl1_Selecting(object sender, TabControlCancelEventArgs e)
        {
            if (tabControl1.SelectedIndex == tabControl1.TabCount-1)
            {
                buttonSubmit.Visible = true;
                buttonNext.Visible = false;
            }
            else
            {
                buttonSubmit.Visible = false;
                buttonNext.Visible = true;
            }
        }

        private void button1_Click(object sender, EventArgs e)
        {
            Form f = new ViewLegendsUI();
            f.Show();
        }
    }
}
