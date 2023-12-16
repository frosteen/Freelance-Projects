using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace Thesis.Ver2.Searchbar
{
    public partial class SearchScreen : UserControl
    {
        readonly TextBox textbox;

        public SearchScreen(TextBox _textbox)
        {
            InitializeComponent();
            textbox = _textbox;
        }

        private void button1_Click(object sender, EventArgs e)
        {
            textbox.Clear();
            this.Parent.Controls.Remove(this);
        }
    }
}
