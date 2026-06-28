import os
import logging
from typing import Any

import httpx
from pydantic import BaseModel


PUBSUB_NAME = os.getenv("DAPR_PUBSUB_NAME", "pubsub")
logger = logging.getLogger("uvicorn.error")


def _dapr_url(path: str) -> str:
    port = os.getenv("DAPR_HTTP_PORT", "3500")
    return f"http://localhost:{port}{path}"


async def publish_event(topic: str, payload: BaseModel | dict[str, Any]) -> None:
    body = payload.model_dump(mode="json") if isinstance(payload, BaseModel) else payload
    url = _dapr_url(f"/v1.0/publish/{PUBSUB_NAME}/{topic}")
    async with httpx.AsyncClient(timeout=5) as client:
        response = await client.post(url, json=body)
        response.raise_for_status()
    logger.info("Published Dapr event topic=%s pubsub=%s payload=%s", topic, PUBSUB_NAME, body)


async def invoke_service(app_id: str, method: str, params: dict[str, Any] | None = None) -> Any:
    url = _dapr_url(f"/v1.0/invoke/{app_id}/method/{method.lstrip('/')}")
    async with httpx.AsyncClient(timeout=5) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
    logger.info("Invoked Dapr service app_id=%s method=%s params=%s", app_id, method, params)
    return data
