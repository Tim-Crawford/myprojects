using Newtonsoft.Json;

namespace Gsnll.Models.Matchmaking.Incoming
{
    internal abstract class MatchmakingIncomingMessage<TData> : IMessageWithData<TData>, IMatchmakingIncomingMessage where TData : IMatchmakingIncomingData
    {
        public string MessageType { get; }
        public abstract TData Data { get; }

        protected MatchmakingIncomingMessage(string messageType) {
            this.MessageType = messageType;
        }
    }
}