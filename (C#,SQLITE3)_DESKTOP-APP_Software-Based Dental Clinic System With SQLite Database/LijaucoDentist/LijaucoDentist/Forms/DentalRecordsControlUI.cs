using System;
using System.Windows.Forms;

namespace LijaucoDentist
{
    public partial class DentalRecordsControlUI : UserControl
    {
        string recordid, date;
        CustomersEditUI form;
        public DentalRecordsControlUI(string _recordid, string _date, CustomersEditUI _form)
        {
            InitializeComponent();
            recordid = _recordid;
            date = _date;
            form = _form;
            labelRecordID.Text = recordid;
            labelDate.Text = date;
            var res = Program.database.SELECT("RECORDS", "RecordID='" + recordid + "'", null)[0];
            labelCharged.Text = "Php. " + res["AmountCharged"];
            if (labelCharged.Text == "Php. NONE")
            {
                labelCharged.Text = "NONE";
                this.BackColor = System.Drawing.Color.MistyRose;
            }
            labelPaid.Text = "Php. " + res["AmountPaid"];
            if (labelPaid.Text == "Php. NONE")
            {
                labelPaid.Text = "NONE";
                this.BackColor = System.Drawing.Color.MistyRose;
            }
            if (Decimal.Parse(res["Balance"]) != 0)
            {
                Helper.ThreadLib.SetProperty(this, labelbb, "Visible", true);
                Helper.ThreadLib.SetProperty(this, labelBalance, "Visible", true);
                Helper.ThreadLib.SetProperty(this, buttonPay, "Visible", true);
                Helper.ThreadLib.SetProperty(this, numericUpDownPayment, "Visible", true);
                Helper.ThreadLib.SetProperty(this, labelBalance, "Text", "Php. " + res["Balance"]);
                //labelbb.Visible = true;
                //labelBalance.Visible = true;
                //buttonPay.Visible = true;
                //numericUpDownPayment.Visible = true;
                //labelBalance.Text = "Php. " + res["Balance"];
            }
        }

        private void button1_Enter(object sender, EventArgs e)
        {
            label1.Focus();
        }

        private void buttonEdit_Click(object sender, EventArgs e)
        {
            form.Opacity = LoginUI.opacity;
            new CategoryEditUI(recordid, date, form).ShowDialog();
            form.Opacity = 1;
        }

        private void buttonPay_Click(object sender, EventArgs e)
        {
            var res = Program.database.SELECT("RECORDS", "RecordID='" + recordid + "'", null)[0];
            if (Decimal.Parse(numericUpDownPayment.Value.ToString("F")) <= Decimal.Parse(res["Balance"]))
            {
                if (Decimal.Parse(numericUpDownPayment.Value.ToString("F")) != 0)
                {
                    Program.database.INSERT("RECORDS", new string[] { "RecordID", "AmountPaid", "Balance" }, new string[] { recordid,
                    (Decimal.Parse(res["AmountPaid"]) + Decimal.Parse(numericUpDownPayment.Value.ToString("F"))).ToString("F"),
                    (Decimal.Parse(res["AmountCharged"]) - (Decimal.Parse(res["AmountPaid"])+Decimal.Parse(numericUpDownPayment.Value.ToString("F")))).ToString("F")
                    });
                    res = Program.database.SELECT("RECORDS", "RecordID='" + recordid + "'", null)[0];
                    labelCharged.Text = "Php. " + res["AmountCharged"];
                    labelPaid.Text = "Php. " + res["AmountPaid"];
                    if (Decimal.Parse(res["Balance"]) != 0)
                    {
                        labelbb.Visible = true;
                        labelBalance.Visible = true;
                        buttonPay.Visible = true;
                        numericUpDownPayment.Visible = true;
                        labelBalance.Text = "Php. " + res["Balance"];
                    }
                    else
                    {
                        labelbb.Visible = false;
                        labelBalance.Visible = false;
                        buttonPay.Visible = false;
                        numericUpDownPayment.Visible = false;
                        labelBalance.Text = "Php. " + res["Balance"];
                    }
                    Helper.Msg.Default("Payment done.", "Information");
                }
            }
            else
            {
                Helper.Msg.Information("Amount payment shouldn't be greater than the amount balance.", "Information");
            }
            numericUpDownPayment.Value = 0;
        }

        private void buttonDelete_Click(object sender, EventArgs e)
        {
            if (Helper.Msg.Question("Delete this treatment record?", "Information") == DialogResult.Yes)
            {
                Program.database.DELETE("RECORDS", "RecordID='" + recordid + "'");
                form.button1_Click(null, null);
            }
        }
    }
}
