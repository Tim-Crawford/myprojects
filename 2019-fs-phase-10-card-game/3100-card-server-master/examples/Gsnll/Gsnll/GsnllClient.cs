using System;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using System.Threading.Tasks;
using Gsnll.Extensions;
using Gsnll.Models.Matchmaking.Incoming;
using Gsnll.Models.Matchmaking.Outgoing;

namespace Gsnll
{
    public sealed class GsnllClient
    {
        public IPAddress RemoteAddress { get; }
        public int RemotePort { get; }

        public GsnllClient(string remoteHostname, ushort remotePort)
        {
            if (!IPAddress.TryParse(remoteHostname, out IPAddress remoteAddress))
            {
                throw new ArgumentException("Invalid remote hostname", nameof(remoteHostname));
            }

            if (remotePort < 1024)
            {
                throw new ArgumentOutOfRangeException(nameof(remotePort), "Remote port must be between 1024-65535");
            }

            this.RemoteAddress = remoteAddress;
            this.RemotePort = remotePort;
        }

        public async Task<GsnllLobby<TState, TClientInfo>> EnterMatchAsync<TState, TClientInfo>(IGsnllGameManager<TState, TClientInfo> gameManager, string clientId, CancellationToken cancellation = default)
        {
            TcpClient tcpClient = null;
            bool successful = false;

            try
            {
                tcpClient = new TcpClient();

                // Connect to the matchmaking server
                await tcpClient.ConnectAsync(this.RemoteAddress, this.RemotePort);

                // Send connection details
                NetworkStream stream = tcpClient.GetStream();
                await stream.WriteJsonAsync(new MatchmakingConnectOutgoingMessage(new MatchmakingConnectOutgoingMessage.ConnectionData("default", new MatchmakingConnectOutgoingMessage.ClientConfiguration(clientId))), cancellation: cancellation);

                // Wait for matchmaking server response
                IMatchmakingIncomingMessage response = await stream.ReadJsonAsync<IMatchmakingIncomingMessage>(cancellation: cancellation);

                // Process response
                switch (response)
                {
                    case MatchmakingIncomingResponseMessage responseMessage:
                    {
                        Console.WriteLine("Ready to connect!");
                        break;
                    }

                    case MatchmakingIncomingErrorMessage errorMessage:
                    {
                        throw new Exception($"An error was received by the matchmaking server while connecting: {errorMessage.Data.ErrorType} - {errorMessage.Data.Message}");
                    }

                    default:
                    {
                        throw new Exception($"Unexpected message: {response.MessageType}");
                    }
                }

                // Wait until connected to a lobby
                while (!(response is MatchmakingIncomingConnectMessage))
                {
                    response = await stream.ReadJsonAsync<IMatchmakingIncomingMessage>(cancellation: cancellation);
                }

                Console.WriteLine("Connected to a lobby!");
                successful = true;
                return new GsnllLobby<TState, TClientInfo>(tcpClient, clientId, gameManager);
            }
            finally
            {
                if (!successful)
                {
                    tcpClient?.Dispose();
                }
            }
        }
    }
}
