using System;
using System.Collections.Generic;
using System.Drawing;
using System.Windows.Forms;

namespace LijaucoDentist
{
    public partial class CategoryEditUI : Form
    {
        Point lastClick;
        string recordid;
        CustomersEditUI parentUI;
        Dictionary<string, string> recordData;
        string date;
        public CategoryEditUI(string _recordid, string _date, CustomersEditUI _parentUI)
        {
            InitializeComponent();
            recordid = _recordid;
            labelRecordID.Text = recordid;
            parentUI = _parentUI;
            date = _date;
            recordData = Program.database.SELECT("RECORDS", "RecordID='"+_recordid+"'", null)[0];
            textBoxDate.Text = DateTime.ParseExact(recordData["Date"], "MM/dd/yyyy", null).ToString();
            foreach (Control cntrl1 in panel1.Controls)
            {
                if (cntrl1 is GroupBox)
                {
                    foreach (Control cntrl2 in cntrl1.Controls)
                    {
                        if (cntrl2 is RadioButton)
                        {
                            foreach (var v in recordData)
                            {
                                if (v.Value.ToString() == cntrl2.Text.ToString())
                                {
                                    ((RadioButton)cntrl2).Checked = true;
                                }
                            }
                        }
                        if (cntrl2 is CheckBox)
                        {
                            foreach (var v in recordData)
                            {
                                string[] valuesNeedToBeChecked = Helper.Str.Split(v.Value, new string[] { "|" });
                                foreach (string v2 in valuesNeedToBeChecked)
                                {
                                    if (cntrl2.Text == v2)
                                    {
                                        ((CheckBox)cntrl2).Checked = true;
                                    }
                                }
                            }
                        }
                        if (cntrl2 is TextBox)
                        {
                            foreach (var v in recordData)
                            {
                                if ((Helper.Str.Replace(cntrl1.Text, " ", "") + "ToothNo") == v.Key)
                                {
                                    cntrl2.Text = recordData[Helper.Str.Replace(cntrl1.Text, " ", "")+"ToothNo"];
                                }
                            }
                        }
                    }
                }
            }
            AmountCharged.Text = recordData["AmountCharged"];
            AmountPaid.Text = recordData["AmountPaid"];
            try
            {
                if ((Decimal.Parse(AmountCharged.Text) - Decimal.Parse(AmountPaid.Text)) != 0)
                {
                    labelBalancePhp.Visible = true;
                    Balance.Visible = true;
                    Balance.Text = ((Decimal.Parse(AmountCharged.Text)) - Decimal.Parse(AmountPaid.Text)).ToString("F");
                }
                else
                {
                    labelBalancePhp.Visible = false;
                    Balance.Visible = false;
                    Balance.Text = 0.ToString("F");
                }
            }
            catch (Exception e)
            {
                Console.WriteLine("Amount charged and Amount paid can't be found: " + e.Message);
            }
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

        private void buttonBack_Click(object sender, EventArgs e)
        {
            this.Close();
        }

        private void buttonRecord_Click(object sender, EventArgs e)
        {
            if (AmountCharged.Text != "" && AmountPaid.Text != "")
            {
                if (decimal.TryParse(AmountCharged.Text, out decimal amountCharged) &&
                    decimal.TryParse(AmountPaid.Text, out decimal amountPaid))
                {
                    if (amountCharged >=0 && amountPaid >= 0)
                    {
                        if (amountCharged >= amountPaid)
                        {
                            List<string> columnNames = new List<string> { "RecordID" };
                            List<string> values = new List<string> { recordid };
                            foreach (Control cntrl1 in panel1.Controls)
                            {
                                if (cntrl1 is GroupBox)
                                {
                                    string modifiedChecks = "";
                                    bool isCheck = false;
                                    foreach (Control cntrl2 in cntrl1.Controls)
                                    {
                                        if (cntrl2 is CheckBox)
                                        {
                                            if (((CheckBox)cntrl2).Checked == true)
                                            {
                                                modifiedChecks += cntrl2.Text + "|";
                                            }
                                            isCheck = true;
                                        }
                                        if (cntrl2 is RadioButton)
                                        {
                                            if (((RadioButton)cntrl2).Checked == true)
                                            {
                                                //Program.database.INSERT("RECORDS", new string[] { "RecordID", "ID", Helper.Str.Replace(cntrl1.Text, " ", "") },
                                                //new string[] { currentSeq, id, cntrl2.Text });
                                                columnNames.Add(Helper.Str.Replace(cntrl1.Text, " ", ""));
                                                values.Add(cntrl2.Text);
                                            }
                                        }
                                        if (cntrl2 is TextBox)
                                        {
                                            if (((TextBox)cntrl2).Text != "")
                                            {
                                                //   Program.database.INSERT("RECORDS", new string[] { "RecordID", "ID", Helper.Str.Replace(cntrl1.Text, " ", "") + "ToothNo" },
                                                // new string[] { currentSeq, id, cntrl2.Text });
                                                columnNames.Add(Helper.Str.Replace(cntrl1.Text, " ", "") + "ToothNo");
                                                values.Add(cntrl2.Text);
                                            }
                                        }
                                    }
                                    if (isCheck == true)
                                    {
                                        if (modifiedChecks != "")
                                        {
                                            modifiedChecks = modifiedChecks.Remove(modifiedChecks.Length - 1);
                                        }
                                        //Program.database.INSERT("RECORDS", new string[] { "RecordID", "ID", Helper.Str.Replace(cntrl1.Text, " ", "") },
                                        //new string[] { currentSeq, id, modifiedChecks });
                                        columnNames.Add(Helper.Str.Replace(cntrl1.Text, " ", ""));
                                        values.Add(modifiedChecks);
                                        isCheck = false;
                                    }
                                }
                            }
                            //PAYMENTS//
                            //Program.database.INSERT("RECORDS", new string[] { "RecordID", "ID", "AmountCharged", "AmountPaid" },
                            //new string[] { currentSeq, id, amountCharged.ToString(), amountPaid.ToString() });
                            columnNames.Add("AmountCharged");
                            columnNames.Add("AmountPaid");
                            values.Add(amountCharged.ToString("F"));
                            values.Add(amountPaid.ToString("F"));
                            if ((amountCharged - amountPaid) != 0)
                            {
                                labelBalancePhp.Visible = true;
                                Balance.Visible = true;
                                Balance.Text = (amountCharged - amountPaid).ToString("F");
                            }
                            else
                            {
                                labelBalancePhp.Visible = false;
                                Balance.Visible = false;
                                Balance.Text = 0.ToString("F");
                            }
                            //Program.database.INSERT("RECORDS", new string[] { "RecordID", "ID", "Balance" },
                            //new string[] { currentSeq, id, Decimal.Parse(Balance.Text).ToString() });
                            columnNames.Add("Balance");
                            values.Add(Decimal.Parse(Balance.Text).ToString("F"));
                            columnNames.Add("Date");
                            values.Add(textBoxDate.Value.ToString("MM/dd/yyyy"));
                            Program.database.INSERT("RECORDS", columnNames.ToArray(), values.ToArray());
                            parentUI.button1_Click(sender, e);
                            Helper.Msg.Information("Dental record of the patient successfully saved.", "Success");
                        }
                        else
                        {
                            Helper.Msg.Information("Amount paid shouldn't be greater than the amount charged.", "Information");
                        }
                    }
                    else
                    {
                        Helper.Msg.Information("Payments shouldn't be negative.", "Information");
                    }
                }
                else
                {
                    Helper.Msg.Information("Amount should be in decimal.", "Money Information");
                }
            }
            else
            {
                Helper.Msg.Information("Some amount fields are empty.", "Information");
            }
        }

        private void buttonNote_Click(object sender, EventArgs e)
        {
            recordData = Program.database.SELECT("RECORDS", "RecordID='" + recordid + "'", null)[0];
            this.Opacity = LoginUI.opacity;
            Form f = new NoteUI(this, recordData["Notes"].ToString(), recordid);
            f.ShowDialog();
            this.Opacity = 1;
        }

        private void radioButton40_CheckedChanged(object sender, EventArgs e)
        {

        }

        private void CategoryEditUI_Load(object sender, EventArgs e)
        {
        }
    }
}
