using System;
using System.Threading.Tasks;
using Gsnll;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace Sample
{
    class Program
    {
        private static async Task Main(string[] args)
        {
            Console.WriteLine("Who are you?");
            string name = Console.ReadLine();

            Console.WriteLine("Entering a match...");
            GsnllClient client = new GsnllClient("127.0.0.1", 8000);
            using (GsnllLobby<DefaultGameState, DefaultClientInfo> lobby = await client.EnterMatchAsync(new DefaultGameManager(), name))
            {
                Console.WriteLine("Found a match!");
                await lobby.Play(new DefaultClientInfo(lobby.ClientId));
            }

            Console.WriteLine("Done");
        }
    }

    internal class DefaultGameManager : IGsnllGameManager<DefaultGameState, DefaultClientInfo>
    {
        public string GameName => "default";

        public string SerializeState(DefaultGameState gameState) {
            return JsonConvert.SerializeObject(gameState);
        }

        public string SerializeClientInfo(DefaultClientInfo clientInfo) {
            return JsonConvert.SerializeObject(clientInfo);
        }

        public DefaultGameState DeserializeState(JToken data) {
            return data.ToObject<DefaultGameState>();
        }

        public DefaultClientInfo DeserializeClientInfo(JToken data) {
            return data.ToObject<DefaultClientInfo>();
        }
    }

    internal class DefaultGameState
    {
        [JsonProperty("test")]
        public string Test { get; }

        [JsonConstructor]
        public DefaultGameState(string test)
        {
            this.Test = test;
        }
    }

    internal class DefaultClientInfo
    {
        [JsonProperty("id")]
        public string Id { get; }

        [JsonConstructor]
        public DefaultClientInfo(string id)
        {
            this.Id = id;
        }
    }
}
