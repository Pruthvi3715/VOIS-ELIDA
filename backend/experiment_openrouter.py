from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    print("Please set OPENROUTER_API_KEY in .env file")
    exit(1)

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=api_key,
)

print("Sending first request...")
# First API call with reasoning
response = client.chat.completions.create(
  model="openrouter/pony-alpha", # Note: This model might not be available or might necessitate specific permissions. 
  # If it fails, we might try another reasoning model or just check if the parameters are accepted.
  # The user specifically asked for pony-alpha, so we keep it.
  messages=[
          {
            "role": "user",
            "content": "How many r's are in the word 'strawberry'?"
          }
        ],
  extra_body={"reasoning": {"enabled": True}}
)

# Extract the assistant message with reasoning_details
response_message = response.choices[0].message
print(f"Response: {response_message.content}")

# Check if reasoning_details exists
reasoning_details = None
if hasattr(response_message, 'reasoning_details'):
    print(f"Reasoning details found: {response_message.reasoning_details}")
    reasoning_details = response_message.reasoning_details
else:
    print("Reasoning details NOT found in the response object directly.")
    # It might be in model_extra
    if response_message.model_extra and 'reasoning_details' in response_message.model_extra:
         print(f"Reasoning details found in model_extra: {response_message.model_extra['reasoning_details']}")
         reasoning_details = response_message.model_extra['reasoning_details']
    else:
         print("Reasoning details not found in model_extra either.")
         reasoning_details = None

# Preserve the assistant message with reasoning_details
messages = [
  {"role": "user", "content": "How many r's are in the word 'strawberry'?"},
  {
    "role": "assistant",
    "content": response_message.content,
  },
  {"role": "user", "content": "Are you sure? Think carefully."}
]

# If we found reasoning details, add them
if reasoning_details:
    messages[1]["reasoning_details"] = reasoning_details

print("\nSending second request...")
# Second API call - model continues reasoning from where it left off
try:
    response2 = client.chat.completions.create(
      model="openrouter/pony-alpha",
      messages=messages,
      extra_body={"reasoning": {"enabled": True}}
    )
    print(f"Second Response: {response2.choices[0].message.content}")
except Exception as e:
    print(f"Error in second request: {e}")
