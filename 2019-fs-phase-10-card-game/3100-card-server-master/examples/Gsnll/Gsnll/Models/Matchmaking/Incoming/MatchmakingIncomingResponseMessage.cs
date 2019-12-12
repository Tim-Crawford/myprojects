namespace Gsnll.Models.Matchmaking.Incoming
{
    internal sealed class MatchmakingIncomingResponseMessage : MatchmakingIncomingSimpleMessage
    {
        public MatchmakingIncomingResponseMessage(string message) : base("response", message) { }
    }
}