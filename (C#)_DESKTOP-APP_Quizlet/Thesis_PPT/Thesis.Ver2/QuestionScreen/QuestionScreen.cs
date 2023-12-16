using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Windows.Forms;

namespace Thesis.Ver2.QuestionScreen
{
    public partial class QuestionScreen : UserControl
    {
        readonly string LessonName;
        Dictionary<string, string> question_bank;
        List<QuestionCard> question_cards;
        bool is_user_done;

        public QuestionScreen(QuestionBank _question_bank)
        {
            InitializeComponent();
            this.LessonName = _question_bank.LessonName;
            this.question_bank = _question_bank.GetQuestionBank();
            this.is_user_done = false;

            this.ShowQuestions();
        }

        private void ShowQuestions()
        {
            // Set the instruction
            label_Title.Text = this.question_bank["Question"];

            // Remove the question in the array to avoid mixing with the answers
            this.question_bank.Remove("Question");

            // Clear if there are existing cards in the panel
            if (flowLayoutPanel_Questions.Controls.Count > 0)
                flowLayoutPanel_Questions.Controls.Clear();

            // shuffle questions
            Random rnd = new Random();
            this.question_bank = this.question_bank.OrderBy(x => rnd.Next())
                .ToDictionary(item => item.Key, item => item.Value);

            // Convert answers to string array
            string[] question_bank_answers = new string[this.question_bank.Keys.Count];
            this.question_bank.Values.CopyTo(question_bank_answers, 0);
            
            // shuffle answers
            rnd = new Random();
            question_bank_answers = question_bank_answers.OrderBy(x => rnd.Next()).ToArray();

            // Get only unique answers
            string[] question_bank_answers_unique = question_bank_answers.Distinct().ToArray();

            // Add questions on the flowlayoutpanel
            this.question_cards = new List<QuestionCard>();

            foreach (string item in this.question_bank.Keys)
            {
                QuestionCard question_card = new QuestionCard
                {
                    Answers = question_bank_answers_unique.ToArray(),
                    Question = item
                };
                flowLayoutPanel_Questions.Controls.Add(question_card);
                this.question_cards.Add(question_card);
            }
        }

        private void ButtonSubmitClick(object sender, EventArgs e)
        {
            Dictionary<string, string> question_bank_answered= new Dictionary<string, string>();

            foreach (QuestionCard item in this.question_cards)
            {
                if (item.Answer == "")
                {
                    MessageBox.Show("You have left unanswered!");
                    break;
                }
                question_bank_answered.Add(item.Question, item.Answer);
            }

            // If everything is answered, calculate score
            if (question_bank_answered.Count == this.question_bank.Count)
            {
                string message = "";

                if (!question_bank_answered.Except(this.question_bank).Any())
                {
                    message = "Congratulations! You got a perfect score.";
                }
                else
                {
                    // calculate score
                    int get_score = this.question_bank.Count - 
                        question_bank_answered
                        .Except(this.question_bank)
                        .ToDictionary(x => x.Key, x => x.Value).Count();

                    message = "Congratulations! You scored " +
                        get_score.ToString() +
                        " out of " +
                        this.question_bank.Count.ToString() + ".";
                }

                // show score via messagebox
                DialogResult result = MessageBox.Show(message,
                   "Congratulations",
                   MessageBoxButtons.YesNo);

                if (result == DialogResult.Yes)
                {
                    this.is_user_done = false;
                    this.TryAgain();
                }
                else
                {
                    this.is_user_done = true;
                    this.Parent.Controls.Remove(this);
                }
            }
        }

        private void TryAgain()
        {
            flowLayoutPanel_Questions.Controls.Clear();

            this.question_bank = new QuestionBank(this.LessonName).GetQuestionBank();

            this.ShowQuestions();
        }

        private void ChallengeScreen_Leave(object sender, EventArgs e)
        {
            if (is_user_done == false)
                TryAgain();
        }
    }
}
