namespace Gsnll.Models.GameServer.Incoming {
    internal sealed class GameServerIncomingGameStateMessage<TState> : GameServerIncomingMessage, IMessageWithData<GameServerIncomingGameStateMessage<TState>.MessageData>
    {
        public MessageData Data { get; }

        public GameServerIncomingGameStateMessage(TState gameState) : base("client-info")
        {
            this.Data = new MessageData(gameState);
        }

        public sealed class MessageData
        {
            public TState GameState { get; }

            public MessageData(TState gameState)
            {
                this.GameState = gameState;
            }
        }
    }
}