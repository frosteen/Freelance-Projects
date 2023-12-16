using System;
using System.Collections.Generic;

namespace Thesis.Ver2.QuestionScreen
{
    public class QuestionBank
    {
        string lesson;

        public QuestionBank(string _lesson)
        {
            this.lesson = _lesson;
        }

        public string LessonName
        {
            get { return this.lesson; }
            set { this.lesson = value; }
        }

        public Dictionary<string, String> GetQuestionBank()
        {
            List<Dictionary<string, string>> question_bank = new List<Dictionary<string, string>>();

            Random rnd = new Random();

            switch (this.lesson)
            {
                case "Aritmethic Sequence":
                    question_bank = new List<Dictionary<string, string>>
                    {
                        new Dictionary<string, string>
                        {
                            ["Question"] = "Determine if the given sequence is an arithmetic sequence. Write Yes if it is an arithmetic sequence and No if it is not.",
                            ["2, 6, 10, 14, . . ."] = "Yes",
                            ["–4, 8, –16, 32, –64, . . ."] = "No",
                            ["2, 1, 1/2, 1/4, 1/8, . . ."] = "No",
                            ["20, 13, 6, –1, –8, . . ."] = "Yes",
                            ["2, 2 1/2 , 3, 3 1/2, . . ."] = "Yes",
                        },
                        new Dictionary<string, string>
                        {
                            ["Question"] = "Determine if the following series of numbers are arithmetic sequences or not. If the given is an arithmetic sequence, write S on the space provided. If not, write N.",
                            ["2, 4, 6, 8, 10, 12, 14"] = "S",
                            ["5, 4, 7, 9, 11, 10, 8"] = "N",
                            ["25, 28, 31, 34, 37, 40, 43"] = "S",
                            ["14, 15, 17, 17, 19, 20, 21"] = "N",
                            ["124, 126, 128, 130, 132, 134, 136"] = "S",
                            ["10, 20, 30, 40, 50, 60, 70"] = "S",
                            ["1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5"] = "S",
                            ["P15.00, P17.00, P19.00, P21.00"] = "S",
                            ["17, 18, 35, 34, 21, 22, 16"] = "N",
                            ["4, 8, 12, 16, 20, 24, 28"] = "S",
                        },
                        new Dictionary<string, string>
                        {
                            ["Question"] = "Determine if the given sequence is an arithmetic sequence or not. Write Yes if it is and No if it is not.",
                            ["3, –1, –5, –9, . . ."] = "Yes",
                            ["½, 2, 8, 16, . . ."] = "No",
                            ["5¼, 5½, 5¾, 6, . . ."] = "Yes",
                            ["3/2, –3/4, 3/8, –3/16, . . ."] = "No",
                            ["6, –18, 54, –162, . . ."] = "No",
                        },
                    };
                    break;
                case "Geometric Sequence":
                    question_bank = new List<Dictionary<string, string>>
                    {
                        new Dictionary<string, string>
                        {
                            ["Question"] = "Determine if the given sequence is geometric or not. Write G in the blank if it is and N if it is not.",
                            ["1, 3, 9, 27, 81, . . ."] = "G",
                            ["–4, 8, –16, 32, –64, . . ."] = "G",
                            ["1, 4, 16, 64, . . ."] = "G",
                            ["20, 13, 6, –1, –8, . . ."] = "N",
                            ["–5, 0, 5, 10, 15, . . ."] = "N",
                        },
                        new Dictionary<string, string>
                        {
                            ["Question"] = "Identify if the following sequences of numbers are arithmetic sequences or geometric sequences.Write A in the blanks if they are arithmetic sequences and G if they are geometric sequences.",
                            ["2, 4, 6, 8, 10, . . ."] = "A",
                            ["5, 15, 45, 135, . . ."] = "G",
                            ["4, 16, 64, 256, . . ."] = "G",
                            ["2, 1, .5, .25, .125, . . ."] = "G",
                            ["3, 6, 9, 12, 15, . . ."] = "A",
                        },
                        new Dictionary<string, string>
                        {
                            ["Question"] = "Determine if the given set of numbers is an arithmetic sequence or a geometric sequence.Write A in the blank if the sequence is arithmetic and G if it is geometric.",
                            ["3, –1, –5, –9, . . ."] = "A",
                            ["½, 2, 8, 32, . . ."] = "G",
                            ["5¼, 5½, 5¾, 6, . . ."] = "A",
                            ["3/2, –3/4, 3/8, –3/16, . . ."] = "G",
                            ["6, –18, 54, –162, . . ."] = "G",
                        }
                    };
                    break;

            }

            int total_question_bank = question_bank.Count;

            int number = rnd.Next(0, total_question_bank);

            return question_bank[number];
        }

    }
}
