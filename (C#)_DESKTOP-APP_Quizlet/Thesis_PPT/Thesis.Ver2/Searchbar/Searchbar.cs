using System;
using System.Collections.Generic;
using System.Windows.Forms;
using Thesis.Ver2.Lessons;

namespace Thesis.Ver2.Searchbar
{
    public partial class Searchbar : UserControl
    {
        SearchScreen SC;

        Control panel_container;

        readonly Dictionary<string, UserControl> list_of_forms = new Dictionary<string, UserControl>()
        {
            ["First Quarter"] = new FirstQuarter(),
            ["Arithmetic Sequence"] = new Lessons.FirstQuarterLessons.Arithmetic_Sequence.ArithmeticMain(),
            ["Arithmetic Sequence\nLesson 1\nArithmetic Sequence"] = new Lessons.FirstQuarterLessons.Lesson1.ASPage1(),
            ["Arithmetic Sequence\nLesson 2\nThe nth Term"] = new Lessons.FirstQuarterLessons.Lesson2.TntasPage1(),
            ["Arithmetic Sequence\nLesson 3\nThe sum of the first Nth term"] = new Lessons.FirstQuarterLessons.Lesson_3.TsfntPage1(),
        };

        public Searchbar()
        {
            InitializeComponent();
        }

        private void TextBoxEnter(object sender, EventArgs e)
        {
            panel_container = this.Parent.Parent.Controls["PanelContainer"];

            TextBox.Clear();

            if (!panel_container.Controls.Contains(SC))
            {
                SC = new SearchScreen(TextBox)
                {
                    Dock = DockStyle.Fill
                };

                panel_container.Controls.Add(SC);
            }

            panel_container.Controls[SC.Name].BringToFront();

            TextBoxTextChanged(sender, e);
        }

        private void TextBoxTextChanged(object sender, EventArgs e)
        {
            int index = 0;

            foreach (var item in list_of_forms)
            {
                if (item.Key.ToLower().Contains(TextBox.Text.ToLower()))
                {
                    if (!SC.flowLayoutPanel1.Controls.ContainsKey(item.Key))
                    {
                        Item item_panel = new Item();

                        item_panel.Name = item.Key;
                        item_panel.VariableButton.Text = item.Key;

                        item_panel.VariableButton.Click += (object sender, EventArgs e) =>
                        {
                            if (!panel_container.Controls.Contains(item.Value))
                            {
                                item.Value.Dock = DockStyle.Fill;
                                panel_container.Controls.Add(item.Value);
                            }

                            panel_container.Controls[item.Value.Name].BringToFront();
                            panel_container.Controls.Remove(SC);
                        };


                        SC.flowLayoutPanel1.Controls.Add(item_panel);
                        SC.flowLayoutPanel1.Controls.SetChildIndex(item_panel, index);
                    }
                } else
                    SC.flowLayoutPanel1.Controls.RemoveByKey(item.Key);

                index++;
            }
        }
    }
}
