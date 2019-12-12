using System;
using Gsnll.Models.GameServer.Incoming;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace Gsnll.Models.GameServer.JsonConverters
{
    internal class GameServerIncomingMessageConverter<TState, TClientInfo> : IncomingMessageConverter<IGameServerIncomingMessage>
    {
        private readonly IGsnllGameManager<TState, TClientInfo> _gameManager;

        public GameServerIncomingMessageConverter(IGsnllGameManager<TState, TClientInfo> gameManager)
        {
            this._gameManager = gameManager;
        }

        protected override IGameServerIncomingMessage ReadMessage(JObject obj, string messageType)
        {
            switch (messageType)
            {
                case "whois":
                {
                    if (!this.TryGetObjectToken(obj, "data", out JObject data))
                    {
                        throw new Exception("Invalid JSON: #/data must be an object.");
                    }

                    if (!this.TryGetValue(data, "id", out int id))
                    {
                        throw new Exception("Invalid JSON: #/data/id must be an integer.");
                    }

                    return new GameServerIncomingWhoisMessage(id);
                }

                case "client-info":
                {
                    if (!this.TryGetObjectToken(obj, "data", out JObject data))
                    {
                        throw new Exception("Invalid JSON: #/data must be an object.");
                    }

                    if (!this.TryGetValue(data, "id", out int id))
                    {
                        throw new Exception("Invalid JSON: #/data/id must be an integer.");
                    }

                    if (!this.TryGetToken(data, "clientInfo", out JToken clientInfoToken))
                    {
                        throw new Exception("Invalid JSON: #/data/state is missing.");
                    }

                    return new GameServerIncomingClientInfoMessage<TClientInfo>(id, this._gameManager.DeserializeClientInfo(clientInfoToken));
                }

                case "game-state":
                {
                    if (!this.TryGetObjectToken(obj, "data", out JObject data))
                    {
                        throw new Exception("Invalid JSON: #/data must be an object.");
                    }

                    if (!this.TryGetToken(data, "state", out JToken stateToken))
                    {
                        throw new Exception("Invalid JSON: #/data/state is missing.");
                    }

                    return new GameServerIncomingGameStateMessage<TState>(this._gameManager.DeserializeState(stateToken));
                }

                case "game-finished":
                {
                    return new GameServerIncomingGameFinishedMessage();
                }

                case "disconnect":
                {
                    return new GameServerIncomingDisconnectMessage();
                }

                case "client-list":
                {
                    throw new NotImplementedException();
                }

                case "client-disconnected":
                {
                    if (!this.TryGetObjectToken(obj, "data", out JObject data))
                    {
                        throw new Exception("Invalid JSON: #/data must be an object.");
                    }

                    if (!this.TryGetValue(data, "id", out int id))
                    {
                        throw new Exception("Invalid JSON: #/data/id must be an integer.");
                    }

                    if (!this.TryGetToken(data, "clientInfo", out JToken clientInfoToken))
                    {
                        throw new Exception("Invalid JSON: #/data/state is missing.");
                    }

                    return new GameServerIncomingClientDisconnectedMessage<TClientInfo>(id, this._gameManager.DeserializeClientInfo(clientInfoToken));
                }

                case "random-data":
                {
                    throw new NotImplementedException();
                }

                case "error":
                {
                    if (!this.TryGetObjectToken(obj, "data", out JObject data))
                    {
                        throw new Exception("Invalid JSON: #/data must be an object.");
                    }

                    if (!this.TryGetValue(data, "reason", out string reason))
                    {
                        throw new Exception("Invalid JSON: #/data/reason must be a string.");
                    }

                    // Optional message
                    this.TryGetValue(data, "message", out string message);

                    if (!this.TryGetToken(data, "state", out JToken stateToken))
                    {
                        throw new Exception("Invalid JSON: #/data/state is missing.");
                    }

                    return new GameServerIncomingErrorMessage<TState>(reason, message, this._gameManager.DeserializeState(stateToken));
                }

                default:
                {
                    throw new Exception($"Unknown message type: ${messageType}");
                }
            }
        }
    }
}
