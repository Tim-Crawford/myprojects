namespace Gsnll.Models.Matchmaking.Incoming
{
    internal abstract class MatchmakingIncomingSimpleMessage : MatchmakingIncomingMessage<MatchmakingIncomingSimpleMessage.MessageData>
    {
        public override MessageData Data { get; }

        protected MatchmakingIncomingSimpleMessage(string messageType, string message) : base(messageType)
        {
            this.Data = new MessageData(message);
        }

        public sealed class MessageData : IMatchmakingIncomingData
        {
            public string Message { get; }

            public MessageData(string message)
            {
                this.Message = message;
            }
        }
    }
}