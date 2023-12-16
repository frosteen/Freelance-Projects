using System;
using System.Drawing;
using System.Windows.Forms;

namespace LijaucoDentist
{
    public partial class NoteUI : Form
    {
        Point lastClick;
        Form parentUI;
        string note;
        string recordid;

        public NoteUI(Form _parentUI, string _note, string _recordid)
        {
            InitializeComponent();
            parentUI = _parentUI;
            note = _note;
            recordid = _recordid;
            string modifiedText = "";
            if (_note != null)
            {
                string[] texts = Helper.Str.Split(note, new string[] { "~|ENTER|~" });
                int i = 0;
                foreach (string text in texts)
                {
                    if (i != texts.Length - 1)
                    {
                        if (text == "~|BLANK|~")
                        {
                            modifiedText += "\n";
                        }
                        else
                        {
                            modifiedText += text + "\n";
                        }
                    }
                    else
                    {
                        if (text == "~|BLANK|~")
                        {
                            modifiedText += "";
                        }
                        else
                        {
                            modifiedText += text;
                        }
                    }
                    i++;
                }
            }
            txtNote.Text = modifiedText;
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

        private void buttonClose_Click(object sender, EventArgs e)
        {
            this.Close();
        }

        private void buttonMinimize_Enter(object sender, EventArgs e)
        {
            labelTitle.Focus();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            string modifiedText = "";
            int i = 0;
            foreach (string line in txtNote.Lines)
            {
                if (line == "")
                {
                    modifiedText += "~|BLANK|~";
                }
                if (i != (txtNote.Lines.Length - 1))
                {
                    modifiedText += line + "~|ENTER|~";
                }
                else
                {
                    modifiedText += line;
                }
                i++;
            }
            Program.database.INSERT("RECORDS", new string[] { "RecordID", "Notes" },
                new string[] { recordid, modifiedText });
            Helper.Msg.Information("Note saved.", "Saved");
        }
    }
}
