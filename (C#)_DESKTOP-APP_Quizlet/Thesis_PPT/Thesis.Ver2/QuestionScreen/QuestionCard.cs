using System.Windows.Forms;

namespace Thesis.Ver2.QuestionScreen
{
    public partial class QuestionCard : UserControl
    {
        public QuestionCard()
        {
            InitializeComponent();
        }

        public string Answer {
            get
            {
                if (comboBox1.SelectedItem != null)
                    return comboBox1.SelectedItem.ToString();
                return "";
            }
            set
            {
                if (int.TryParse(value, out int val))
                    comboBox1.SelectedIndex = val;
                else
                    comboBox1.SelectedIndex = -1;
            }
        }

        public string[] Answers
        {
            set
            {
                foreach (string item in value)
                    comboBox1.Items.Add(item);
            }
        }

        public string Question
        {
            get { return label1.Text; }
            set { label1.Text = value; }
        }
    }
}
