using Newtonsoft.Json;

namespace Gsnll.Models.GameServer.Outgoing
{
    internal sealed class GameServerOutgoingGameStateMessage<TState> : GameServerOutgoingMessage, IMessageWithData<GameServerOutgoingGameStateMessage<TState>.MessageData>
    {
        [JsonProperty("data")]
        public MessageData Data { get; }

        [JsonConstructor]
        public GameServerOutgoingGameStateMessage(TState state) : base("game-state")
        {
            this.Data = new MessageData(state);
        }

        public class MessageData
        {
            [JsonProperty("state")]
            public TState GameState { get; }

            public MessageData(TState state)
            {
                this.GameState = state;
            }
        }
    }
}