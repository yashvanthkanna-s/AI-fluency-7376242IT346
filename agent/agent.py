"""
AI Agent - Combines LLM + Tools + Loop.
The agent reasons about the user's request, decides which tools to use,
observes results, and keeps going until the task is done.

Uses the shared config.py and tools.py (same pattern from the Day 1 lab).
"""

import json
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import client, MODEL, banner
from tools  import TOOLS, TOOL_FUNCTIONS

SYSTEM_PROMPT = """You are an intelligent expense management agent. You have access to tools 
that let you read the user's private expense data, analyze their budget, and provide 
personalized financial advice.

Never guess spending amounts: always use read_expenses and read_budget to get real data.
Use calculator for any arithmetic. If no tool is needed, answer directly."""


def agent(question, max_steps=8, verbose=True):
    """
    THE AGENT LOOP - this is what makes it an agent.
    The LLM reasons -> picks tools -> observes results -> repeats until done.
    (Same loop structure as the Day 1 lab agent.py)
    """
    messages = [{"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": question}]

    for step in range(1, max_steps + 1):
        # 1. REASON: ask the LLM what to do next
        response = client.chat.completions.create(
            model=MODEL, messages=messages, tools=TOOLS, temperature=0)
        message = response.choices[0].message

        # 2. If no tool is requested, the LLM has finished
        if not message.tool_calls:
            return message.content.strip()

        messages.append({
            "role": "assistant", "content": message.content or "",
            "tool_calls": [{"id": call.id, "type": "function",
                            "function": {"name": call.function.name,
                                         "arguments": call.function.arguments}}
                           for call in message.tool_calls]})

        # 3. ACT and OBSERVE: run each tool, send the result back
        for call in message.tool_calls:
            name      = call.function.name
            try:
                arguments = json.loads(call.function.arguments or "{}")
            except Exception:
                arguments = {}
            function  = TOOL_FUNCTIONS.get(name)
            try:
                result    = function(**arguments) if function else f"Unknown tool: {name}"
            except Exception as err:
                result    = f"Error running {name}: {err}"

            if verbose:
                print(f"  step {step}: {name}({list(arguments.keys())}) -> {result[:80]}...")

            messages.append({"role": "tool", "tool_call_id": call.id, "content": result})

    return "Stopped: maximum steps reached without a final answer."


# Test questions (same ones we'll ask all three systems)
QUESTIONS = [
    "What is my total spending this month?",
    "Am I over budget on food?",
    "What are my top 3 most expensive purchases?",
    "Give me tips to save money on food delivery.",
]


if __name__ == "__main__":
    banner("SYSTEM 3: AI AGENT (LLM + Tools + Loop)")
    for question in QUESTIONS:
        print("Q:", question)
        print("A:", agent(question))
        print("-" * 70)
