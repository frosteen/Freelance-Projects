using System.Collections.Generic;
using System.Data.SQLite;
using System.IO;
using System.Text;

namespace LijaucoDentist
{
    class DatabaseSQLite
    {
        public SQLiteConnection sqlite_conn;
        public SQLiteCommand sqlite_cmd;
        public SQLiteDataReader sqlite_datareader;

        public DatabaseSQLite(string databaseName, string password)
        {
            if (!File.Exists(databaseName))
            {
                sqlite_conn = new SQLiteConnection("Data Source=" + databaseName + ";Version=3;New=True;Compressed=True;");
                //sqlite_conn.SetPassword(password);
            }
            else
            {
                sqlite_conn = new SQLiteConnection("Data Source=" + databaseName + ";Version=3;New=False;Compressed=True;");
                //sqlite_conn.SetPassword("");
            }
        }

        public void CREATE(string tableName, string command)
        {
            try
            {
                MakeQuery("CREATE TABLE " + tableName + " (" + command + ");");
            }
            catch { sqlite_conn.Close(); }
        }

        public List<Dictionary<string, string>> SELECT(string tableName, string uniqueName, string orderBy)
        {
            sqlite_conn.Open();
            sqlite_cmd = sqlite_conn.CreateCommand();
            if (uniqueName != null)
            {
                if (orderBy != null)
                {
                    sqlite_cmd.CommandText = "SELECT * FROM " + tableName + " WHERE " + uniqueName + " ORDER BY " + orderBy + ";";
                } else
                {
                    sqlite_cmd.CommandText = "SELECT * FROM " + tableName + " WHERE " + uniqueName + ";";
                }
            } else
            {
                if (orderBy != null)
                {
                    sqlite_cmd.CommandText = "SELECT * FROM " + tableName + " ORDER BY " + orderBy +  ";";
                }
                else
                {
                    sqlite_cmd.CommandText = "SELECT * FROM " + tableName + ";";
                }
            }
            sqlite_datareader = sqlite_cmd.ExecuteReader();
            List<Dictionary<string, string>> results = new List<Dictionary<string, string>>();
            while(sqlite_datareader.Read())
            {
                Dictionary<string, string> rows = new Dictionary<string, string>();
                for (int i = 0; i < sqlite_datareader.FieldCount; i++)
                {
                    rows.Add(sqlite_datareader.GetName(i).ToString(), sqlite_datareader[i].ToString());
                }
                results.Add(rows);
            }
            sqlite_datareader.Close();
            sqlite_conn.Close();
            return results;
        }

        public void INSERT(string tableName, string[] columnNames, string[] valueNames)
        {
            sqlite_conn.Open();
            sqlite_cmd = sqlite_conn.CreateCommand();
            string modifiedLabel = "";
            string modifiedValue = "";
            StringBuilder generate = new StringBuilder();
            modifiedLabel += "(";
            foreach (string v in columnNames)
            {
                generate.Append(string.Format("{0},", v));
            }
            modifiedLabel += generate.ToString();
            modifiedLabel = modifiedLabel.Remove(modifiedLabel.Length-1);
            modifiedLabel += ")";
            modifiedValue += "(";
            generate.Clear();
            foreach (string v in valueNames)
            {
               generate.Append(string.Format("'{0}',", v));
            }
            modifiedValue += generate.ToString();
            modifiedValue = modifiedValue.Remove(modifiedValue.Length - 1);
            modifiedValue += ")";
            try
            {
                sqlite_cmd.CommandText = string.Format("INSERT INTO {0} {1} VALUES {2};", tableName,
                    modifiedLabel, modifiedValue);
                sqlite_cmd.ExecuteNonQuery();
            }
            catch
            {
                generate.Clear();
                modifiedLabel = "";
                for (int i = 1; i < columnNames.Length; i++)
                {
                    generate.Append(string.Format("{0}='{1}',", columnNames[i], valueNames[i]));
                }
                modifiedLabel += generate.ToString();
                modifiedLabel = modifiedLabel.Remove(modifiedLabel.Length - 1);
                sqlite_cmd.CommandText = string.Format("UPDATE {0} SET {1} WHERE {2};", tableName,
                    modifiedLabel, columnNames[0]+"="+"'"+valueNames[0]+"'");
                sqlite_cmd.ExecuteNonQuery();
            }
            sqlite_conn.Close();
        }

        public void DELETE(string tableName, string uniqueName)
        {
            try
            {
                MakeQuery(string.Format("DELETE FROM {0} WHERE {1};", tableName, uniqueName));
            }
            catch { sqlite_conn.Close(); }
        }

        public void DROPTABLE(string tableName)
        {
            try
            {
                MakeQuery(string.Format("DROP TABLE {0};", tableName));
            }
            catch { sqlite_conn.Close(); }
        }

        public void MakeQuery(string command)
        {
            sqlite_conn.Open();
            sqlite_cmd = sqlite_conn.CreateCommand();
            sqlite_cmd.CommandText = command;
            sqlite_cmd.ExecuteNonQuery();
            sqlite_conn.Close();
        }
    }
}
