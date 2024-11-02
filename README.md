# Conversations Inference Server

## Overview

A FastAPI server that processes user and store messages, maintains context using Redis, and infers intents using a locally loaded LLM. It responds with both the intent and the appropriate message template based on the message source.

## Features

-   **POST /inference**: Accepts a phone number, message, and a flag indicating whether the message is from a store. Stores the message, maintains conversation context, and returns the inferred intent and corresponding message template.
-   **Context Management**: Stores and retrieves messages per phone number to maintain conversation context.
-   **LLM Integration**: Uses a locally loaded Hugging Face model to determine intent.
-   **Intent Whitelisting**: Ensures only predefined intents are recognized; otherwise, returns `unknown_intent`.
-   **Template Mapping**: Maps each intent to a specific message template.
-   **Performance**: Utilizes Redis for fast in-memory data storage.

## Setup

### Prerequisites

-   Python 3.8+
-   Redis Server
-   Sufficient memory for the LLM model

### Installation

1. **Clone the repository**

    ```bash
    git clone https://github.com/locality/conversations.git
    cd conversations
    ```
