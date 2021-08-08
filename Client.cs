using System;
using System.Net;
using System.Net.Sockets;
using System.Text;

class Client
{
    static void Main(string[] args)
    {
        int port = 7622;
        string host = "127.0.0.1";

        //Initialize empty byte array to use as buffer
        byte[] buffer = new byte[1024];

        //Connection class
        TcpClient client = new TcpClient(host, port);

        //Class for data transfer over socket
        NetworkStream ns = client.GetStream();

        while (true)
        {
            Console.WriteLine("Message: ");
            string data = Console.ReadLine();
            buffer = Encoding.ASCII.GetBytes(data);
            ns.Write(buffer, 0, buffer.Length);

            ns.Read(buffer, 0, buffer.Length);
            Console.WriteLine(Encoding.ASCII.GetString(buffer));
        }
    }
}