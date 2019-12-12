namespace Gsnll.Models.Matchmaking.Incoming
{
    internal sealed class MatchmakingIncomingKickMessage : MatchmakingIncomingSimpleMessage
    {
        public MatchmakingIncomingKickMessage(string message) : base("kick", message) { }
    }
}