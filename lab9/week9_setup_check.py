#!/usr/bin/env python3
"""
Week 9 setup check. Run this BEFORE the lab (it is part of the self-paced module).

    pip install chromadb anthropic
    python week9_setup_check.py

It checks that:
  1. Python is new enough,
  2. the packages import,
  3. the local embedding model can be downloaded and run (the first run downloads it: be patient,
     and do it on a good network, not in the middle of class),
  4. semantic search ranks a paraphrase above an unrelated sentence.
It makes NO API calls and needs no API key.
"""
import sys

print("1. Python version:", sys.version.split()[0])
if sys.version_info < (3, 9):
    sys.exit("   Please use Python 3.9 or newer.")

try:
    import numpy as np
except ImportError:
    sys.exit("2. numpy is missing. Run: pip install chromadb   (it installs numpy too)")

try:
    from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
    print("2. chromadb imports: OK")
except ImportError:
    sys.exit("2. chromadb is missing. Run: pip install chromadb")

try:
    import anthropic  # noqa: F401
    print("   anthropic imports: OK")
except ImportError:
    print("   anthropic is missing (you need it for the lab, not for this check). Run: pip install anthropic")

print("3. Loading the local embedding model (the first run downloads it)...")
try:
    embed = DefaultEmbeddingFunction()
    texts = [
        "Customers can get a refund within 14 days of purchase.",   # 0: the document
        "How long do I have to get my money back?",                  # 1: a paraphrased question
        "The release freeze starts on Monday at 17:00.",             # 2: an unrelated sentence
    ]
    vectors = np.array(embed(texts), dtype=float)
except Exception as exc:                                             # network, disk, firewall...
    sys.exit(f"   The embedding model could not be loaded: {type(exc).__name__}: {exc}\n"
             "   Check your network connection, free disk space, and that a VPN or proxy is not blocking downloads.\n"
             "   If it still fails, tell a TA before the lab.")
print(f"   OK: each text became a vector of {vectors.shape[1]} numbers")

vectors = vectors / np.linalg.norm(vectors, axis=1, keepdims=True)
sim_related, sim_unrelated = float(vectors[0] @ vectors[1]), float(vectors[0] @ vectors[2])
print("4. Semantic search check")
print(f"   document vs paraphrased question : {sim_related:.2f}")
print(f"   document vs unrelated sentence   : {sim_unrelated:.2f}")
if sim_related > sim_unrelated:
    print("   PASS. The paraphrase scores higher even though it shares almost no words with the document.")
else:
    print("   Unexpected: the unrelated sentence scored higher. Tell a TA, and include this output.")
print("\nAll set. You are ready for the Week 9 lab.")
