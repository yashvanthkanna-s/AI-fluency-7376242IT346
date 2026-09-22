# Comparing a Plain Chatbot, a Rule-Based Workflow, and an AI Agent

## My Scenario: Personal Expense Tracking for a College Student

The scenario I picked is something I actually deal with every month — keeping track of where my money goes. As a college student, I have a limited budget (around Rs.8000/month), and I spend on food (Swiggy, Zomato, canteen), transport (Ola, metro), shopping (Amazon, Flipkart), entertainment (Netflix, Spotify, movies), education stuff (courses, books), and utilities (phone recharge, electricity). I have my expense data stored in a JSON file and a budget config file with limits per category. The question I'm trying to answer with all three approaches is: "How am I doing this month? Am I overspending somewhere? Where should I cut back?"

---

## Explanation of Each Approach

### 1. Plain Chatbot

The plain chatbot is basically just an LLM (I used OpenAI's GPT-4o-mini) sitting behind a terminal prompt. You type something, it sends your message to the API, and it replies. That's it. There's no file reading, no tools, no access to my expenses.json or budget.json at all — the chatbot has zero idea what I actually spent money on.

So when I ask it "Am I overspending on food this month?", it gives me generic advice like "track your expenses using an app" or "the 50/30/20 rule is great for budgeting." It's not wrong, but it's not useful either because it can't see my data. If I manually type "I spent Rs.3880 on food this month and my limit is Rs.3000", then it can do basic math and tell me I'm over budget — but I had to do all the work myself. The chatbot is just parroting back what I told it with some extra advice layered on top.

The limitation here is obvious. The LLM is powerful at understanding language and giving decent general answers, but it's completely blind to my private data. It can't read files, it can't calculate my real totals, it can't check my actual budget. It's like asking a smart friend for money advice without showing them your bank statement — they'll give you textbook answers but nothing specific to your situation.

### 2. Rule-Based Workflow

The rule-based workflow is the opposite extreme. There's no LLM at all — it's pure Python with if/else statements, loops, and predefined processing steps. It directly reads my expenses.json and budget.json files, so it has full access to my private data.

The way it works is pretty straightforward. It takes my input, checks for keywords (like "summary", "budget", "top expenses", "food"), and then runs a fixed sequence of steps based on what keyword it matched. If I type "budget check", it loads all expenses, calculates totals per category, compares each total against the limit in budget.json, and prints out which categories are over budget and by how much.

This actually works well for what it does. It gives me real numbers — it can tell me exactly that I spent Rs.3930 on food against a Rs.3000 limit, so I'm Rs.930 over. The problem is that it's rigid. It only understands the keywords I programmed into it. If I type "where should I cut back to save more?" — it doesn't understand that at all and just dumps a generic summary. It can't reason, it can't give advice, it can't handle anything outside the predefined rules. Adding a new feature means writing new code, new if/else branches, new functions. There's no flexibility.

Also, the output is always the same format. It doesn't adapt to how I ask the question. "Show me food expenses" and "how much did I spend on food" give the same output, but "what's eating up my food budget" gives nothing useful because "eating" doesn't match any keyword rule.

### 3. AI Agent

The AI agent is where things get interesting. It combines the LLM's ability to understand natural language with actual tools that can read and process my private data, and it does this in a loop — meaning it can make multiple decisions and tool calls before giving me a final answer.

Here's how it works. I ask something like "Am I overspending? Where should I cut back?" The LLM first reasons about what it needs to do. It decides "I need to read the expenses first", so it calls the `read_expenses` tool. Then it looks at the result and thinks "now I need the budget to compare against", so it calls `read_budget`. Then it calls `calculate_totals` to crunch the numbers, then `check_budget` to find violations. After all of that, it has all the data it needs, and it generates a personalized response telling me exactly which categories are over budget, by how much, and gives specific suggestions like "your food spending is Rs.930 over — maybe cut down on Swiggy orders and eat at the canteen more."

The key difference is the loop. The agent doesn't just do one thing — it keeps going, calling tool after tool, until it has enough information to answer properly. And because the LLM is in the loop, it can handle any phrasing. I can ask "what's my most expensive bad habit" and it'll figure out that it needs to read expenses, sort them, maybe look at entertainment and food, and then give me a thoughtful answer. The rule-based workflow would have no idea what to do with that question.

The limitation of the agent is that it needs an API key (costs money per call), it's slower because of multiple API round trips, and sometimes the LLM might make a mistake in reasoning or call the wrong tool. But for a complex, multi-step task with private data, it's by far the most capable approach.

---

## Comparison Table

| Basis for Comparison | Plain Chatbot | Rule-Based Workflow | AI Agent |
|---|---|---|---|
| **Flexibility** | High for general conversation but can't adapt to my specific data. Answers any question but generically. | Very low. Only responds to predefined keywords and patterns. New functionality needs new code. | Very high. Understands natural language, handles unexpected questions, adapts its approach based on the data it reads. |
| **Decision-making** | The LLM decides what to say, but decisions are based only on general knowledge, not my actual situation. | No real decision-making. Follows fixed if/else rules. The decisions were made by me when I wrote the code. | The LLM makes real-time decisions — which tools to call, in what order, and what to do with the results. This is genuine reasoning. |
| **Tool usage** | None. The chatbot has no tools. It can only generate text. | Uses built-in Python functions to read files and do calculations, but these aren't "tools" in the agent sense — they run in a fixed pipeline. | Uses tools through function calling. The LLM chooses which tools to invoke and when. Tools include reading expense data, calculating totals, checking budgets, and filtering by category. |
| **Private-data access** | No access at all. Can't read my files. Only knows what I manually type into the chat. | Full access. Directly reads expenses.json and budget.json using file I/O. | Full access through tools. The agent calls `read_expenses` and `read_budget` tools to pull my private data into its reasoning context. |
| **Multi-step task handling** | Single step only. One question, one answer. Can't chain operations or build on previous data retrieval. | Multi-step but fixed. Always runs the same steps in the same order for a given keyword match. Can't dynamically add or skip steps. | Truly multi-step and dynamic. The agent decides the sequence at runtime — it might call 2 tools or 6 tools depending on what the question needs. Each step informs the next. |
| **Automation** | No automation. Every interaction is a standalone question-answer. Can't trigger workflows or act on data. | Automated within its rules. Give it a keyword and it runs the full pipeline automatically. But can't go beyond what's coded. | Fully automated and adaptive. Give it a complex request and it autonomously plans, executes, and delivers — no manual intervention needed. |
| **Reliability** | Reliable in giving some kind of answer, but the answer may be vague or wrong because it's guessing without data. Might hallucinate numbers. | Very reliable within its scope. The calculations are deterministic — same input always gives same output. No hallucination risk. | Mostly reliable but has some unpredictability. The LLM might occasionally call the wrong tool or misinterpret results. More reliable than the plain chatbot because it uses real data, but less deterministic than the rule-based workflow. |

---

## Suitability Analysis

For my specific scenario — personal expense tracking with private data, budget checking, and getting actionable advice — the **AI agent** is the most suitable approach.

Here's why. My scenario involves multiple steps that need to happen in sequence (read data, compute totals, compare to budget, generate advice), it requires access to private data files, and I want answers in natural language that are tailored to my actual spending patterns. The plain chatbot fails because it can't see my data at all. The rule-based workflow handles the data part but can't give me personalized advice or handle flexible questions. Only the agent does both — it reads my real data using tools AND reasons about it using the LLM to give me specific, actionable suggestions.

Looking at the comparison table, the agent wins on flexibility (handles any question I throw at it), decision-making (dynamically picks which tools to use), tool usage (actually has tools and uses them intelligently), private-data access (reads my files through tools), multi-step handling (chains multiple tool calls together), and automation (does everything end-to-end without me needing to specify each step). The only dimension where the rule-based workflow beats the agent is reliability — the workflow's output is deterministic and never hallucinates, while the agent's LLM could occasionally make mistakes. But for my use case, the flexibility and intelligence of the agent far outweigh the small reliability trade-off.

---

## Conclusion

Each of the three approaches has its place — it just depends on the kind of problem you're solving.

A **plain chatbot** is the right choice when you need a conversational interface for general knowledge questions, brainstorming, or situations where there's no private data involved. If someone wants help understanding budgeting concepts, learning about the 50/30/20 rule, or just having a conversation about financial planning in general, a chatbot is perfectly fine. It's quick to build, doesn't need any backend infrastructure, and the LLM handles the complexity of language understanding. But the moment you need it to work with specific, private, real-world data — it falls short.

A **rule-based workflow** is the right choice when the task is well-defined, the steps are known in advance, and reliability matters more than flexibility. Think of things like automated invoice processing, payroll calculation, form validation, or any scenario where the logic can be fully captured in rules and conditions. These systems are deterministic, fast, and don't need an API key or internet connection. The downside is that they can't handle anything outside their predefined rules — if a new situation comes up that wasn't anticipated, the workflow just breaks or gives a default response.

An **AI agent** is the right choice when the task is complex, involves multiple steps that aren't always predictable, requires both data access and reasoning, and benefits from natural language understanding. Scenarios like personal finance analysis, research assistance, customer support with access to account data, or any situation where the system needs to figure out what to do rather than being told exactly what to do — that's where agents shine. The combination of LLM + Tools + Loop means the agent can reason about what information it needs, go get that information, process it, and keep iterating until it has a complete answer. Yes, it's more expensive to run and slightly less predictable than a rule-based system, but for complex real-world tasks with private data, it's the most capable and practical solution.

In short: use a chatbot for conversation, a workflow for automation of known processes, and an agent when you need intelligent automation that can think on its feet.
