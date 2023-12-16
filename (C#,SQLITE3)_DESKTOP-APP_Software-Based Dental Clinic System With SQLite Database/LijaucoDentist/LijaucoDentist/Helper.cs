using System;
using System.Reflection;
using System.Windows.Forms;

//SELF-MADE CLASS

namespace Helper
{
    public class Str
    {
        //String replace
        public static string Replace(string text, string whatToReplace, string theReplace)
        {
            string modString = text.ToString();
            modString = modString.Replace(whatToReplace, theReplace);
            return modString;
        }

        //String split
        public static string[] Split(string stringToBeSplit, string[] splits)
        {
            string[] splitThisBes = stringToBeSplit.ToString().Split(splits, StringSplitOptions.RemoveEmptyEntries);
            return splitThisBes;
        }
    }

    public class Msg
    {
        //Pops a default message
        public static void Default(string message, string caption)
        {
            MessageBox.Show(message, caption);
        }

        //Pops an information message
        public static void Information(string message, string caption)
        {
            //MessageBox.Show(message, caption, MessageBoxButtons.OK, MessageBoxIcon.Information);
            Default(message, caption);
        }

        //Pops an error message
        public static void Error(string message, string caption)
        {
            MessageBox.Show(message, caption, MessageBoxButtons.OK, MessageBoxIcon.Error);
        }

        //Pops a question message
        public static DialogResult Question(string message, string caption)
        {
            return MessageBox.Show(message, caption, MessageBoxButtons.YesNo, MessageBoxIcon.None);
        }

        //Pops a warning message
        public static void Warning(string message, string caption)
        {
            MessageBox.Show(message, caption, MessageBoxButtons.OK, MessageBoxIcon.Warning);
        }
    }

    public class ThreadLib
    {
        //Create an anonymous multithreading
        public static void Create(Action func)
        {
            System.Threading.ThreadStart tref = new System.Threading.ThreadStart(func);
            System.Threading.Thread t = new System.Threading.Thread(tref);
            //t.SetApartmentState(System.Threading.ApartmentState.STA);
            t.Start();
        }

        public static void AddRow(Form f, DataGridView ctrl, string[] text)
        {
            if (ctrl.InvokeRequired)
            {
                AddRowCallBack method = new AddRowCallBack(AddRow);
                f.Invoke(method, new object[] { f, ctrl, text });
            }
            else
            {
                ctrl.Rows.Add(text);
            }
        }

        public static void AddValueToRow(Form f, DataGridView ctrl, int count, int cell, string value)
        {
            if (ctrl.InvokeRequired)
            {
                AddValueToRowCallBack method = new AddValueToRowCallBack(AddValueToRow);
                f.Invoke(method, new object[] { f, ctrl, count, cell, value });
            }
            else
            {
                ctrl.Rows[count].Cells[cell].Value = value;
            }
        }

        public static void AddItemsList(Form f, dynamic ctrl, string text)
        {
            if (ctrl.InvokeRequired)
            {
                AddItemsListCallBack method = new AddItemsListCallBack(AddItemsList);
                f.Invoke(method, new object[] { f, ctrl, text });
            }
            else
            {
                ctrl.Items.Add(text);
            }
        }

        public static void ClearItemsList(Form form, dynamic ctrl)
        {
            if (ctrl.InvokeRequired)
            {
                ClearItemsListCallBack method = new ClearItemsListCallBack(ClearItemsList);
                form.Invoke(method, new object[] { form, ctrl });
            }
            else
            {
                ctrl.Items.Clear();
            }
        }

        public static void ClearRow(Form f, DataGridView ctrl)
        {
            if (ctrl.InvokeRequired)
            {
                ClearRowCallBack method = new ClearRowCallBack(ClearRow);
                f.Invoke(method, new object[] { f, ctrl });
            }
            else
            {
                ctrl.Rows.Clear();
                ctrl.Refresh();
            }
        }

        public static void ControlsClear(Form f, dynamic ctrl)
        {
            if (ctrl.InvokeRequired)
            {
                ControlsClearCallBack method = new ControlsClearCallBack(ControlsClear);
                f.Invoke(method, new object[] { f, ctrl });
            }
            else
            {
                ctrl.Controls.Clear();
            }
        }

        public static void ControlsAdd(Form f, dynamic ctrl, Control cntrl)
        {
            if (ctrl.InvokeRequired)
            {
                ControlsAddCallBack method = new ControlsAddCallBack(ControlsAdd);
                f.Invoke(method, new object[] { f, ctrl, cntrl });
            }
            else
            {
                ctrl.Controls.Add(cntrl);
            }
        }

        //Read property in multithreading
        public static dynamic ReadProperty(Form f, dynamic varControl, string property)
        {
            if (varControl.InvokeRequired)
            {
                dynamic res = "";
                Action<dynamic> action = new Action<dynamic>(c =>
                res = varControl.GetType().GetProperty(property, BindingFlags.Instance | BindingFlags.Public | BindingFlags.IgnoreCase).GetValue(varControl, null));
                f.Invoke(action, varControl);
                return res.ToString();
            }
            dynamic varText = varControl.GetType().GetProperty(property, BindingFlags.Instance | BindingFlags.Public | BindingFlags.IgnoreCase).GetValue(varControl, null);
            return varText.ToString();
        }

        //Set property in multithreading
        public static void SetProperty(dynamic f, dynamic ctrl, string property, dynamic text)
        {
            if (ctrl.InvokeRequired)
            {
                SetPropertyCallBack method = new SetPropertyCallBack(SetProperty);
                f.Invoke(method, new object[] { f, ctrl, property, text });
            }
            else
            {
                ctrl.GetType().GetProperty(property, BindingFlags.Instance | BindingFlags.Public | BindingFlags.IgnoreCase).SetValue(ctrl, text, null);

            }
        }

        private delegate void SetPropertyCallBack(dynamic f, dynamic ctrl, string property, dynamic text);

        private delegate void AddRowCallBack(Form f, DataGridView ctrl, string[] text);

        private delegate void AddItemsListCallBack(Form f, dynamic ctrl, string text);

        private delegate void ControlsAddCallBack(Form f, dynamic ctrl, Control cntrl);

        private delegate void ClearItemsListCallBack(Form f, dynamic ctrl);

        private delegate void ControlsClearCallBack(Form f, dynamic ctrl);

        private delegate void AddValueToRowCallBack(Form f, DataGridView ctrl, int count, int cell, string value);

        private delegate void ClearRowCallBack(Form f, DataGridView ctrl);
    }
}
