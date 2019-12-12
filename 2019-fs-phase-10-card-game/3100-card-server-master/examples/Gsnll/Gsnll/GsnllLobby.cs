using System;
using System.Net.Sockets;
using System.Threading;
using System.Threading.Tasks;
using Gsnll.Extensions;
using Gsnll.Models.GameServer.Incoming;
using Gsnll.Models.GameServer.JsonConverters;
using Gsnll.Models.GameServer.Outgoing;
using Newtonsoft.Json;

namespace Gsnll
{
    public sealed class GsnllLobby<TState, TClientInfo> : IDisposable
    {
        private readonly TcpClient _tcpClient;
        private readonly NetworkStream _tcpStream;
        private readonly CancellationTokenSource _stoppedTokenSource;

        public string ClientId { get; }
        public IGsnllGameManager<TState, TClientInfo> GameManager { get; }
        public TState GameState { get; private set; }
        public TClientInfo ClientInfo { get; private set; }

        public GsnllLobby(TcpClient tcpClient, string clientId, IGsnllGameManager<TState, TClientInfo> gameManager)
        {
            this._tcpClient = tcpClient;
            this._tcpStream = tcpClient.GetStream();
            this.ClientId = clientId;
            this.GameManager = gameManager;
            this._stoppedTokenSource = new CancellationTokenSource();
        }

        public async Task Play(TClientInfo clientInfo, CancellationToken cancellation = default)
        {
            this.ClientInfo = clientInfo;
            using (CancellationTokenSource linkedTokenSource = CancellationTokenSource.CreateLinkedTokenSource(this._stoppedTokenSource.Token, cancellation))
            {
                await Task.WhenAny(
                    this.Listen(linkedTokenSource.Token),
                    this.MonitorConnection(linkedTokenSource.Token)
                );
            }
        }

        private async Task Listen(CancellationToken cancellation = default)
        {
            JsonConverter[] converters = { new GameServerIncomingMessageConverter<TState, TClientInfo>(this.GameManager) };

            try
            {
                while (!cancellation.IsCancellationRequested && this._tcpClient.Connected)
                {
                    try
                    {
                        // Read a message from the server
                        IGameServerIncomingMessage message = await this._tcpStream.ReadJsonAsync<IGameServerIncomingMessage>(converters, cancellation).ConfigureAwait(false);

                        // Process the message
                        switch (message)
                        {
                            case GameServerIncomingWhoisMessage whoisMessage:
                            {
                                // Send client info message to server
                                await this.UpdateClientInfo(this.ClientInfo, cancellation).ConfigureAwait(false);
                                break;
                            }

                            case GameServerIncomingDisconnectMessage disconnectMessage:
                            {
                                this.Stop();
                                break;
                            }

                            case GameServerIncomingErrorMessage<TState> errorMessage:
                            {
                                throw new Exception($"An error occurred while playing the game: {errorMessage.Data.Reason} - {errorMessage.Data.Message ?? "?"}");
                            }

                            default:
                            {
                                Console.WriteLine($"Unexpected message: {message.MessageType}");
                                break;
                            }
                        }
                    }
                    catch (NotImplementedException) { }
                }
            }
            catch (OperationCanceledException) { }
        }

        private async Task MonitorConnection(CancellationToken cancellation = default)
        {
            try
            {
                // Check every second if connected
                while (this._tcpClient.Connected)
                {
                    await Task.Delay(1000, cancellation).ConfigureAwait(false);
                }

                if (!cancellation.IsCancellationRequested)
                {
                    this.Stop();
                }
            }
            catch (OperationCanceledException) { }
        }

        public Task UpdateClientInfo(TClientInfo clientInfo, CancellationToken cancellation = default)
        {
            this.ClientInfo = clientInfo;
            return this._tcpStream.WriteJsonAsync(new GameServerOutgoingClientInfoMessage<TClientInfo>(this.ClientInfo), cancellation);
        }

        public void Stop()
        {
            this._stoppedTokenSource.Cancel();
            this._tcpClient.Close();
        }

        public void Dispose()
        {
            this._tcpClient?.Dispose();
        }

        private void OnStateReceived(StateReceivedEventArgs<TState> e)
        {
            this.StateReceived?.Invoke(this, e);
        }

        private void OnClientInfoReceived(TClientInfo e)
        {
            this.ClientInfoReceived?.Invoke(this, e);
        }

        public event EventHandler<StateReceivedEventArgs<TState>> StateReceived;
        public event EventHandler<TClientInfo> ClientInfoReceived;
    }

    public class StateReceivedEventArgs<TState> : EventArgs
    {
        public TState PreviousState { get; }
        public TState NewState { get; }

        public StateReceivedEventArgs(TState previousState, TState newState)
        {
            this.PreviousState = previousState;
            this.NewState = newState;
        }
    }

    public class ClientInfoReceivedEventArgs<TClientInfo> : EventArgs
    {

    }
}