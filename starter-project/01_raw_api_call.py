"""
Phase 1 hands-on: talk to an LLM API directly, no framework.

Goal: see exactly what a "message" is, how the system prompt works, and
what comes back — before any framework (LangGraph, LlamaIndex, etc.)
hides these details from you.

Run: python 01_raw_api_call.py
"""

import os

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=500,
    system=(
        "You are a terse technical mentor. Explain things the way you'd "
        "explain them to a strong engineer who is new to a specific topic."
    ),
    messages=[
        {
            "role": "user",
            "content": (
                "In 3 sentences, explain what a 'context window' is and "
                "why it matters when building an application on top of an LLM."
            ),
        }
    ],
)

print(response.content[0].text)
print("\n---")
print(f"Input tokens: {response.usage.input_tokens}")
print(f"Output tokens: {response.usage.output_tokens}")

# --- Temperature comparison ---
# Same prompt, run twice at different temperatures, so "sampling" stops
# being an abstract parameter and becomes something you've actually seen
# change the output. temperature=0 is close to deterministic; temperature=1
# lets the model take more varied word choices at each step.
prompt = "Suggest one metaphor for what a neural network is."

for temp in (0, 1):
    r = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=100,
        temperature=temp,
        messages=[{"role": "user", "content": prompt}],
    )
    print(f"\n--- temperature={temp} ---")
    print(r.content[0].text)
