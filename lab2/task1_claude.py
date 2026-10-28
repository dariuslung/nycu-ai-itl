import json
from claude_client import client

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

file_paths = {
    "sentence": "./task1_file/sentence.txt",
    "paragraph": "./task1_file/paragraph.txt",
    "mandarin": "./task1_file/mandarin.txt",
    "code": "./task1_file/functions.py",
    "json_obj": "./task1_file/info.json",
}

inputs = {}
for name, path in file_paths.items():
    raw = read_file(path)
    if path.endswith(".json"):
        # Re-serialize so token counting reflects the same text
        # the model would actually see if passed the parsed object
        raw = json.dumps(json.loads(raw))
    inputs[name] = raw

for name, text in inputs.items():
    result = client.messages.count_tokens(
        model="claude-sonnet-4-6",
        messages=[{"role": "user", "content": text}],
    )
    char_count = len(text)
    token_count = result.input_tokens
    ratio = char_count / token_count if token_count else 0
    print(f"{name}: {char_count} chars, {token_count} tokens, {ratio:.2f} chars/token")