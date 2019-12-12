namespace Gsnll.Models.Matchmaking.Incoming
{
    internal sealed class MatchmakingIncomingErrorMessage : MatchmakingIncomingMessage<MatchmakingIncomingErrorMessage.MessageData>
    {
        public override MessageData Data { get; }

        public MatchmakingIncomingErrorMessage(string message, string errorType) : base("error")
        {
            this.Data = new MessageData(message, errorType);
        }

        public sealed class MessageData : IMatchmakingIncomingData
        {
            public string Message { get; }
            public string ErrorType { get; }

            public MessageData(string message, string errorType)
            {
                this.Message = message;
                this.ErrorType = errorType;
            }
        }
    }
}