namespace Gsnll.Models.Matchmaking.Incoming
{
    internal sealed class MatchmakingIncomingConnectMessage : MatchmakingIncomingSimpleMessage
    {
        public MatchmakingIncomingConnectMessage(string message) : base("connect", message) { }
    }
}