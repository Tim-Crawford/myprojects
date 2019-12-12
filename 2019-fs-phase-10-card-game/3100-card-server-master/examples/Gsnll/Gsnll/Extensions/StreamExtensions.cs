using System;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using Gsnll.Models;
using Newtonsoft.Json;

namespace Gsnll.Extensions
{
    internal static class StreamExtensions
    {
        public static Task WriteJsonAsync<TData>(this Stream stream, IMessageWithData<TData> value, CancellationToken cancellation = default)
        {
            return stream.WriteJsonAsync(JsonConvert.SerializeObject(value, Formatting.None), cancellation);
        }

        public static Task WriteJsonAsync<TData>(this Stream stream, IMessageWithData<TData> value, JsonConverter[] converters, CancellationToken cancellation = default)
        {
            return stream.WriteJsonAsync(JsonConvert.SerializeObject(value, Formatting.None, converters), cancellation);
        }

        private static async Task WriteJsonAsync(this Stream stream, string serialized, CancellationToken cancellation = default)
        {
            Console.WriteLine($"Sending message: {serialized}");

            // Convert everything into byte arrays
            byte[] jsonBytes = Encoding.UTF8.GetBytes("JSON");
            byte[] lengthBytes = BitConverter.GetBytes(serialized.Length);
            byte[] serializedBytes = Encoding.UTF8.GetBytes(serialized);

            // Send all the data
            await stream.WriteAsync(jsonBytes, 0, jsonBytes.Length, cancellation);
            await stream.WriteAsync(lengthBytes, 0, lengthBytes.Length, cancellation);
            await stream.WriteAsync(serializedBytes, 0, serializedBytes.Length, cancellation);
        }

        public static Task<T> ReadJsonAsync<T>(this Stream stream, CancellationToken cancellation = default)
        {
            return stream.ReadJsonAsync<T>(new JsonConverter[0], cancellation);
        }

        public static async Task<T> ReadJsonAsync<T>(this Stream stream, JsonConverter[] converters, CancellationToken cancellation = default)
        {
            byte[] buffer = await stream.ReadBytesAsync(4, cancellation);

            // Skip until a valid JSON message is reached
            byte[] expected = Encoding.UTF8.GetBytes("JSON");
            while (!expected.SequenceEqual(buffer))
            {
                Console.WriteLine($"Skipping byte, current buffer value is '{Encoding.UTF8.GetString(buffer)}'.");

                // Shift buffer down
                for (int i = 0; i < buffer.Length; i++)
                {
                    buffer[i] = buffer[i + 1];
                }

                // Read an additional byte into the buffer
                byte[] newByte = await stream.ReadBytesAsync(1, cancellation);
                buffer[buffer.Length - 1] = newByte[0];
            }

            // Get length
            buffer = await stream.ReadBytesAsync(4, cancellation);
            int length = BitConverter.ToInt32(buffer, 0);

            // Get JSON data
            buffer = await stream.ReadBytesAsync(length, cancellation);
            string rawData = Encoding.UTF8.GetString(buffer);
            Console.WriteLine($"Message received: '{rawData}'.");

            // Deserialize the raw data
            return JsonConvert.DeserializeObject<T>(rawData, converters);
        }

        private static async Task<byte[]> ReadBytesAsync(this Stream stream, int count, CancellationToken cancellation = default)
        {
            byte[] buffer = new byte[count];
            int offset = 0;

            while (offset < count)
            {
                if (!stream.CanRead)
                {
                    throw new ArgumentException("End of stream reached", nameof(stream));
                }

                offset += await stream.ReadAsync(buffer, offset, count - offset, cancellation);
            }

            return buffer;
        }
    }
}
