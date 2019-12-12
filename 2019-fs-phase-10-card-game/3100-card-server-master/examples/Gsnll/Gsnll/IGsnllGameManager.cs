using Newtonsoft.Json.Linq;

namespace Gsnll {
    public interface IGsnllGameManager<TState, TClientInfo> {
        string GameName { get; }

        string SerializeState(TState gameState);
        string SerializeClientInfo(TClientInfo clientInfo);

        TState DeserializeState(JToken data);
        TClientInfo DeserializeClientInfo(JToken data);
    }
}