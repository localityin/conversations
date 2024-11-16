# Conversations Inference Application

This is a scalable locality inference application built with FastAPI, Redis for caching, and MongoDB for persistent storage. It uses a Meta LLaMA 3.2 1B language model to infer user intents based on contextual inputs. The application is designed for production-grade deployment with Docker and features robust logging.

## Features

-   Intent Inference: Leverages a fine-tuned language model to infer user intents based on their messages.
-   Context Awareness: Incorporates recent user messages (from Redis cache) for contextual inference.
-   Robust Logging: Logs user messages, context, and inferred intents into dated log files.
-   Data Persistence: Backs up Redis cache data to MongoDB on shutdown and restores it on startup.
-   Dockerized Deployment: Easily deployable using Docker Compose.
-   Configurable Resources: Fine-grained control over resource allocation for services via Docker.

## Table of Contents

-   Getting Started
-   Project Structure
-   Endpoints
-   Environment Variables
-   Deployment
-   Logging
-   Future Improvements

## Getting Started

### Prerequisites

-   Python 3.10+
-   Docker and Docker Compose
-   Redis
-   MongoDB

### Installation

1. Clone the repository:

```bash
git clone https://github.com/localityin/conversations.git
cd conversations
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables in a .env file:

```
MONGO_URI=mongodb://localhost:27017/
REDIS_HOST=localhost
REDIS_PORT=6379
MODEL_NAME=meta-llama/Llama-3.2-1b-Instruct
HUGGINGFACE_TOKEN=your_huggingface_api_token
```

5. Run the application:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Project Structure

```
conversations/
├── app/
│   ├── __init__.py
│   ├── main.py               # FastAPI application entry point
│   ├── config.py             # Configuration for environment variables
│   ├── models.py             # Pydantic models for requests
│   ├── services/             # Redis and MongoDB services
│   │   ├── redis_service.py
│   │   ├── mongo_service.py
│   ├── utils/
│       ├── inference.py      # Model inference logic
│       ├── logger.py         # Logging utility
├── logs/                     # Directory for log files
├── .env                      # Environment variables
├── Dockerfile                # Dockerfile for building the app image
├── docker-compose.yml        # Docker Compose configuration
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

## Endpoints

### 1. POST /inference

Perform intent inference based on user messages.

**Request**

```json
{
	"user_id": "usr_1234rfhyu87",
	"message": "Hey, I want to create an account"
}
```

**Response**

```json
{
	"intent": "user_welcome_onboarding"
}
```

## Environment Variables

Define the following in a .env file:

| Variable          | Description                                               |
| ----------------- | --------------------------------------------------------- |
| MONGO_URI         | MongoDB connection URI (e.g., mongodb://localhost:27017/) |
| REDIS_HOST        | Redis server host (e.g., localhost)                       |
| REDIS_PORT        | Redis server port (e.g., 6379)                            |
| MODEL_NAME        | Name of the Hugging Face model to load                    |
| HUGGINGFACE_TOKEN | API token for accessing Hugging Face models               |

## Deployment

### With Docker Compose

1. Build and start the application:

```bash
docker-compose up --build
```

2. Access the application at http://localhost:8000

## Logging

The application uses a structured logging setup. Logs are stored in `logs/` with daily rotation.

### Example Log

```
2024-11-16 14:35:21,123 - INFO - User message: Hey I want to create an account
2024-11-16 14:35:21,124 - DEBUG - Context passed to model: <context>
2024-11-16 14:35:21,400 - DEBUG - Model generated response: user_welcome_onboarding
2024-11-16 14:35:21,401 - INFO - Extracted intent: user_welcome_onboarding
```

## Future Improvements

-   Model Optimization: Implement GPU acceleration for faster inference.
-   Horizontal Scaling: Add support for running multiple instances with a load balancer.
-   Enhanced Context Handling: Expand the context window for more complex interactions.
-   Monitoring and Alerts: Integrate tools like Prometheus and Grafana for system monitoring.

## Contributing

Feel free to fork the repository, submit issues, or make pull requests to contribute to the project.

## License

This project is licensed under the MIT License.
