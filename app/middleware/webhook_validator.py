from starlette.middleware.base import BaseHTTPMiddleware
import os
import hmac
import hashlib
from fastapi import Request, Response
from dotenv import load_dotenv
import json
import asyncio

class WebhookValidator(BaseHTTPMiddleware):
    load_dotenv()
    SECRET = os.getenv('GIT_WEBHOOK_SECRET')

    EXCLUDE_ROUTES = [
        "/healthcheck",
        "/docs",
        "/redoc",
        "/openapi.json",
        "/favicon.ico"
    ]

    def compute_hmac(self, payload: bytes) -> str:
        print("Secret:", self.SECRET)
        if not self.SECRET:
            raise ValueError("Webhook secret is not set")
        # Await the coroutine to get the payload bytes
        if asyncio.iscoroutine(payload):
            payload_bytes =  payload
        else:
            payload_bytes = payload

        # Try to decode bytes to string and parse as JSON
        try:
            # payload_json = json.loads(payload_bytes.decode('utf-8'))
            payload_str = json.dumps(payload_json, separators=(',', ':'))
        except Exception:
            payload_str = payload_bytes.decode('utf-8')

        print("Payload:", payload_str)
        digest = hmac.new(
            self.SECRET.encode('utf-8'),
            payload_str.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return digest

    def validate(self, request, x_hub_signature: str = None):
        # Implement validation logic here
        # For example, check headers or body against the secret
        if x_hub_signature != f'sha256={self.compute_hmac(request.decode('utf-8'))}':
            raise ValueError("Invalid webhook secret")
        return True
    
    async def dispatch(self, request: Request, call_next):
        try:
            request_body = await request.body()
            
            self.validate(request_body, request.headers.get('X-Hub-Signature-256'))
        except ValueError as e:
            return Response(str(e), status_code=400)
        request = Request(request.scope)
        response = await call_next(request)
        return response