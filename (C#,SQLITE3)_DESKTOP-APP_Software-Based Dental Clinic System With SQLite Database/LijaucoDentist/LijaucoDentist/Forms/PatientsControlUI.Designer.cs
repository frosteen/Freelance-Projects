namespace LijaucoDentist
{
    partial class PatientsControlUI
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
            this.label1 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.buttonEdit = new System.Windows.Forms.Button();
            this.button2 = new System.Windows.Forms.Button();
            this.labelID = new System.Windows.Forms.Label();
            this.labelName = new System.Windows.Forms.Label();
            this.buttonNEW = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F);
            this.label1.Location = new System.Drawing.Point(16, 17);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(88, 20);
            this.label1.TabIndex = 8;
            this.label1.Text = "Patient ID:";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F);
            this.label2.Location = new System.Drawing.Point(16, 43);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(58, 20);
            this.label2.TabIndex = 9;
            this.label2.Text = "Name:";
            // 
            // buttonEdit
            // 
            this.buttonEdit.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(239)))), ((int)(((byte)(155)))), ((int)(((byte)(15)))));
            this.buttonEdit.FlatAppearance.BorderColor = System.Drawing.Color.Black;
            this.buttonEdit.FlatAppearance.BorderSize = 0;
            this.buttonEdit.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.buttonEdit.Font = new System.Drawing.Font("Microsoft Sans Serif", 7.8F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.buttonEdit.ForeColor = System.Drawing.Color.White;
            this.buttonEdit.Location = new System.Drawing.Point(497, 9);
            this.buttonEdit.Name = "buttonEdit";
            this.buttonEdit.Size = new System.Drawing.Size(81, 28);
            this.buttonEdit.TabIndex = 13;
            this.buttonEdit.TabStop = false;
            this.buttonEdit.Text = "VIEW";
            this.buttonEdit.UseVisualStyleBackColor = false;
            this.buttonEdit.Click += new System.EventHandler(this.buttonEdit_Click);
            this.buttonEdit.Enter += new System.EventHandler(this.button1_Enter);
            // 
            // button2
            // 
            this.button2.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(219)))), ((int)(((byte)(0)))), ((int)(((byte)(0)))));
            this.button2.FlatAppearance.BorderColor = System.Drawing.Color.Black;
            this.button2.FlatAppearance.BorderSize = 0;
            this.button2.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.button2.Font = new System.Drawing.Font("Microsoft Sans Serif", 7.8F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.button2.ForeColor = System.Drawing.Color.White;
            this.button2.Location = new System.Drawing.Point(410, 43);
            this.button2.Name = "button2";
            this.button2.Size = new System.Drawing.Size(168, 28);
            this.button2.TabIndex = 14;
            this.button2.TabStop = false;
            this.button2.Text = "DELETE";
            this.button2.UseVisualStyleBackColor = false;
            this.button2.Click += new System.EventHandler(this.button2_Click);
            this.button2.Enter += new System.EventHandler(this.button1_Enter);
            // 
            // labelID
            // 
            this.labelID.AutoSize = true;
            this.labelID.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.labelID.Location = new System.Drawing.Point(124, 17);
            this.labelID.Name = "labelID";
            this.labelID.Size = new System.Drawing.Size(18, 20);
            this.labelID.TabIndex = 15;
            this.labelID.Text = "1";
            // 
            // labelName
            // 
            this.labelName.AutoSize = true;
            this.labelName.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.labelName.Location = new System.Drawing.Point(92, 43);
            this.labelName.Name = "labelName";
            this.labelName.Size = new System.Drawing.Size(254, 20);
            this.labelName.TabIndex = 16;
            this.labelName.Text = "LIJAUO, VINCE ZACHARDY DG";
            // 
            // buttonNEW
            // 
            this.buttonNEW.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(91)))), ((int)(((byte)(158)))), ((int)(((byte)(246)))));
            this.buttonNEW.FlatAppearance.BorderColor = System.Drawing.Color.Black;
            this.buttonNEW.FlatAppearance.BorderSize = 0;
            this.buttonNEW.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.buttonNEW.Font = new System.Drawing.Font("Microsoft Sans Serif", 7.8F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.buttonNEW.ForeColor = System.Drawing.Color.White;
            this.buttonNEW.Location = new System.Drawing.Point(410, 9);
            this.buttonNEW.Name = "buttonNEW";
            this.buttonNEW.Size = new System.Drawing.Size(81, 28);
            this.buttonNEW.TabIndex = 17;
            this.buttonNEW.TabStop = false;
            this.buttonNEW.Text = "NEW";
            this.buttonNEW.UseVisualStyleBackColor = false;
            this.buttonNEW.Click += new System.EventHandler(this.buttonNEW_Click);
            this.buttonNEW.Enter += new System.EventHandler(this.button1_Enter);
            // 
            // PatientsControlUI
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(120F, 120F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Dpi;
            this.BackColor = System.Drawing.SystemColors.ControlLight;
            this.Controls.Add(this.buttonNEW);
            this.Controls.Add(this.labelName);
            this.Controls.Add(this.labelID);
            this.Controls.Add(this.button2);
            this.Controls.Add(this.buttonEdit);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.label1);
            this.Name = "PatientsControlUI";
            this.Size = new System.Drawing.Size(590, 81);
            this.Enter += new System.EventHandler(this.button1_Enter);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Button buttonEdit;
        private System.Windows.Forms.Button button2;
        private System.Windows.Forms.Label labelID;
        private System.Windows.Forms.Label labelName;
        private System.Windows.Forms.Button buttonNEW;
    }
}
