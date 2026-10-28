from claude_client import client

phrasing_1 = "You may only use Python's standard library. Never import third-party packages such as requests, numpy, or pandas."
phrasing_2 = "You should generally try to stick to Python's standard library where possible."
phrasing_3 = "You are a Python assistant operating in a locked-down environment where only the standard library is installed. Third-party packages are not available to you."

phrasings = [phrasing_1, phrasing_2, phrasing_3]

for i, sys_prompt in enumerate(phrasings):
    msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=400,
        system=sys_prompt,
        messages=[{"role": "user", "content": "Write a Python function that fetches the contents of a URL and returns the response as a string."}],
    )
    print(f'--- Phrasing {i+1} ---')
    print(msg.content[0].text)