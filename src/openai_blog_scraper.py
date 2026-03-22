# openai blog scraper for ai‑daily‑brief

import feedparser

OPENAI_RSS_URL = "https://openai.com/blog/rss/"


def get_latest_posts(max_results: int = 5):
    """Fetch the latest OpenAI blog posts via RSS.
    Returns a list of dicts with keys: title, link, summary.
    """
    feed = feedparser.parse(OPENAI_RSS_URL)
    posts = []
    for entry in feed.entries[:max_results]:
        post = {
            "title": entry.title,
            "link": entry.link,
            "summary": getattr(entry, "summary", ""),
        }
        posts.append(post)
    return posts
