namespace KioskHttpClientApp
{
    partial class Form1
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
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

        #region Windows Form Designer generated code

        /// <summary>
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            action = new Label();
            btnGetDetect = new Button();
            btnLedTest = new Button();
            pictureBox1 = new PictureBox();
            action_name = new Label();
            label1 = new Label();
            lb_confidence = new Label();
            tabControl = new TabControl();
            tabPageStreaming = new TabPage();
            tabPageSettings = new TabPage();
            btnReset = new Button();
            groupBox1 = new GroupBox();
            tableLayoutPanel1 = new TableLayoutPanel();
            numericUpDownYend = new NumericUpDown();
            numericUpDownXend = new NumericUpDown();
            numericUpDownYstart = new NumericUpDown();
            numericUpDownXstart = new NumericUpDown();
            label2 = new Label();
            label3 = new Label();
            label5 = new Label();
            label4 = new Label();
            btnApply = new Button();
            pictureBox2 = new PictureBox();
            tabPageDebug = new TabPage();
            button3 = new Button();
            btnGetDetectRoi = new Button();
            ((System.ComponentModel.ISupportInitialize)pictureBox1).BeginInit();
            tabControl.SuspendLayout();
            tabPageStreaming.SuspendLayout();
            tabPageSettings.SuspendLayout();
            groupBox1.SuspendLayout();
            tableLayoutPanel1.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)numericUpDownYend).BeginInit();
            ((System.ComponentModel.ISupportInitialize)numericUpDownXend).BeginInit();
            ((System.ComponentModel.ISupportInitialize)numericUpDownYstart).BeginInit();
            ((System.ComponentModel.ISupportInitialize)numericUpDownXstart).BeginInit();
            ((System.ComponentModel.ISupportInitialize)pictureBox2).BeginInit();
            tabPageDebug.SuspendLayout();
            SuspendLayout();
            // 
            // action
            // 
            action.AutoSize = true;
            action.Font = new Font("Microsoft JhengHei UI", 20F, FontStyle.Regular, GraphicsUnit.Point);
            action.Location = new Point(706, 100);
            action.Name = "action";
            action.Size = new Size(0, 35);
            action.TabIndex = 0;
            // 
            // btnGetDetect
            // 
            btnGetDetect.Location = new Point(145, 149);
            btnGetDetect.Name = "btnGetDetect";
            btnGetDetect.Size = new Size(152, 56);
            btnGetDetect.TabIndex = 1;
            btnGetDetect.Text = "GET api/detect";
            btnGetDetect.UseVisualStyleBackColor = true;
            btnGetDetect.Click += btnGet_Click;
            // 
            // btnLedTest
            // 
            btnLedTest.Location = new Point(370, 240);
            btnLedTest.Name = "btnLedTest";
            btnLedTest.Size = new Size(152, 52);
            btnLedTest.TabIndex = 3;
            btnLedTest.Text = "LED Test";
            btnLedTest.UseVisualStyleBackColor = true;
            btnLedTest.Click += btnLedTest_Click;
            // 
            // pictureBox1
            // 
            pictureBox1.Location = new Point(28, 24);
            pictureBox1.Name = "pictureBox1";
            pictureBox1.Size = new Size(960, 540);
            pictureBox1.SizeMode = PictureBoxSizeMode.AutoSize;
            pictureBox1.TabIndex = 4;
            pictureBox1.TabStop = false;
            // 
            // action_name
            // 
            action_name.AutoSize = true;
            action_name.Font = new Font("Microsoft JhengHei UI", 20F, FontStyle.Regular, GraphicsUnit.Point);
            action_name.Location = new Point(805, 100);
            action_name.Name = "action_name";
            action_name.Size = new Size(0, 35);
            action_name.TabIndex = 5;
            // 
            // label1
            // 
            label1.AutoSize = true;
            label1.Font = new Font("Microsoft JhengHei UI", 20F, FontStyle.Regular, GraphicsUnit.Point);
            label1.Location = new Point(706, 152);
            label1.Name = "label1";
            label1.Size = new Size(0, 35);
            label1.TabIndex = 6;
            // 
            // lb_confidence
            // 
            lb_confidence.AutoSize = true;
            lb_confidence.Font = new Font("Microsoft JhengHei UI", 20F, FontStyle.Regular, GraphicsUnit.Point);
            lb_confidence.Location = new Point(876, 152);
            lb_confidence.Name = "lb_confidence";
            lb_confidence.Size = new Size(0, 35);
            lb_confidence.TabIndex = 7;
            // 
            // tabControl
            // 
            tabControl.Controls.Add(tabPageStreaming);
            tabControl.Controls.Add(tabPageSettings);
            tabControl.Controls.Add(tabPageDebug);
            tabControl.ItemSize = new Size(70, 25);
            tabControl.Location = new Point(12, 12);
            tabControl.Name = "tabControl";
            tabControl.SelectedIndex = 0;
            tabControl.Size = new Size(1028, 612);
            tabControl.SizeMode = TabSizeMode.Fixed;
            tabControl.TabIndex = 8;
            // 
            // tabPageStreaming
            // 
            tabPageStreaming.Controls.Add(pictureBox1);
            tabPageStreaming.Location = new Point(4, 29);
            tabPageStreaming.Name = "tabPageStreaming";
            tabPageStreaming.Padding = new Padding(3);
            tabPageStreaming.Size = new Size(1020, 579);
            tabPageStreaming.TabIndex = 0;
            tabPageStreaming.Text = "Streaming";
            tabPageStreaming.UseVisualStyleBackColor = true;
            // 
            // tabPageSettings
            // 
            tabPageSettings.Controls.Add(btnReset);
            tabPageSettings.Controls.Add(groupBox1);
            tabPageSettings.Controls.Add(btnApply);
            tabPageSettings.Controls.Add(pictureBox2);
            tabPageSettings.Location = new Point(4, 29);
            tabPageSettings.Name = "tabPageSettings";
            tabPageSettings.Padding = new Padding(3);
            tabPageSettings.Size = new Size(1020, 579);
            tabPageSettings.TabIndex = 1;
            tabPageSettings.Text = "Settings";
            tabPageSettings.UseVisualStyleBackColor = true;
            // 
            // btnReset
            // 
            btnReset.Font = new Font("Microsoft JhengHei UI", 12F, FontStyle.Regular, GraphicsUnit.Point);
            btnReset.Location = new Point(701, 405);
            btnReset.Name = "btnReset";
            btnReset.Size = new Size(136, 69);
            btnReset.TabIndex = 11;
            btnReset.Text = "Reset";
            btnReset.UseVisualStyleBackColor = true;
            btnReset.Click += btnReset_Click;
            // 
            // groupBox1
            // 
            groupBox1.Controls.Add(tableLayoutPanel1);
            groupBox1.Font = new Font("Microsoft JhengHei UI", 12F, FontStyle.Regular, GraphicsUnit.Point);
            groupBox1.Location = new Point(701, 114);
            groupBox1.Name = "groupBox1";
            groupBox1.Size = new Size(281, 272);
            groupBox1.TabIndex = 10;
            groupBox1.TabStop = false;
            groupBox1.Text = "ROI Coordinates";
            // 
            // tableLayoutPanel1
            // 
            tableLayoutPanel1.ColumnCount = 2;
            tableLayoutPanel1.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 37.0967751F));
            tableLayoutPanel1.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 62.9032249F));
            tableLayoutPanel1.Controls.Add(numericUpDownYend, 1, 3);
            tableLayoutPanel1.Controls.Add(numericUpDownXend, 1, 2);
            tableLayoutPanel1.Controls.Add(numericUpDownYstart, 1, 1);
            tableLayoutPanel1.Controls.Add(numericUpDownXstart, 1, 0);
            tableLayoutPanel1.Controls.Add(label2, 0, 0);
            tableLayoutPanel1.Controls.Add(label3, 0, 1);
            tableLayoutPanel1.Controls.Add(label5, 0, 2);
            tableLayoutPanel1.Controls.Add(label4, 0, 3);
            tableLayoutPanel1.Location = new Point(16, 38);
            tableLayoutPanel1.Name = "tableLayoutPanel1";
            tableLayoutPanel1.RowCount = 4;
            tableLayoutPanel1.RowStyles.Add(new RowStyle(SizeType.Percent, 25F));
            tableLayoutPanel1.RowStyles.Add(new RowStyle(SizeType.Percent, 25F));
            tableLayoutPanel1.RowStyles.Add(new RowStyle(SizeType.Percent, 25F));
            tableLayoutPanel1.RowStyles.Add(new RowStyle(SizeType.Percent, 25F));
            tableLayoutPanel1.Size = new Size(248, 211);
            tableLayoutPanel1.TabIndex = 3;
            // 
            // numericUpDownYend
            // 
            numericUpDownYend.Anchor = AnchorStyles.Left;
            numericUpDownYend.Increment = new decimal(new int[] { 5, 0, 0, 0 });
            numericUpDownYend.Location = new Point(95, 169);
            numericUpDownYend.Maximum = new decimal(new int[] { 2000, 0, 0, 0 });
            numericUpDownYend.Name = "numericUpDownYend";
            numericUpDownYend.Size = new Size(120, 28);
            numericUpDownYend.TabIndex = 15;
            numericUpDownYend.Value = new decimal(new int[] { 400, 0, 0, 0 });
            // 
            // numericUpDownXend
            // 
            numericUpDownXend.Anchor = AnchorStyles.Left;
            numericUpDownXend.Increment = new decimal(new int[] { 5, 0, 0, 0 });
            numericUpDownXend.Location = new Point(95, 116);
            numericUpDownXend.Maximum = new decimal(new int[] { 2000, 0, 0, 0 });
            numericUpDownXend.Name = "numericUpDownXend";
            numericUpDownXend.Size = new Size(120, 28);
            numericUpDownXend.TabIndex = 14;
            numericUpDownXend.Value = new decimal(new int[] { 400, 0, 0, 0 });
            // 
            // numericUpDownYstart
            // 
            numericUpDownYstart.Anchor = AnchorStyles.Left;
            numericUpDownYstart.Increment = new decimal(new int[] { 5, 0, 0, 0 });
            numericUpDownYstart.Location = new Point(95, 64);
            numericUpDownYstart.Maximum = new decimal(new int[] { 2000, 0, 0, 0 });
            numericUpDownYstart.Name = "numericUpDownYstart";
            numericUpDownYstart.Size = new Size(120, 28);
            numericUpDownYstart.TabIndex = 13;
            numericUpDownYstart.Value = new decimal(new int[] { 100, 0, 0, 0 });
            // 
            // numericUpDownXstart
            // 
            numericUpDownXstart.Anchor = AnchorStyles.Left;
            numericUpDownXstart.Increment = new decimal(new int[] { 5, 0, 0, 0 });
            numericUpDownXstart.Location = new Point(95, 12);
            numericUpDownXstart.Maximum = new decimal(new int[] { 2000, 0, 0, 0 });
            numericUpDownXstart.Name = "numericUpDownXstart";
            numericUpDownXstart.Size = new Size(120, 28);
            numericUpDownXstart.TabIndex = 12;
            numericUpDownXstart.Value = new decimal(new int[] { 100, 0, 0, 0 });
            // 
            // label2
            // 
            label2.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Right;
            label2.AutoSize = true;
            label2.Font = new Font("Microsoft JhengHei UI", 12F, FontStyle.Regular, GraphicsUnit.Point);
            label2.Location = new Point(20, 0);
            label2.Name = "label2";
            label2.Size = new Size(69, 52);
            label2.TabIndex = 2;
            label2.Text = "x (start):";
            label2.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // label3
            // 
            label3.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Right;
            label3.AutoSize = true;
            label3.Font = new Font("Microsoft JhengHei UI", 12F, FontStyle.Regular, GraphicsUnit.Point);
            label3.Location = new Point(20, 52);
            label3.Name = "label3";
            label3.Size = new Size(69, 52);
            label3.TabIndex = 4;
            label3.Text = "y (start):";
            label3.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // label5
            // 
            label5.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Right;
            label5.AutoSize = true;
            label5.Font = new Font("Microsoft JhengHei UI", 12F, FontStyle.Regular, GraphicsUnit.Point);
            label5.Location = new Point(25, 104);
            label5.Name = "label5";
            label5.Size = new Size(64, 52);
            label5.TabIndex = 6;
            label5.Text = "x (end):";
            label5.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // label4
            // 
            label4.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Right;
            label4.AutoSize = true;
            label4.Font = new Font("Microsoft JhengHei UI", 12F, FontStyle.Regular, GraphicsUnit.Point);
            label4.Location = new Point(25, 156);
            label4.Name = "label4";
            label4.Size = new Size(64, 55);
            label4.TabIndex = 8;
            label4.Text = "y (end):";
            label4.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // btnApply
            // 
            btnApply.Font = new Font("Microsoft JhengHei UI", 12F, FontStyle.Regular, GraphicsUnit.Point);
            btnApply.Location = new Point(846, 405);
            btnApply.Name = "btnApply";
            btnApply.Size = new Size(136, 69);
            btnApply.TabIndex = 9;
            btnApply.Text = "Apply";
            btnApply.UseVisualStyleBackColor = true;
            btnApply.Click += btnApply_Click;
            // 
            // pictureBox2
            // 
            pictureBox2.Location = new Point(36, 114);
            pictureBox2.Name = "pictureBox2";
            pictureBox2.Size = new Size(640, 360);
            pictureBox2.SizeMode = PictureBoxSizeMode.StretchImage;
            pictureBox2.TabIndex = 0;
            pictureBox2.TabStop = false;
            // 
            // tabPageDebug
            // 
            tabPageDebug.Controls.Add(button3);
            tabPageDebug.Controls.Add(btnGetDetectRoi);
            tabPageDebug.Controls.Add(btnGetDetect);
            tabPageDebug.Controls.Add(btnLedTest);
            tabPageDebug.Location = new Point(4, 29);
            tabPageDebug.Name = "tabPageDebug";
            tabPageDebug.Size = new Size(1020, 579);
            tabPageDebug.TabIndex = 2;
            tabPageDebug.Text = "Debug";
            tabPageDebug.UseVisualStyleBackColor = true;
            // 
            // button3
            // 
            button3.Location = new Point(145, 327);
            button3.Name = "button3";
            button3.Size = new Size(152, 82);
            button3.TabIndex = 5;
            button3.Text = "POST api/detect/setroi\r\n(100,200,300,400)";
            button3.UseVisualStyleBackColor = true;
            button3.Click += button3_Click;
            // 
            // btnGetDetectRoi
            // 
            btnGetDetectRoi.Location = new Point(145, 236);
            btnGetDetectRoi.Name = "btnGetDetectRoi";
            btnGetDetectRoi.Size = new Size(152, 56);
            btnGetDetectRoi.TabIndex = 4;
            btnGetDetectRoi.Text = "GET api/detect/getroi";
            btnGetDetectRoi.UseVisualStyleBackColor = true;
            btnGetDetectRoi.Click += btnGetDetectRoi_Click;
            // 
            // Form1
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(1052, 626);
            Controls.Add(tabControl);
            Controls.Add(lb_confidence);
            Controls.Add(label1);
            Controls.Add(action_name);
            Controls.Add(action);
            Name = "Form1";
            Text = "KioskClientApp";
            Load += Form1_Load;
            ((System.ComponentModel.ISupportInitialize)pictureBox1).EndInit();
            tabControl.ResumeLayout(false);
            tabPageStreaming.ResumeLayout(false);
            tabPageStreaming.PerformLayout();
            tabPageSettings.ResumeLayout(false);
            groupBox1.ResumeLayout(false);
            tableLayoutPanel1.ResumeLayout(false);
            tableLayoutPanel1.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)numericUpDownYend).EndInit();
            ((System.ComponentModel.ISupportInitialize)numericUpDownXend).EndInit();
            ((System.ComponentModel.ISupportInitialize)numericUpDownYstart).EndInit();
            ((System.ComponentModel.ISupportInitialize)numericUpDownXstart).EndInit();
            ((System.ComponentModel.ISupportInitialize)pictureBox2).EndInit();
            tabPageDebug.ResumeLayout(false);
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private Label action;
        private Button btnGetDetect;
        private Button btnLedTest;
        private PictureBox pictureBox1;
        private Label action_name;
        private Label label1;
        private Label lb_confidence;
        private TabControl tabControl;
        private TabPage tabPageStreaming;
        private TabPage tabPageSettings;
        private TabPage tabPageDebug;
        private Button btnGetDetectRoi;
        private PictureBox pictureBox2;
        private Label label2;
        private GroupBox groupBox1;
        private Button btnApply;
        private Label label4;
        private Label label5;
        private Label label3;
        private Button btnReset;
        private TableLayoutPanel tableLayoutPanel1;
        private Button button3;
        private NumericUpDown numericUpDownXstart;
        private NumericUpDown numericUpDownYend;
        private NumericUpDown numericUpDownXend;
        private NumericUpDown numericUpDownYstart;
    }
}
