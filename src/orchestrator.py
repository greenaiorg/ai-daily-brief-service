# orchestrator script for AI daily brief service

import os
import sys

# Ensure src directory is on sys.path for imports
sys.path.append(os.path.dirname(__file__))

from scraper import get_latest_papers
from summarizer import summarize_texts
from emailer import send_email


def run():
    # Retrieve latest papers (e.g., from arXiv)
    papers = get_latest_papers()
    # Extract abstracts for summarization
    abstracts = [p["summary"] for p in papers]
    # Summarize using the summarizer stub
    summaries = summarize_texts(abstracts)
    # Build email body
    lines = []
    for paper, summary in zip(papers, summaries):
        lines.append(f"Title: {paper['title']}")
        lines.append(f"Link: {paper['link']}")
        lines.append(f"Summary: {summary}")
        lines.append("")
    body = "\n".join(lines)
    # Recipients list from environment variable (comma‑separated)
    recipients = os.getenv("DAILY_BRIEF_RECIPIENTS", "")
    for rcpt in [r.strip() for r in recipients.split(",") if r.strip()]:
        send_email(to=rcpt, subject="Daily AI Research Brief", body=body)


if __name__ == "__main__":
    run()
