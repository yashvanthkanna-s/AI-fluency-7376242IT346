# AI Fluency - Day 1: Comparing Chatbot vs Workflow vs AI Agent

## Project Structure

This repository contains two parts:

### 1. `day1_lab/` — Lab Manual Work
The lab setup and practice programs from the Day 1 lab manual, using the **college course fees** scenario (CS101, AI202, DS303).

```
day1_lab/
├── .env                  # Provider config (Ollama/Groq/HuggingFace)
├── config.py             # Shared settings and provider setup
├── check_setup.py        # Step 1: test the LLM connection
├── chatbot.py            # System 1: plain chatbot (LLM only)
├── workflow.py           # System 2: rule-based workflow (no LLM)
├── tools.py              # Tools for the agent (fee lookup + calculator)
├── agent.py              # System 3: AI agent (LLM + Tools + Loop)
└── challenge.py          # Bonus question testing flexibility
```

### 2. Root — Day 1 Assessment Task
The assessment task, built on top of the lab patterns, using a **personal expense tracking** scenario.

```
├── config.py             # Shared provider config (same pattern as lab)
├── tools.py              # Expense tools (same pattern as lab's tools.py)
├── chatbot/chatbot.py    # System 1: plain chatbot (no data access)
├── workflow/workflow.py  # System 2: rule-based workflow (if/else only)
├── agent/agent.py        # System 3: AI agent (LLM + Tools + Loop)
├── data/
│   ├── expenses.json     # Private expense data (30 transactions)
│   └── budget.json       # Budget limits per category
├── analysis.md           # Full written analysis (graded document)
└── Output/               # Screenshots of all three systems running
```

## Setup

1. **Create a `.env` file** in the root (copy from `.env.example`):
   ```
   PROVIDER=groq
   GROQ_API_KEY=your_key_here
   MODEL=openai/gpt-oss-20b
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the lab programs** (in `day1_lab/`):
   ```bash
   cd day1_lab
   python check_setup.py
   python chatbot.py
   python workflow.py
   python agent.py
   python challenge.py
   ```

4. **Run the assessment programs** (from root):
   ```bash
   python chatbot/chatbot.py
   python workflow/workflow.py
   python agent/agent.py
   ```

## Key Takeaway

| System | Uses LLM? | Reads Private Data? | Has Tools? | Flexible? |
|---|---|---|---|---|
| Plain Chatbot | Yes | No | No | High (but generic) |
| Rule-Based Workflow | No | Yes | No | Low (rigid rules) |
| AI Agent | Yes | Yes (via tools) | Yes | High (and specific) |

See [analysis.md](analysis.md) for the full written comparison.
