using Newtonsoft.Json;
using System;
using System.IO;
using System.Net;
using System.Net.NetworkInformation;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

//SELF-MADE CLASS

namespace Helper
{
    public class Firebase
    {
        string Link;

        //Firebase Constructor
        public Firebase(string firebaseURL)
        {
            Link = firebaseURL;
        }

        //Insert data in firebase
        public async Task Insert(string jsonName, dynamic jsonValue, string directory)
        {
            await Task.Run(() => {
                string json = "{\"" + jsonName.ToString() + "\":\"" + jsonValue.ToString() + "\"}";
                WebRequest request = WebRequest.Create(Link + directory + "/.json");
                request.ContentType = "application/json";
                request.Method = "PATCH";
                byte[] buffer = Encoding.UTF8.GetBytes(json);
                request.ContentLength = buffer.Length;
                request.GetRequestStream().Write(buffer, 0, buffer.Length);
                try
                {
                    WebResponse response = request.GetResponse();
                    json = (new StreamReader(response.GetResponseStream())).ReadToEnd();
                    response.Close();
                }
                catch (System.Net.WebException error)
                {
                    Message.Default("WebException Error: " + error.Message, "Error");
                    Application.Exit();
                }
            });
        }

        public async Task InsertJSON(string json, string directory)
        {
            await Task.Run(() => {
                WebRequest request = WebRequest.Create(Link + directory + "/.json");
                request.ContentType = "application/json";
                request.Method = "PATCH";
                byte[] buffer = Encoding.UTF8.GetBytes(json);
                request.ContentLength = buffer.Length;
                request.GetRequestStream().Write(buffer, 0, buffer.Length);
                try
                {
                    WebResponse response = request.GetResponse();
                    json = (new StreamReader(response.GetResponseStream())).ReadToEnd();
                    response.Close();
                }
                catch (System.Net.WebException error)
                {
                    Message.Default("WebException Error: " + error.Message, "Error");
                    Application.Exit();
                }
            });
        }

        //Receive data in firebase
        public async Task<dynamic> Receive(string directory)
        {
            object values = null;
            await Task.Run(() => {
                string firebaseURL = Link + directory + "/.json";
                HttpWebRequest request1 = (HttpWebRequest)WebRequest.Create(firebaseURL);
                request1.ContentType = "application/json: charset=utf-8";
                HttpWebResponse response1 = request1.GetResponse() as HttpWebResponse;
                using (Stream responsestream = response1.GetResponseStream())
                {
                    StreamReader Read = new StreamReader(responsestream, Encoding.UTF8);
                    values = JsonConvert.DeserializeObject(Read.ReadToEnd());
                }
            });
            return values;
        }

        //Delete data in firebase
        public async Task Delete(string directory)
        {
            await Task.Run(() => {
                WebRequest request = WebRequest.Create(Link + directory + "/.json");
                request.ContentType = "application/json";
                request.Method = "DELETE";
                WebResponse response = request.GetResponse();
                response.Close();
            });
        }
    }

    public class Check
    {
        //Check internet connection
        public static bool InternetConnection()
        {
            bool connection = NetworkInterface.GetIsNetworkAvailable();
            if (connection == true)
            {
                return true;
            }
            else
            {
                return false;
            }
        }
    }

    public class String
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

    public class Message
    {
        //Pops a default message
        public static void Default(string message, string caption)
        {
            MessageBox.Show(message, caption);
        }

        //Pops an information message
        public static void Information(string message, string caption)
        {
            MessageBox.Show(message, caption, MessageBoxButtons.OK, MessageBoxIcon.Information);
        }

        //Pops an error message
        public static void Error(string message, string caption)
        {
            MessageBox.Show(message, caption, MessageBoxButtons.OK, MessageBoxIcon.Error);
        }

        //Pops a question message
        public static DialogResult Question(string message, string caption)
        {
            return MessageBox.Show(message, caption, MessageBoxButtons.YesNo);
        }

        //Pops a warning message
        public static void Warning(string message, string caption)
        {
            MessageBox.Show(message, caption, MessageBoxButtons.OK, MessageBoxIcon.Warning);
        }
    }
}
