namespace Thesis.Ver2.Searchbar
{
    partial class Item
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
            this.VariableButton = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // VariableButton
            // 
            this.VariableButton.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.VariableButton.Location = new System.Drawing.Point(3, 3);
            this.VariableButton.Name = "VariableButton";
            this.VariableButton.Size = new System.Drawing.Size(297, 127);
            this.VariableButton.TabIndex = 0;
            this.VariableButton.Text = "VariableButton";
            this.VariableButton.UseVisualStyleBackColor = true;
            // 
            // Item
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 20F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.Controls.Add(this.VariableButton);
            this.Name = "Item";
            this.Size = new System.Drawing.Size(303, 133);
            this.ResumeLayout(false);

        }

        #endregion

        public System.Windows.Forms.Button VariableButton;
    }
}
