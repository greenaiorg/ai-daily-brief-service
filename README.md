# AI Daily Brief Service

this repository implements an ai‑powered daily brief service that scrapes the latest ai research papers, summarises each with a local large language model, and emails a concise digest to subscribers.

## features

- daily scraping of arxiv, open‑ai blog, and other ai venues
- automatic summarisation using a locally hosted llm (e.g. llama.cpp or llama‑2)
- email generation and dispatch via gmail api
- simple subscription management (add/remove email addresses)

## stack

- python 3.11+ 
- requests / beautifulsoup4 for web scraping
- llama.cpp for on‑device llm inference
- google api client for gmail

## getting started

```bash
# clone the repo (already done)
cd ai-daily-brief-service
# create virtual env
python -m venv .venv
source .venv/bin/activate
# install dependencies
pip install -r requirements.txt
# configure .env (see .env.example)
# run the daily job locally for testing
python -m src.main
```

## deployment

use a cron job or github actions to run the scraper daily and send the email.
