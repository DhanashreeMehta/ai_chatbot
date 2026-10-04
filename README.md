# MSAI 631 — Chatbot with Azure AI Language (Sentiment Analysis)

## Provenance
The base bot structure in this project was adapted from the Microsoft Bot
Framework echo bot sample. It was copied and extended for the MSAI 631
assignment to integrate the Azure AI Language service for sentiment analysis.
Original echo bot files are the starting point; all sentiment-related code
(`bots/sentiment_bot.py`, additions to `config.py`) is my own work.

## What it does
- Greets users and lists its capabilities (`help`)
- Analyzes the sentiment of any message using Azure AI Language
- Reports overall sentiment + confidence scores + sentence breakdown
- Handles empty and malformed input gracefully

## Setup
1. Create a free Azure AI Language resource (Free F0 tier).
2. Copy your endpoint and key.
3. Copy `.env.example` to `.env` (or use SET) and fill in values:
