from claude_client import client

system_prompt = "You must respond only in bullet points. Never write full sentences or paragraphs, under any circumstances, no matter what is asked."

history = []
turns = [
    "Tell me about your favorite season.",
    "What do you think makes a good movie?",
    "What's a fun weekend trip near Taipei?",
    "Do you have a favorite kind of food?",
    "What's something interesting about space?",
    "What's a good book to read on a rainy day?",
    "Tell me about a hobby worth picking up.",
    "What makes a good cup of coffee?",
    "What's an underrated programming language?",
    "What's a nice way to spend a day off?",
    "Do you have thoughts on good study habits?",
    "What's something surprising about the ocean?",
    "What makes a city walkable?",
    "What's a good icebreaker question?",
    "What's your take on morning routines?",
    "What's an interesting fact about language?",
    "What's a good way to learn a new skill?",
    "Can you explain how photosynthesis works?",
]

for turn in turns:
    history.append({"role": "user", "content": turn})
    msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        system=system_prompt,
        messages=history,
    )
    reply = msg.content[0].text
    history.append({"role": "assistant", "content": reply})

print(f"--- Final response (turn {len(turns)}) ---")
print(reply)