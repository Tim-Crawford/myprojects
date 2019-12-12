namespace Gsnll.Models.GameServer.Incoming
{
    internal sealed class GameServerIncomingErrorMessage<TState> : GameServerIncomingMessage, IMessageWithData<GameServerIncomingErrorMessage<TState>.MessageData>
    {
        public MessageData Data { get; }

        public GameServerIncomingErrorMessage(string message, string reason, TState state) : base("error")
        {
            this.Data = new MessageData(message, reason, state);
        }

        public sealed class MessageData
        {
            public string Message { get; }
            public string Reason { get; }
            public TState State { get; }

            public MessageData(string message, string reason, TState state)
            {
                this.Message = message;
                this.Reason = reason;
                this.State = state;
            }
        }
    }
}