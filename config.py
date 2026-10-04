#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
#
# Original source: Bot Framework echo bot sample.
# Copied and extended for MSAI 631 to add Azure AI sentiment analysis.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")

    # --- Added to support interaction with Azure AI Language API ---
    # Read secrets from environment variables rather than hard-coding them.
    # Set locally with:
    #   SET MicrosoftAIServiceEndpoint=https://<resource-name>.cognitiveservices.azure.com/
    #   SET MicrosoftAPIKey=<your-key>
    ENDPOINT_URI = os.environ.get("MicrosoftAIServiceEndpoint", "")
    API_KEY = os.environ.get("MicrosoftAPIKey", "")
