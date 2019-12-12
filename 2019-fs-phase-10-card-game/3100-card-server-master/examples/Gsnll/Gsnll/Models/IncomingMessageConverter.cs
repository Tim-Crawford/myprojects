using System;
using System.Globalization;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace Gsnll.Models
{
    internal abstract class IncomingMessageConverter<TMessage> : JsonConverter<TMessage> where TMessage : IMessage
    {
        public override bool CanWrite => false;

        public override void WriteJson(JsonWriter writer, TMessage value, JsonSerializer serializer)
        {
            throw new NotImplementedException();
        }

        public override TMessage ReadJson(JsonReader reader, Type objectType, TMessage existingValue, bool hasExistingValue, JsonSerializer serializer)
        {
            JObject obj = JObject.Load(reader);

            if (!obj.TryGetValue("messageType", StringComparison.OrdinalIgnoreCase, out JToken messageTypeToken) || !(messageTypeToken is JValue messageTypeValueToken) || !(messageTypeValueToken.Value is string messageType))
            {
                throw new Exception("Invalid JSON: #messageType must be a string.");
            }

            return this.ReadMessage(obj, messageType);
        }

        protected bool TryGetToken(JObject obj, string key, out JToken result)
        {
            return obj.TryGetValue(key, StringComparison.OrdinalIgnoreCase, out result);
        }

        protected bool TryGetValueToken(JObject obj, string key, out JValue result)
        {
            if (this.TryGetToken(obj, key, out JToken token) && token is JValue valueToken)
            {
                result = valueToken;
                return true;
            }

            result = default;
            return false;
        }

        protected bool TryGetValue<T>(JObject obj, string key, out T result)
        {
            if (this.TryGetValueToken(obj, key, out JValue valueToken))
            {
                // Try to cast the value
                if (valueToken.Value is T value)
                {
                    result = value;
                    return true;
                }

                // Try to convert the value
                if (valueToken.Value is IConvertible convertible && this.TryConvert(convertible, typeof(T), out object converted))
                {
                    result = (T)converted;
                    return true;
                }
            }

            result = default;
            return false;
        }

        protected bool TryGetObjectToken(JObject obj, string key, out JObject result)
        {
            if (this.TryGetToken(obj, key, out JToken token) && token is JObject objectToken)
            {
                result = objectToken;
                return true;
            }

            result = default;
            return false;
        }

        private bool TryConvert(IConvertible convertible, Type target, out object result)
        {
            if (target == typeof(bool))
            {
                result = convertible.ToBoolean(CultureInfo.CurrentCulture);
                return true;
            }

            if (target == typeof(byte))
            {
                result = convertible.ToByte(CultureInfo.CurrentCulture);
                return true;
            }

            if (target == typeof(char))
            {
                result = convertible.ToChar(CultureInfo.CurrentCulture);
                return true;
            }

            if (target == typeof(DateTime))
            {
                result = convertible.ToDateTime(CultureInfo.CurrentCulture);
                return true;
            }

            if (target == typeof(decimal))
            {
                result = convertible.ToDecimal(CultureInfo.CurrentCulture);
                return true;
            }

            if (target == typeof(double))
            {
                result = convertible.ToDouble(CultureInfo.CurrentCulture);
                return true;
            }

            if (target == typeof(short))
            {
                result = convertible.ToInt16(CultureInfo.CurrentCulture);
                return true;
            }

            if (target == typeof(int))
            {
                result = convertible.ToInt32(CultureInfo.CurrentCulture);
                return true;
            }

            if (target == typeof(long))
            {
                result = convertible.ToInt64(CultureInfo.CurrentCulture);
                return true;
            }

            if (target == typeof(sbyte))
            {
                result = convertible.ToSByte(CultureInfo.CurrentCulture);
                return true;
            }

            if (target == typeof(float))
            {
                result = convertible.ToSingle(CultureInfo.CurrentCulture);
                return true;
            }

            if (target == typeof(ushort))
            {
                result = convertible.ToUInt16(CultureInfo.CurrentCulture);
                return true;
            }

            if (target == typeof(uint))
            {
                result = convertible.ToUInt32(CultureInfo.CurrentCulture);
                return true;
            }

            if (target == typeof(ulong))
            {
                result = convertible.ToUInt64(CultureInfo.CurrentCulture);
                return true;
            }

            if (target == typeof(string))
            {
                result = convertible.ToString(CultureInfo.CurrentCulture);
                return true;
            }

            result = default;
            return false;
        }

        protected abstract TMessage ReadMessage(JObject obj, string messageType);
    }
}
