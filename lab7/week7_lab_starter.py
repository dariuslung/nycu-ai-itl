#!/usr/bin/env python3
"""
Week 7 Lab starter: a three-tool agent.

The lab has two halves:
  A. DIAGNOSE  - run the PROVIDED tool descriptions (TOOLS_V0, deliberately flawed) and find out how they fail.
  B. FIX       - write your OWN descriptions (TOOLS, look for TODO) and show that they fix the failures.

What is already done for you:  the three tool functions, the knowledge base, the calendar,
                               the message loop, a trace printer, and a repeat-runner.
What YOU write:                (1) handle_tool_call()      (look for TODO, Part 1)
                               (2) the schemas in TOOLS    (look for TODO, Part 3)

Run it:
    python week7_lab_starter.py --v0 --tests          # baseline queries, using the PROVIDED (flawed) descriptions
    python week7_lab_starter.py --v0 --modes          # starter queries for each failure mode, on V0
    python week7_lab_starter.py --v0 --modes --repeat 5   # run each query 5 times and count what happens
    python week7_lab_starter.py --v0 --stress --repeat 5  # harder queries, 5 runs each
    python week7_lab_starter.py --modes --repeat 5    # the same, using YOUR descriptions (TOOLS)
    python week7_lab_starter.py "your own question"   # one question (add --v0 to use the flawed set)
    python week7_lab_starter.py                       # interactive prompt

Setup:
    pip install anthropic
    set your key in the terminal (do NOT paste it into this file):
        macOS/Linux:  export ANTHROPIC_API_KEY=your-key-here
        Windows:      setx ANTHROPIC_API_KEY your-key-here    (then open a new terminal)
"""
import ast
import json
import operator
import os
import sys
from collections import Counter

import anthropic

MODEL = os.environ.get("LAB_MODEL", "claude-haiku-5-5")
MAX_TURNS = 5          # the loop stops after this many model calls (never loop forever)
client = anthropic.Anthropic()   # reads ANTHROPIC_API_KEY from your environment


# =============================================================================
# THE TOOLS (the code that runs when the model asks). Already written.
# =============================================================================
_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
        ast.Div: operator.truediv, ast.Pow: operator.pow, ast.USub: operator.neg,
        ast.Mod: operator.mod, ast.FloorDiv: operator.floordiv}


def _eval(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        left, right = _eval(node.left), _eval(node.right)
        if isinstance(node.op, ast.Pow) and abs(right) > 100:
            raise ValueError("exponent too large")
        return _OPS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval(node.operand))
    raise ValueError("only numbers and + - * / ** % // are allowed")


def run_calculator(expression: str) -> str:
    """Evaluate plain arithmetic safely. Never uses eval()."""
    try:
        return str(_eval(ast.parse(expression, mode="eval").body))
    except Exception as e:
        return f"Error: {e}"


KNOWLEDGE_BASE = {
    "week 5": "Week 5 covers prompt engineering techniques: zero-shot, few-shot, chain-of-thought, and self-correction.",
    "week 6": "Week 6 is async and covers why prompts fail: hallucination, sycophancy, sensitivity, over-refusal and bias.",
    "week 7": "Week 7 is online and covers tool use, function calling, and MCP. Students build a tool-using agent.",
    "assignment 1": "Assignment 1 has two parts: five prompting techniques on a code task, and diagnosing three broken prompts. Due Oct 30.",
    "cp1": "CP1 was due Oct 12. Deliverables: team charter, problem statement with evidence, interaction design sketch, evaluation plan, repository link.",
    "code steward": "The code steward is the designated PR reviewer for a period. Everyone does it at least twice. Rotations are recorded in DECISIONS.md.",
}


def search_knowledge_base(query: str) -> str:
    """Course CONTENT: what is covered, what is in a deliverable, what a role does."""
    q = query.lower()
    for key, value in KNOWLEDGE_BASE.items():
        if key in q:
            return value
    return "No relevant information found for this query."


CALENDAR = {
    "cp1": "CP1 was due Mon Oct 12.",
    "week 6 lab": "The Week 6 lab was due Wed Oct 14, 23:59.",
    "week 7 lab": "The Week 7 lab is due Wed Oct 21, 23:59.",
    "assignment 1": "Assignment 1 is due Fri Oct 30.",
}


def get_course_calendar(item: str) -> str:
    """Course DATES only: when something is due. Does not describe content."""
    q = item.lower()
    for key, value in CALENDAR.items():
        if key in q:
            return value
    return ("No date found for that item. Items with dates: "
            + ", ".join(CALENDAR) + ".")


# =============================================================================
# THE PROVIDED SCHEMAS (V0): deliberately flawed. Test these first (Part 2).
# Do not edit this list. Your own descriptions go in TOOLS (Part 3).
# =============================================================================
TOOLS_V0 = [
    {"name": "calculator",
     "description": "Does calculations. Use for anything involving numbers.",
     "input_schema": {"type": "object",
                      "properties": {"expression": {"type": "string",
                                                    "description": "The thing to calculate."}},
                      "required": ["expression"]}},
    {"name": "search_knowledge_base",
     "description": "Searches course information. Use only if you do not already know the answer.",
     "input_schema": {"type": "object",
                      "properties": {"query": {"type": "string",
                                               "description": "What to look for."}},
                      "required": ["query"]}},
    {"name": "get_course_calendar",
     "description": "Finds course dates and information.",
     "input_schema": {"type": "object",
                      "properties": {"item": {"type": "string",
                                              "description": "The thing to look up."}},
                      "required": ["item"]}},
]


# =============================================================================
# PART 3: WRITE YOUR OWN SCHEMAS  (TODO)
# Replace every "TODO" string. Use the six-question checklist from the lecture.
# Your goal: fix the failures you found in V0 without creating new ones.
# =============================================================================
TOOLS = [
    {
        "name": "calculator",
        "description": (
            "Evaluates one plain arithmetic expression exactly and returns the result as a number. "
            "Use it for any multiplication, division or multi-step arithmetic where precision matters, "
            "and for date differences (compute them from dates you got from get_course_calendar). "
            "Do NOT use it for trivial arithmetic you can do reliably yourself, such as 2+2 or 10/2, "
            "and never for questions about course content or dates. "
            "Supported: numbers, + - * / ** (power, exponent at most 100), % (modulo), // (floor "
            "division), unary minus. NOT supported: sqrt(), percent signs (write 15% of 240 as "
            "0.15 * 240), ^, commas in numbers, words, variables. Invalid input returns an "
            "'Error: ...' message; fix the expression and retry."),
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": (
                        "A single arithmetic expression using only digits, decimal points, "
                        "parentheses and + - * / ** % //. Example: '(0.15 * 240 + 3 ** 2) / 2'. "
                        "Use ** for powers, 12 ** 0.5 for a square root, no thousands separators."),
                }
            },
            "required": ["expression"],
        },
    },
    {
        "name": "search_knowledge_base",
        "description": (
            "Looks up course CONTENT: what each week covers, what is in an assignment or checkpoint "
            "deliverable (e.g. CP1), and what a role such as the code steward does. Use it whenever "
            "the question is about this course's specific material, even if you think you know the "
            "answer, because course details may differ from general knowledge. Do NOT use it for "
            "deadlines or due dates (use get_course_calendar), for arithmetic (use calculator), or for "
            "general-knowledge questions unrelated to the course, such as geography or what "
            "chain-of-thought prompting is in general. Returns a short text passage, or 'No relevant "
            "information found'. It only knows weeks 5-7, assignment 1, CP1 and the code steward; "
            "if it finds nothing, say so instead of guessing."),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": (
                        "Short keyword phrase naming the topic, with spaces and normal spelling, "
                        "e.g. 'week 6', 'cp1 deliverables', 'code steward', 'assignment 1'."),
                }
            },
            "required": ["query"],
        },
    },
    {
        "name": "get_course_calendar",
        "description": (
            "Looks up course DATES only: when something is due or was due. Use it for any "
            "'when' or 'deadline' question about CP1, the Week 6 lab, the Week 7 lab or Assignment 1. "
            "Do NOT use it for what a week covers, what a deliverable contains or what a role does "
            "(use search_knowledge_base), and do not use it for arithmetic. Returns one sentence "
            "with the due date and time, or 'No date found' plus the list of items that have dates. "
            "For questions that compare dates, call it once per item, then use calculator for the "
            "difference."),
        "input_schema": {
            "type": "object",
            "properties": {
                "item": {
                    "type": "string",
                    "description": (
                        "Name of the dated item, lowercase, e.g. 'cp1', 'week 6 lab', "
                        "'week 7 lab', 'assignment 1'. Name only the item, not the question."),
                }
            },
            "required": ["item"],
        },
    },
]


# =============================================================================
# PART 1: HANDLE A TOOL CALL  (TODO)
# Given the tool's name and the arguments the model sent, run the right function
# and return (result_text, is_error).
#   - calculator            -> run_calculator(tool_input["expression"])
#   - search_knowledge_base -> search_knowledge_base(tool_input["query"])
#   - get_course_calendar   -> get_course_calendar(tool_input["item"])
#   - anything else         -> return an error message the model can understand
#   - if something raises an exception, return its message with is_error=True
# Note: run_calculator reports bad input as a string starting with "Error:".
#       Decide whether that should count as is_error=True.
# =============================================================================
def handle_tool_call(tool_name: str, tool_input: dict):
    try:
        if tool_name == "calculator":
            result = run_calculator(tool_input["expression"])
            # Design decision: "Error: ..." means the call failed, so flag it.
            return result, result.startswith("Error:")
        if tool_name == "search_knowledge_base":
            return search_knowledge_base(tool_input["query"]), False
        if tool_name == "get_course_calendar":
            return get_course_calendar(tool_input["item"]), False
        return (f"Unknown tool '{tool_name}'. Available tools: calculator, "
                "search_knowledge_base, get_course_calendar."), True
    except Exception as e:
        return f"{type(e).__name__}: {e}", True

# =============================================================================
# THE LOOP (already written). Read it. It is the loop from the lecture.
# `trace` (optional) collects what happened, so runs can be counted.
# =============================================================================
def run_agent(user_text: str, verbose: bool = True, trace=None) -> str:
    messages = [{"role": "user", "content": user_text}]
    n_calls = 0
    for turn in range(MAX_TURNS):
        response = client.messages.create(
            model=MODEL, max_tokens=1024, tools=TOOLS, messages=messages)
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason != "tool_use":
            answer = "".join(b.text for b in response.content if b.type == "text")
            if verbose:
                if n_calls == 0:
                    print("   (no tool called: the model answered directly)")
                print(f"   ANSWER: {answer}")
            return answer

        results = []
        for block in response.content:
            if block.type == "tool_use":
                n_calls += 1
                if verbose:
                    print(f"   TOOL CALL -> {block.name}({json.dumps(block.input, ensure_ascii=False)})")
                try:
                    output, is_error = handle_tool_call(block.name, block.input)
                except NotImplementedError:
                    raise
                except Exception as e:
                    output, is_error = f"{type(e).__name__}: {e}", True
                if trace is not None:
                    trace.append({"name": block.name, "input": block.input,
                                  "output": output, "is_error": bool(is_error)})
                if verbose:
                    flag = " [is_error]" if is_error else ""
                    print(f"   RESULT{flag} <- {output}")
                result = {"type": "tool_result", "tool_use_id": block.id, "content": output}
                if is_error:
                    result["is_error"] = True
                results.append(result)
        messages.append({"role": "user", "content": results})

    msg = f"(stopped after {MAX_TURNS} model calls)"
    if verbose:
        print("   " + msg)
    return msg


# =============================================================================
# TEST QUERIES (edit freely; add your own)
# =============================================================================
TEST_QUERIES = [
    "What is 247 times 38?",                 # calculator          -> 9386
    "What is covered in Week 6?",            # knowledge base
    "When is the Week 7 lab due?",           # calendar
    "What is the capital of France?",        # no tool
]

# Starting points for the diagnosis. Results vary between runs: use --repeat.
QUERIES_BY_MODE = {
    "1. Wrong tool": [
        "How many techniques are covered in Week 5?",       # knowledge base, not the calculator
        "What are the deliverables for CP1?",               # knowledge base, not the calendar
        "When is the Week 7 lab due?",                      # calendar, not the knowledge base
    ],
    "2. Wrong parameters": [
        "What is twenty-four divided by eight, then multiplied by three?",
        "What is the square root of 144 plus 15 percent of 240?",
        "What is covered in Week6?",                        # note the missing space
    ],
    "3. Tool called unnecessarily": [
        "What does the term 'hallucination' mean in the context of language models?",
        "What is the capital of France?",
        "What is chain-of-thought prompting?",
    ],
    "4. Tool not called when it should be": [
        "What does the code steward do?",
        "When is Assignment 1 due?",
        "What is 48273 times 9167?",                        # true answer: 442518591
    ],
}

# Harder queries. Use these if the starter queries did not fail (see the lab guide).
STRESS_BY_MODE = {
    "1. Wrong tool": [
        "Which came first, CP1 or the Week 6 lab, and by how many days?",   # CP1, by 2 days: calendar + calculator
        "How many days are there between the CP1 deadline and the Assignment 1 deadline?",  # 18
    ],
    "2. Wrong parameters": [
        "What is 1,234 times 5,678?",                       # commas; true answer 7006652
        "What is 15% of 240 plus 3 squared, all divided by 2?",   # 22.5
        "What is 2 to the power of 200?",                   # the calculator refuses; what does the model do?
    ],
    "3. Tool called unnecessarily": [
        "Explain in one sentence why the sky is blue.",
        "What is 10 divided by 2?",                         # is a tool worth it here?
    ],
    "4. Tool not called when it should be": [
        "What is 987654 times 123456?",                     # true answer: 121931812224
        "Who is the code steward this week?",               # the KB does not say: a good model says so
        "What is the topic of Week 9?",                     # the KB has no entry: a good model says so
    ],
}


def run_tests(queries):
    for q in queries:
        print(f"\nQ: {q}")
        run_agent(q)


def run_repeated(queries, n):
    """Run each query n times and count what the model did. Results vary, so counts are evidence."""
    for q in queries:
        print(f"\nQ: {q}   ({n} runs)")
        sequences, error_runs, first_answer, example = Counter(), 0, None, None
        for i in range(n):
            trace = []
            try:
                answer = run_agent(q, verbose=False, trace=trace)
            except NotImplementedError:
                raise
            except Exception as e:                      # rate limit, network, etc.
                print(f"   run {i + 1} stopped: {type(e).__name__}: {e}")
                break
            seq = " -> ".join(t["name"] for t in trace) or "(no tool)"
            sequences[seq] += 1
            if any(t["is_error"] for t in trace):
                error_runs += 1
                if example is None:
                    bad = next(t for t in trace if t["is_error"])
                    example = f'{bad["name"]}({json.dumps(bad["input"], ensure_ascii=False)}) -> {bad["output"]}'
            if first_answer is None:
                first_answer = answer
        for seq, count in sequences.most_common():
            print(f"   {count} x {seq}")
        print(f"   tool errors in {error_runs} of {sum(sequences.values())} runs")
        if example:
            print(f"   e.g. {example}")
        if first_answer is not None:
            short = first_answer.replace("\n", " ")
            print(f"   first answer: {short[:300]}{'...' if len(short) > 300 else ''}")


def warn_if_todo():
    if "TODO" in json.dumps(TOOLS):
        print("Note: your schemas in TOOLS still contain TODO text (Part 3). "
              "Use --v0 to run the provided descriptions.\n")


def main(argv):
    global TOOLS
    args = list(argv)
    if "--v0" in args:
        args.remove("--v0")
        TOOLS = TOOLS_V0
        print("Using TOOLS_V0: the PROVIDED descriptions (deliberately flawed). Your own schemas are untouched.\n")
    else:
        warn_if_todo()
    repeat = 1
    if "--repeat" in args:
        i = args.index("--repeat")
        try:
            repeat = max(1, int(args[i + 1]))
        except (IndexError, ValueError):
            sys.exit("--repeat needs a number, for example: --repeat 5")
        del args[i:i + 2]
    if repeat > 10:
        sys.exit("Please keep --repeat at 10 or below: the class shares a budget.")

    def go(queries_or_table):
        run = (lambda qs: run_repeated(qs, repeat)) if repeat > 1 else run_tests
        if isinstance(queries_or_table, dict):
            for mode, qs in queries_or_table.items():
                print(f"\n===== Failure mode {mode} =====")
                run(qs)
        else:
            run(queries_or_table)

    if args == ["--tests"]:
        go(TEST_QUERIES)
    elif args == ["--modes"]:
        go(QUERIES_BY_MODE)
    elif args == ["--stress"]:
        go(STRESS_BY_MODE)
    elif args and not args[0].startswith("--"):
        go([" ".join(args)])
    elif args:
        sys.exit(f"Unknown option(s): {' '.join(args)}. See the top of this file for usage.")
    else:
        print("Type a question (empty line to quit).")
        while True:
            q = input("\nQ: ").strip()
            if not q:
                break
            run_agent(q)


if __name__ == "__main__":
    main(sys.argv[1:])
