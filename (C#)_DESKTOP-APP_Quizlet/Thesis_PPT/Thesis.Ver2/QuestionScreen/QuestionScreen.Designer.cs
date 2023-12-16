
namespace Thesis.Ver2.QuestionScreen
{
    partial class QuestionScreen
    {
        /// <summary> 
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary> 
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Component Designer generated code

        /// <summary> 
        /// Required method for Designer support - do not modify 
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.flowLayoutPanel_Questions = new System.Windows.Forms.FlowLayoutPanel();
            this.button_Submit = new System.Windows.Forms.Button();
            this.label_Title = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // 
            // flowLayoutPanel_Questions
            // 
            this.flowLayoutPanel_Questions.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.flowLayoutPanel_Questions.AutoScroll = true;
            this.flowLayoutPanel_Questions.FlowDirection = System.Windows.Forms.FlowDirection.TopDown;
            this.flowLayoutPanel_Questions.Location = new System.Drawing.Point(32, 135);
            this.flowLayoutPanel_Questions.Name = "flowLayoutPanel_Questions";
            this.flowLayoutPanel_Questions.Size = new System.Drawing.Size(1020, 511);
            this.flowLayoutPanel_Questions.TabIndex = 0;
            this.flowLayoutPanel_Questions.WrapContents = false;
            // 
            // button_Submit
            // 
            this.button_Submit.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Right)));
            this.button_Submit.Location = new System.Drawing.Point(985, 685);
            this.button_Submit.Name = "button_Submit";
            this.button_Submit.Size = new System.Drawing.Size(94, 29);
            this.button_Submit.TabIndex = 1;
            this.button_Submit.Text = "Submit";
            this.button_Submit.UseVisualStyleBackColor = true;
            this.button_Submit.Click += new System.EventHandler(this.ButtonSubmitClick);
            // 
            // label_Title
            // 
            this.label_Title.AutoSize = true;
            this.label_Title.Font = new System.Drawing.Font("Segoe UI", 14F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point);
            this.label_Title.Location = new System.Drawing.Point(32, 11);
            this.label_Title.MaximumSize = new System.Drawing.Size(1040, 0);
            this.label_Title.Name = "label_Title";
            this.label_Title.Size = new System.Drawing.Size(231, 32);
            this.label_Title.TabIndex = 2;
            this.label_Title.Text = "Question Instruction";
            // 
            // ChallengeScreen
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 20F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.Controls.Add(this.label_Title);
            this.Controls.Add(this.button_Submit);
            this.Controls.Add(this.flowLayoutPanel_Questions);
            this.Name = "ChallengeScreen";
            this.Size = new System.Drawing.Size(1082, 717);
            this.Leave += new System.EventHandler(this.ChallengeScreen_Leave);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.FlowLayoutPanel flowLayoutPanel_Questions;
        private System.Windows.Forms.Button button_Submit;
        private System.Windows.Forms.Label label_Title;
    }
}
