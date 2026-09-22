"""
Phase 2 hands-on: structured output with Pydantic.

Goal: instead of parsing free-text LLM output with regex/string matching,
define a schema and get validated, typed data back. This pattern
(schema -> prompt -> validate) is the backbone of every later project
in this plan (RAG, agents).

Run: python 02_structured_output.py
"""

import os

from anthropic import Anthropic
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


class TicketClassification(BaseModel):
    category: str  # e.g. "bug", "feature_request", "data_quality", "question"
    severity: str  # "low", "medium", "high"
    summary: str  # one-sentence summary
    needs_follow_up: bool


TICKET_TEXT = """
The nightly ETL job for the customer_events table has been silently
dropping about 5% of rows for the past two days. No errors in the logs.
Discovered because a downstream dashboard showed a dip in event counts.
"""

SCHEMA_INSTRUCTIONS = f"""
Classify the following support ticket. Respond with ONLY a JSON object
matching this schema, no other text:

{TicketClassification.model_json_schema()}

Ticket:
{TICKET_TEXT}
"""

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=300,
    messages=[{"role": "user", "content": SCHEMA_INSTRUCTIONS}],
)

raw_json = response.content[0].text
result = TicketClassification.model_validate_json(raw_json)

print(result)
print(f"\nCategory: {result.category}")
print(f"Severity: {result.severity}")
print(f"Needs follow-up: {result.needs_follow_up}")
