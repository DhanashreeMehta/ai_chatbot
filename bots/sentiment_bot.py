#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
#
# Extended for MSAI 631 Project - adds Azure AI Language sentiment analysis.

from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount

# From https://learn.microsoft.com/en-us/python/api/overview/azure/ai-textanalytics-readme
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

from config import DefaultConfig


class SentimentBot(ActivityHandler):
    """
    A simple chatbot that analyzes the sentiment of user messages using
    the Azure AI Language service. Demonstrates integrating an
    AI-as-a-service offering into a conversational interface.
    """

    def __init__(self, config: DefaultConfig):
        self.config = config
        self.client = None

        # Only create the client if credentials were supplied. This lets the
        # bot start cleanly even if the environment variables are missing,
        # and surfaces a friendly message to the user instead of crashing.
        if config.API_KEY and config.ENDPOINT_URI:
            credential = AzureKeyCredential(config.API_KEY)
            self.client = TextAnalyticsClient(
                endpoint=config.ENDPOINT_URI, credential=credential
            )

    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        """Greet new users and advertise capabilities."""
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    "👋 Hi! I'm a sentiment analysis bot powered by Azure AI. "
                    "Type 'help' to see what I can do, or just send me a sentence "
                    "and I'll tell you how it feels."
                )

    async def on_message_activity(self, turn_context: TurnContext):
        """Main message handler."""
        user_text = (turn_context.activity.text or "").strip()

        # --- Handle malformed / empty input gracefully ---
        if not user_text:
            await turn_context.send_activity(
                "I didn't catch that. Please send me some text to analyze."
            )
            return

        # --- Capabilities command (required: list capabilities) ---
        if user_text.lower() in ("help", "/help", "capabilities", "what can you do"):
            await turn_context.send_activity(self._capabilities_text())
            return

        # --- Guard against a missing/misconfigured AI client ---
        if self.client is None:
            await turn_context.send_activity(
                "⚠️ My AI service isn't configured. Please set the "
                "MicrosoftAIServiceEndpoint and MicrosoftAPIKey environment "
                "variables and restart me."
            )
            return

        # --- Call the Azure AI Language sentiment analysis API ---
        try:
            documents = [user_text]
            response = self.client.analyze_sentiment(
                documents=documents, language="en"
            )
            # Filter out any error documents returned by the service.
            results = [doc for doc in response if not doc.is_error]

            if not results:
                await turn_context.send_activity(
                    "Hmm, I couldn't analyze that. Try a different sentence."
                )
                return

            doc = results[0]
            reply = self._format_sentiment(doc)
            await turn_context.send_activity(reply)

        except Exception as exc:  # noqa: BLE001 - surface a friendly message
            await turn_context.send_activity(
                "Sorry, something went wrong while contacting the AI service. "
                "Please try again."
            )
            print(f"[SentimentBot] API error: {exc}")

    @staticmethod
    def _capabilities_text() -> str:
        return (
            "Here is what I can do:\n"
            "• Analyze the overall sentiment of your message (positive, "
            "neutral, or negative)\n"
            "• Report confidence scores for each sentiment\n"
            "• Break down sentiment sentence by sentence\n"
            "• Handle empty or malformed input without crashing\n\n"
            "Just type a sentence to get started!"
        )

    @staticmethod
    def _format_sentiment(doc) -> str:
        """Turn the raw SDK result into a friendly, readable reply."""
        scores = doc.confidence_scores
        emoji = {"positive": "😊", "neutral": "😐", "negative": "😞"}.get(
            doc.sentiment, "🤖"
        )

        lines = [
            f"{emoji} Overall sentiment: **{doc.sentiment.upper()}**",
            f"   Confidence — positive: {scores.positive:.2f}, "
            f"neutral: {scores.neutral:.2f}, negative: {scores.negative:.2f}",
        ]

        if len(doc.sentences) > 1:
            lines.append("\nSentence breakdown:")
            for i, sentence in enumerate(doc.sentences, start=1):
                lines.append(f"   {i}. [{sentence.sentiment}] {sentence.text}")

        return "\n".join(lines)
