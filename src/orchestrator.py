# orchestrator script for AI daily brief service

import os
import sys

# Ensure src directory is on sys.path for imports
sys.path.append(os.path.dirname(__file__))

from scraper import get_latest_papers
from openai_blog_scraper import get_latest_posts
from summarizer import summarize_texts
from emailer import send_email
from subscriptions import load_subscribers


def run():
    # Retrieve latest papers (e.g., from arXiv)
    papers = get_latest_papers()
    # Retrieve latest OpenAI blog posts
    blog_posts = get_latest_posts()
    # Combine both sources
    combined = papers + blog_posts
    # Extract summaries/abstracts for summarization (use 'summary' key for both)
    abstracts = [item.get("summary", "") for item in combined]
    # Summarize using the summarizer stub
    summaries = summarize_texts(abstracts)

    # Build email body
    lines = []
    for item, summary in zip(combined, summaries):
        lines.append(f"Title: {item.get('title', 'N/A')}")
        lines.append(f"Link: {item.get('link', 'N/A')}")
        lines.append(f"Summary: {summary}")
        lines.append("")
    body = "\n".join(lines)

    # Load recipients from subscription list
    recipients = load_subscribers()
    # If no subscribers, fallback to env variable list
    if not recipients:
        env_recipients = os.getenv("DAILY_BRIEF_RECIPIENTS", "")
        recipients = [r.strip() for r in env_recipients.split(",") if r.strip()]

    for rcpt in recipients:
        send_email(to=rcpt, subject="Daily AI Research Brief", body=body)


if __name__ == "__main__":
    run()
