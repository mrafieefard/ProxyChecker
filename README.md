# Proxy Checker API

A FastAPI-based proxy checker service that validates V2Ray and Telegram proxies.

## Features

- V2Ray proxy validation
- Telegram proxy validation (placeholder)
- FastAPI web interface with automatic documentation
- Docker support for easy deployment
- Environment-based configuration

## Requirements

- Python 3.11+
- Docker (optional)
- Telegram API credentials (API_ID and API_HASH)

## Docker Setup

### Using Docker Compose (Recommended)

1. Copy the environment template:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your actual values:
   ```bash
   API_ID=your_telegram_api_id
   API_HASH=your_telegram_api_hash
   SECRET_KEY=your_secret_key
   ```

3. Build and run:
   ```bash
   docker-compose up --build
   ```

### Using Docker directly

1. Build the image:
   ```bash
   docker build -t proxy-checker .
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 \
     -e API_ID=your_api_id \
     -e API_HASH=your_api_hash \
     -e SECRET_KEY=your_secret_key \
     proxy-checker
   ```

## Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables in `.env` file

3. Run the application:
   ```bash
   python main.py
   ```

## Usage

Once running, visit:
- API Documentation: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

### API Endpoint

**POST /check**

Request body:
```json
{
  "url": "your_proxy_url",
  "proxy_type": "v2ray"
}
```

Headers:
- `secret-key`: Your API secret key

Response:
```json
{
  "is_valid": true,
  "latency": 150
}
```

## Environment Variables

- `API_ID`: Your Telegram API ID
- `API_HASH`: Your Telegram API Hash  
- `SECRET_KEY`: Secret key for API authentication

## Getting Telegram API Credentials

1. Go to https://my.telegram.org/auth
2. Log in with your phone number
3. Go to "API Development tools"
4. Create a new application
5. Copy your `API_ID` and `API_HASH`