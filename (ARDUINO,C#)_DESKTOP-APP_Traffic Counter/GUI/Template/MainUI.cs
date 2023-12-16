using OfficeOpenXml;
using OfficeOpenXml.Style;
using System;
using System.Drawing;
using System.Globalization;
using System.IO;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Template
{
    public partial class MainUI : Form
    {
        Point lastClick;
        Helper.Firebase database = new Helper.Firebase("https://trafficcounter-915f7.firebaseio.com/");

        public MainUI()
        {
            InitializeComponent();
        }

        //PANEL CONFIGURATIONS
        private void buttonClose_Click(object sender, EventArgs e)
        {
            Application.Exit();
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

        private void buttonMinimize_Enter(object sender, EventArgs e)
        {
            labelTitle.Focus();
        }

        private void chart1_Click(object sender, EventArgs e)
        {

        }

        private async void MainUI_Load(object sender, EventArgs e)
        {
            comboBox1.Items.Clear();
            var res = await database.Receive("");
            if (res != null && res["TRAFFIC"] != null)
            {
                foreach (var v in res["TRAFFIC"])
                {
                    comboBox1.Items.Add(Helper.String.Replace(v.Name.ToString(), "~","/"));
                }
                comboBox1.SelectedIndex = 0;
            }
        }

        private void dataGridView1_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {

        }

        int temp = 1;
        int cntr = 0;
        private async void timer1_Tick(object sender, EventArgs e)
        {
            var res = await database.Receive("");
            if (comboBox1.SelectedItem != null)
            {
                string txt = Helper.String.Replace(comboBox1.SelectedItem.ToString(), "/", "~");
                if (res != null && res["TRAFFIC"] != null && res["TRAFFIC"][txt] != null)
                {
                    cntr = 0;
                    foreach (var v in res["TRAFFIC"][txt])
                    {
                        cntr++;
                    }
                    if (temp != cntr)
                    {
                        dataGridView1.Rows.Clear();
                        int cntr2 = 0;
                        foreach (var v in res["TRAFFIC"][txt])
                        {
                            cntr2 = cntr2 + 1;
                            try
                            {
                                DateTime myDate = Convert.ToDateTime(v.Name.ToString());
                                dataGridView1.Rows.Add(cntr2,myDate.ToString("hh:mm tt"), v.Value.ToString());
                            }
                            catch
                            { }
                        }
                        temp = cntr;
                    }
                    label1.Text = String.Format("Date: {0}\nVehicles: {1}", comboBox1.SelectedItem.ToString(), cntr);
                }
            }
        }

        private void dataGridView1_SelectionChanged(object sender, EventArgs e)
        {
        }

        private void comboBox1_SelectedIndexChanged(object sender, EventArgs e)
        {
            Console.WriteLine("changed");
            cntr = 0;
        }

        private async void button1_Click(object sender, EventArgs e)
        {
            if (Helper.Message.Question("Export this to excel?", "Information") == DialogResult.Yes)
            {

                string txt2 = Helper.String.Replace(comboBox1.SelectedItem.ToString(), "/", "~");
                var res = await database.Receive("");
                string txt = Helper.String.Replace(comboBox1.SelectedItem.ToString(), "/", "-");
                string file = "TRAFFIC (" + txt + ").xlsx";

                FileInfo newFile = new FileInfo(file);
                bool doExcel = false;
                if (File.Exists(file))
                {
                    try
                    {
                        File.Delete(file);
                        doExcel = true;
                    }
                    catch (Exception)
                    {
                        doExcel = false;
                        MessageBox.Show(this, "File is currently in used.\nPlease close the Excel file.", "Information",
                            MessageBoxButtons.OK);
                    }
                }
                else
                {
                    newFile = new FileInfo(file);
                    doExcel = true;
                }
                if (doExcel == true)
                {
                    using (ExcelPackage package = await Task.FromResult<ExcelPackage>(new ExcelPackage(newFile)))
                    {
                        ExcelWorksheet wSheet = package.Workbook.Worksheets.Add(txt);
                        wSheet.Cells[1, 1].Value = "TIME INTERVAL";
                        wSheet.Cells[1, 1].Style.Font.Bold = true;
                        wSheet.Cells[1, 2].Value = "VEHICLES";
                        wSheet.Cells[1, 2].Style.Font.Bold = true;
                        //wSheet.Cells[1, 3].Value = "TOTAL x PCU";
                        //wSheet.Cells[1, 3].Style.Font.Bold = true;
                        wSheet.Cells[1, 3].Value = "VOLUME/CAPACITY";
                        wSheet.Cells[1, 3].Style.Font.Bold = true;
                        wSheet.Cells[1, 4].Value = "LEVEL OF SERVICE";
                        wSheet.Cells[1, 4].Style.Font.Bold = true;
                        wSheet.Cells[1, 5].Value = "DESCRIPTION";
                        wSheet.Cells[1, 5].Style.Font.Bold = true;
                        if (res != null && res["TRAFFIC"] != null && res["TRAFFIC"][txt2] != null)
                        {
                            int cntr2 = 0;
                            string[] time = { "01", "02" , "03" , "04" , "05" , "06" , "07" , "08" , "09" , "10" , "11", "12",
                                              "13", "14" , "15" , "16" , "17" , "18" , "19" , "20" , "21" , "22" , "23", "00"};
                            foreach (string v1 in time)
                            {
                                int cntr = 0;
                                string tempDate = "";
                                foreach (var v in res["TRAFFIC"][txt2])
                                {
                                    DateTime myDate = Convert.ToDateTime(v.Name.ToString());
                                    if (v1.ToString() == myDate.ToString("HH"))
                                    {
                                        cntr++;
                                        tempDate = v1.ToString();
                                    }
                                    //wSheet.Cells[2 + cntr, 1].Value = cntr + 1;
                                    //wSheet.Cells[2 + cntr, 2].Value = myDate.ToString("hh:mm tt");
                                    //wSheet.Cells[2 + cntr, 3].Value = v.Value.ToString();
                                    //cntr++;
                                }
                                if (tempDate == v1.ToString())
                                {
                                    string txt69 = v1.ToString() + ":00:00";
                                    string txt699 = "";
                                    if (v1.ToString() != "23")
                                    {
                                        txt699 = (int.Parse(v1) + 1).ToString() + ":00:00";
                                    }
                                    else
                                    {
                                        txt699 = "00:00:00";
                                    }
                                    DateTime myDate1 = Convert.ToDateTime(txt69);
                                    DateTime myDate11 = Convert.ToDateTime(txt699);
                                    wSheet.Cells[2 + cntr2, 1].Value = myDate1.ToString("hh:mm tt") + "-" + myDate11.ToString("hh:mm tt");
                                    wSheet.Cells[2 + cntr2, 2].Value = cntr;
                                    //wSheet.Cells[2 + cntr2, 3].Value = numericUpDown1.Value*cntr;
                                    Decimal calculation = Math.Round(numericUpDown1.Value * cntr / numericUpDown2.Value, 2);
                                    wSheet.Cells[2 + cntr2, 3].Value = calculation;
                                    string remarks = "";
                                    string lvl = "";
                                    if ((Double)calculation<=0.20)
                                    {
                                        lvl = "LOS A";
                                        remarks = "Free flowing traffic";
                                    }
                                    if ((Double)calculation>=0.21 && (Double)calculation<=0.50)
                                    {
                                        lvl = "LOS B";
                                        remarks = "Relatively free flowing traffic";
                                    }
                                    if ((Double)calculation>=0.51 && (Double)calculation<=0.70)
                                    {
                                        lvl = "LOS C";
                                        remarks = "Moderate traffic";
                                    }
                                    if ((Double)calculation >= 0.71 && (Double)calculation <= 0.85)
                                    {
                                        lvl = "LOS D";
                                        remarks = "Moderate to heavy traffic";
                                    }
                                    if ((Double)calculation >= 0.86 && (Double)calculation <= 1.00)
                                    {
                                        lvl = "LOS E";
                                        remarks = "Heavy traffic";
                                    }
                                    if ((Double)calculation > 1)
                                    {
                                        lvl = "LOS F";
                                        remarks = "Saturation traffic volumes";
                                    }
                                    wSheet.Cells[2 + cntr2, 4].Value = lvl;
                                    wSheet.Cells[2 + cntr2, 5].Value = remarks;
                                    cntr2++;
                                }
                            }
                        }
                        for (int i = 1; i <= 5; i++)
                        {
                            wSheet.Column(i).AutoFit();

                            wSheet.Column(i).Style.HorizontalAlignment = ExcelHorizontalAlignment.Center;
                        }
                        package.Save();
                        Helper.Message.Default("FILE EXPORTED WITH SOFTWARE'S DIRECTORY.", "Information");
                    }
                }
            }
        }
    }
}
