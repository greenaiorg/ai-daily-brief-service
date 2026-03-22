# summarizer module for ai‑daily‑brief

"""
Placeholder for the summarisation logic using a local LLM.
In a full implementation this would load a model via llama‑cpp‑python
and generate a concise summary of the paper abstract or full text.
"""

from typing import List


def summarize_texts(texts: List[str]) -> List[str]:
    """Return a list of short summaries for each input text.

    Currently this is a stub – it just returns the first 200 characters
    with an ellipsis. Replace with actual LLM inference when ready.
    """
    summaries = []
    for t in texts:
        summary = t[:200].strip()
        if len(t) > 200:
            summary += "..."
        summaries.append(summary)
    return summaries


if __name__ == "__main__":
    # simple demo
    example = ["""Large language models have shown remarkable abilities in \
    natural language processing tasks, but they also raise concerns about \
    bias, compute cost, and environmental impact. This paper surveys recent \
    advancements and discusses future directions."""]
    for s in summarize_texts(example):
        print(s)
