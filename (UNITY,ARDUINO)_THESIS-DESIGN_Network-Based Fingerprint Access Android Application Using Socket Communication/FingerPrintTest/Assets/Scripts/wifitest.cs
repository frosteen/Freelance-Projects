using UnityEngine;                        // These are the librarys being used
using System.Collections;
using System;
using System.IO;
using System.Net.Sockets;

public class wifitest : MonoBehaviour
{

    bool socketReady = false;                // global variables are setup here
    TcpClient mySocket;
    public NetworkStream theStream;
    StreamWriter theWriter;
    StreamReader theReader;
    public String Host = "192.168.1.200";
    public Int32 Port = 5001;

    Camera cam;

    void Start()
    {               // setup the server connection when the program starts

        cam = GetComponent<Camera>();
        cam.clearFlags = CameraClearFlags.SolidColor;
        setupSocket();
        Debug.Log("connected.");
    }

    // Update is called once per frame
    void Update()
    {
        setupSocket();
        System.Threading.Thread.Sleep(500);
        while (theStream.DataAvailable)
        {                  // if new data is recieved from Arduino
            string recievedData = readSocket();            // write it to a string
            Debug.Log(recievedData);
            if (recievedData == "Verified ID:4")
            {
                cam.backgroundColor = Color.blue;
            } else
            {
                cam.backgroundColor = Color.red;
            }

        }
    }

    public void setupSocket()
    {                            // Socket setup here
        try
        {
            mySocket = new TcpClient(Host, Port);
            theStream = mySocket.GetStream();
            theWriter = new StreamWriter(theStream);
            theReader = new StreamReader(theStream);
            socketReady = true;
        }
        catch (Exception e)
        {
            Debug.Log("Socket error:" + e);                // catch any exceptions
        }
    }

    public void writeSocket(string theLine)
    {            // function to write data out
        if (!socketReady)
            return;
        String tmpString = theLine;
        theWriter.Write(tmpString);
        theWriter.Flush();


    }

    public String readSocket()
    {                        // function to read data in
        if (!socketReady)
            return "";
        if (theStream.DataAvailable)
            return theReader.ReadLine();
        return "NoData";
    }

    public void closeSocket()
    {                            // function to close the socket
        if (!socketReady)
            return;
        theWriter.Close();
        theReader.Close();
        mySocket.Close();
        socketReady = false;
    }

    public void maintainConnection()
    {                    // function to maintain the connection (not sure why! but Im sure it will become a solution to a problem at somestage)
        if (!theStream.CanRead)
        {
            setupSocket();
        }
    }


} // end class