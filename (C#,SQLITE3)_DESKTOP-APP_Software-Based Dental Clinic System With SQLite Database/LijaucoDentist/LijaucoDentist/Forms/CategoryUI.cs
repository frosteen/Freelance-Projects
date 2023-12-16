using System;
using System.Collections.Generic;
using System.Drawing;
using System.Windows.Forms;

namespace LijaucoDentist
{
    public partial class CategoryUI : Form
    {
        Point lastClick;
        string id;
        string currentSeq;
        public CategoryUI(string _id, string _currentSeq)
        {
            InitializeComponent();
            id = _id;
            currentSeq = _currentSeq;
            labelRecordID.Text = currentSeq;
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
                    if (amountCharged >= 0 && amountPaid >= 0)
                    {
                        if (amountCharged >= amountPaid)
                        {
                            List<string> columnNames = new List<string> { "RecordID", "ID" };
                            List<string> values = new List<string> { currentSeq, id };
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
                                                isCheck = true;
                                            }
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
                            Program.database.INSERT("RECORDS", columnNames.ToArray(), values.ToArray());
                            Helper.Msg.Information("Dental record of the patient successfully updated.", "Success");
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
            this.Opacity = LoginUI.opacity;
            Form f = new NoteUI(this, null, currentSeq);
            f.ShowDialog();
            this.Opacity = 1;
        }

        private void CategoryUI_Load(object sender, EventArgs e)
        {
        }
    }
}
