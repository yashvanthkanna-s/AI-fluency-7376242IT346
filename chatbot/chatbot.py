"""
Plain Chatbot - Uses only an LLM to respond to user queries.
No tools, no file access, no private data - just the LLM's general knowledge.

Uses the shared config.py (same provider setup pattern from the Day 1 lab).
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import client, MODEL, banner

SYSTEM_PROMPT = """You are a helpful financial assistant chatbot. 
You can answer general questions about budgeting, saving money, and expense management.
You do NOT have access to any user's personal expense data or files.
Just give general advice based on what the user tells you."""


def chatbot(question):
    """Send a question to the LLM. No tools, no data access."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": question},
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()


# Test questions (same ones we'll ask all three systems)
QUESTIONS = [
    "What is my total spending this month?",
    "Am I over budget on food?",
    "What are my top 3 most expensive purchases?",
    "Give me tips to save money on food delivery.",
]


if __name__ == "__main__":
    banner("SYSTEM 1: PLAIN CHATBOT (no tools, no data)")
    for question in QUESTIONS:
        print("Q:", question)
        print("A:", chatbot(question))
        print("-" * 70)
