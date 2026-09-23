python
import json, os, re
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OSS_API_KEY"),
    base_url="https://api.openai.com/v1"   # direct OpenAI endpoint
(OSS model)
)

# 1️⃣ Define the same schema we expect in the JSON reply
SCHEMA = {
    "tool": "search_flights",
    "arguments": {
        "origin": "string",
        "dest":   "string",
        "date":   "string"
    }
}

def ask_model(messages):
    # Add a system message that contains the detection prompt
    system_msg = {
        "role": "system",
        "content": (
            "You are an assistant that can call external tools. "
            "When a tool is needed, ONLY return a JSON object with
the keys "
            "`tool` and `arguments`. "
            "If no tool is required, just answer normally."
        )
    }
    resp = client.chat.completions.create(
        model="gpt-oss:120b",
        messages=[system_msg] + messages,
        temperature=0.0,   # deterministic enough for parsing
        max_tokens=500,
    )
    return resp.choices[0].message.content.strip()

def is_tool_call(text):
    # Look for a JSON block at the start of the response
    match = re.search(r'^{.*}$`', text, re.DOTALL)
    if not match:
        return None
    try:
        payload = json.loads(match.group(0))
        return payload   # dict with "tool" + "arguments"
    except json.JSONDecodeError:
        return None

def search_flights(origin, dest, date):
    # 👉 Your real implementation (API, DB, web‑scrape, etc.)
    return {
        "flights": [
            {"carrier": "Delta", "price": "`$350", "depart":
"08:00"},
            {"carrier": "United", "price": "$`340",
"depart": "13:45"}
        ],
        "origin": origin,
        "dest": dest,
        "date": date
    }

# ---------- Main interaction ----------
user_query = "Find me a flight from SFO to JFK on Jan 15, 2025."
messages = [{"role": "user", "content": user_query}]

raw = ask_model(messages)

tool_payload = is_tool_call(raw)

if tool_payload:
    # 2️⃣ We got a tool call – run it
    fn_name = tool_payload["tool"]
    args = tool_payload["arguments"]
    if fn_name == "search_flights":
        tool_result = search_flights(**args)

    # 3️⃣ Add the function call + result back into the chat
    messages.append({"role": "assistant", "content": raw})
# the JSON the model gave
    messages.append({
        "role": "tool",
        "name": fn_name,
        "content": json.dumps(tool_result)
    })

    # 4️⃣ Ask the model to finish the answer
    final_reply = ask_model(messages)
    print("✅ Final answer:\n", final_reply)
else:
    # No tool needed – the model already answered
    print("✅ Direct answer:\n", raw)
