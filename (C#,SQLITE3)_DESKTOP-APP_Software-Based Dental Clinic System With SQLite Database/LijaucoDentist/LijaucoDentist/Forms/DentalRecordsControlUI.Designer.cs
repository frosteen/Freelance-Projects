namespace LijaucoDentist
{
    partial class DentalRecordsControlUI
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
            this.buttonDelete = new System.Windows.Forms.Button();
            this.labelRecordID = new System.Windows.Forms.Label();
            this.labelDate = new System.Windows.Forms.Label();
            this.labelCharged = new System.Windows.Forms.Label();
            this.labelbb = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.label5 = new System.Windows.Forms.Label();
            this.labelPaid = new System.Windows.Forms.Label();
            this.labelBalance = new System.Windows.Forms.Label();
            this.buttonPay = new System.Windows.Forms.Button();
            this.numericUpDownPayment = new System.Windows.Forms.NumericUpDown();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDownPayment)).BeginInit();
            this.SuspendLayout();
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F);
            this.label1.Location = new System.Drawing.Point(25, 14);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(90, 20);
            this.label1.TabIndex = 8;
            this.label1.Text = "Record ID:";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F);
            this.label2.Location = new System.Drawing.Point(362, 14);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(50, 20);
            this.label2.TabIndex = 9;
            this.label2.Text = "Date:";
            // 
            // buttonEdit
            // 
            this.buttonEdit.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(239)))), ((int)(((byte)(155)))), ((int)(((byte)(15)))));
            this.buttonEdit.FlatAppearance.BorderColor = System.Drawing.Color.Black;
            this.buttonEdit.FlatAppearance.BorderSize = 0;
            this.buttonEdit.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.buttonEdit.Font = new System.Drawing.Font("Microsoft Sans Serif", 7.8F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.buttonEdit.ForeColor = System.Drawing.Color.White;
            this.buttonEdit.Location = new System.Drawing.Point(656, 22);
            this.buttonEdit.Name = "buttonEdit";
            this.buttonEdit.Size = new System.Drawing.Size(81, 28);
            this.buttonEdit.TabIndex = 13;
            this.buttonEdit.TabStop = false;
            this.buttonEdit.Text = "EDIT";
            this.buttonEdit.UseVisualStyleBackColor = false;
            this.buttonEdit.Click += new System.EventHandler(this.buttonEdit_Click);
            this.buttonEdit.Enter += new System.EventHandler(this.button1_Enter);
            // 
            // buttonDelete
            // 
            this.buttonDelete.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(219)))), ((int)(((byte)(0)))), ((int)(((byte)(0)))));
            this.buttonDelete.FlatAppearance.BorderColor = System.Drawing.Color.Black;
            this.buttonDelete.FlatAppearance.BorderSize = 0;
            this.buttonDelete.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.buttonDelete.Font = new System.Drawing.Font("Microsoft Sans Serif", 7.8F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.buttonDelete.ForeColor = System.Drawing.Color.White;
            this.buttonDelete.Location = new System.Drawing.Point(656, 56);
            this.buttonDelete.Name = "buttonDelete";
            this.buttonDelete.Size = new System.Drawing.Size(81, 28);
            this.buttonDelete.TabIndex = 14;
            this.buttonDelete.TabStop = false;
            this.buttonDelete.Text = "DELETE";
            this.buttonDelete.UseVisualStyleBackColor = false;
            this.buttonDelete.Click += new System.EventHandler(this.buttonDelete_Click);
            this.buttonDelete.Enter += new System.EventHandler(this.button1_Enter);
            // 
            // labelRecordID
            // 
            this.labelRecordID.AutoSize = true;
            this.labelRecordID.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.labelRecordID.Location = new System.Drawing.Point(131, 14);
            this.labelRecordID.Name = "labelRecordID";
            this.labelRecordID.Size = new System.Drawing.Size(18, 20);
            this.labelRecordID.TabIndex = 15;
            this.labelRecordID.Text = "1";
            // 
            // labelDate
            // 
            this.labelDate.AutoSize = true;
            this.labelDate.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.labelDate.Location = new System.Drawing.Point(425, 14);
            this.labelDate.Name = "labelDate";
            this.labelDate.Size = new System.Drawing.Size(73, 20);
            this.labelDate.TabIndex = 16;
            this.labelDate.Text = "01/01/99";
            // 
            // labelCharged
            // 
            this.labelCharged.AutoSize = true;
            this.labelCharged.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.labelCharged.Location = new System.Drawing.Point(115, 43);
            this.labelCharged.Name = "labelCharged";
            this.labelCharged.Size = new System.Drawing.Size(56, 20);
            this.labelCharged.TabIndex = 18;
            this.labelCharged.Text = "Php. 0";
            // 
            // labelbb
            // 
            this.labelbb.AutoSize = true;
            this.labelbb.BackColor = System.Drawing.Color.Transparent;
            this.labelbb.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F);
            this.labelbb.ForeColor = System.Drawing.Color.Red;
            this.labelbb.Location = new System.Drawing.Point(25, 73);
            this.labelbb.Name = "labelbb";
            this.labelbb.Size = new System.Drawing.Size(75, 20);
            this.labelbb.TabIndex = 17;
            this.labelbb.Text = "Balance:";
            this.labelbb.Visible = false;
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F);
            this.label3.Location = new System.Drawing.Point(362, 43);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(47, 20);
            this.label3.TabIndex = 17;
            this.label3.Text = "Paid:";
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F);
            this.label5.Location = new System.Drawing.Point(25, 43);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(77, 20);
            this.label5.TabIndex = 17;
            this.label5.Text = "Charged:";
            // 
            // labelPaid
            // 
            this.labelPaid.AutoSize = true;
            this.labelPaid.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.labelPaid.Location = new System.Drawing.Point(425, 43);
            this.labelPaid.Name = "labelPaid";
            this.labelPaid.Size = new System.Drawing.Size(56, 20);
            this.labelPaid.TabIndex = 19;
            this.labelPaid.Text = "Php. 0";
            // 
            // labelBalance
            // 
            this.labelBalance.AutoSize = true;
            this.labelBalance.BackColor = System.Drawing.Color.Transparent;
            this.labelBalance.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.labelBalance.ForeColor = System.Drawing.Color.Red;
            this.labelBalance.Location = new System.Drawing.Point(115, 73);
            this.labelBalance.Name = "labelBalance";
            this.labelBalance.Size = new System.Drawing.Size(56, 20);
            this.labelBalance.TabIndex = 20;
            this.labelBalance.Text = "Php. 0";
            this.labelBalance.Visible = false;
            // 
            // buttonPay
            // 
            this.buttonPay.BackColor = System.Drawing.Color.Green;
            this.buttonPay.FlatAppearance.BorderColor = System.Drawing.Color.Black;
            this.buttonPay.FlatAppearance.BorderSize = 0;
            this.buttonPay.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.buttonPay.Font = new System.Drawing.Font("Microsoft Sans Serif", 7.8F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.buttonPay.ForeColor = System.Drawing.Color.White;
            this.buttonPay.Location = new System.Drawing.Point(533, 68);
            this.buttonPay.Name = "buttonPay";
            this.buttonPay.Size = new System.Drawing.Size(69, 28);
            this.buttonPay.TabIndex = 13;
            this.buttonPay.TabStop = false;
            this.buttonPay.Text = "PAY";
            this.buttonPay.UseVisualStyleBackColor = false;
            this.buttonPay.Visible = false;
            this.buttonPay.Click += new System.EventHandler(this.buttonPay_Click);
            this.buttonPay.Enter += new System.EventHandler(this.button1_Enter);
            // 
            // numericUpDownPayment
            // 
            this.numericUpDownPayment.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.numericUpDownPayment.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F);
            this.numericUpDownPayment.Location = new System.Drawing.Point(367, 69);
            this.numericUpDownPayment.Maximum = new decimal(new int[] {
            1000000000,
            0,
            0,
            0});
            this.numericUpDownPayment.Name = "numericUpDownPayment";
            this.numericUpDownPayment.Size = new System.Drawing.Size(160, 26);
            this.numericUpDownPayment.TabIndex = 0;
            this.numericUpDownPayment.Visible = false;
            // 
            // DentalRecordsControlUI
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(120F, 120F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Dpi;
            this.BackColor = System.Drawing.SystemColors.ControlLight;
            this.Controls.Add(this.numericUpDownPayment);
            this.Controls.Add(this.labelBalance);
            this.Controls.Add(this.labelPaid);
            this.Controls.Add(this.labelCharged);
            this.Controls.Add(this.label5);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.labelbb);
            this.Controls.Add(this.labelDate);
            this.Controls.Add(this.labelRecordID);
            this.Controls.Add(this.buttonDelete);
            this.Controls.Add(this.buttonPay);
            this.Controls.Add(this.buttonEdit);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.label1);
            this.Name = "DentalRecordsControlUI";
            this.Size = new System.Drawing.Size(762, 106);
            this.Enter += new System.EventHandler(this.button1_Enter);
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDownPayment)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Button buttonEdit;
        private System.Windows.Forms.Button buttonDelete;
        private System.Windows.Forms.Label labelRecordID;
        private System.Windows.Forms.Label labelDate;
        private System.Windows.Forms.Label labelCharged;
        private System.Windows.Forms.Label labelbb;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.Label labelPaid;
        private System.Windows.Forms.Label labelBalance;
        private System.Windows.Forms.Button buttonPay;
        private System.Windows.Forms.NumericUpDown numericUpDownPayment;
    }
}
