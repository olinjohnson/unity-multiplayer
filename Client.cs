using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using System.Net.Sockets;
using System.Text;
using Newtonsoft.Json;

public class ClientController : MonoBehaviour
{
    private int port = 7622;
    private string host = "127.0.0.1";

    private TcpClient client;
    private NetworkStream ns;

    private Rigidbody player;

    public GameObject playerPrefab;

    private string username;

    // Start is called before the first frame update
    void Start()
    {
        // Initialize client and network stream
        client = new TcpClient(host, port);
        ns = client.GetStream();

        // Store reference to the player
        player = GameObject.Find("player").GetComponent<Rigidbody>();

        // Initial connection message containing name
        username = "me";
        ns.Write(Encoding.ASCII.GetBytes(username), 0, username.Length);
    }

    void FixedUpdate()
    {
        // Create player instance of self to send to server
        Player self = new Player()
        {
            username = username,
            position = new float[]
            {
                player.transform.position.x,
                player.transform.position.y,
                player.transform.position.z
            }
        };
        // Send to server
        string serializedPacket = JsonConvert.SerializeObject(self);
        ns.Write(Encoding.ASCII.GetBytes(serializedPacket), 0, serializedPacket.Length);

        // Read response from server about other players and store players in a list
        byte[] buffer = new byte[1024];
        int bytesRead = ns.Read(buffer, 0, buffer.Length);
        string parsedBuffer = Encoding.ASCII.GetString(buffer).Substring(0, bytesRead);
        try
        {
            List<Player> deserializedBuffer = JsonConvert.DeserializeObject<List<Player>>(parsedBuffer);
            UpdatePlayers(deserializedBuffer);
        }
        catch
        {
            Debug.Log("Couldn't update");
        }
    }

    // Function to update the positions of other players
    void UpdatePlayers(List<Player> p)
    {
        foreach (Player otherPlayer in p)
        {
            if (GameObject.Find(otherPlayer.username) == null)
            {
                GameObject newPlayer = Instantiate(playerPrefab, new Vector3(0, 5.65f, 0), Quaternion.identity);
                newPlayer.name = otherPlayer.username;
            }
            else
            {
                Vector3 GOPosition = new Vector3(otherPlayer.position[0], otherPlayer.position[1], otherPlayer.position[2]);
                GameObject.Find(otherPlayer.username).GetComponent<Rigidbody>().transform.position = GOPosition;
            }
        }
    }

    void OnApplicationQuit()
    {
        ns.Close();
    }
}

// Player class
class Player
{
    public string username;
    public float[] position;
}
