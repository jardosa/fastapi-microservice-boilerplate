import os
from typing import Any

import httpx
from pydantic import BaseModel


PUBSUB_NAME = os.getenv("DAPR_PUBSUB_NAME", "pubsub")


def _dapr_url(path: str) -> str:
    port = os.getenv("DAPR_HTTP_PORT", "3500")
    return f"http://localhost:{port}{path}"


async def publish_event(topic: str, payload: BaseModel | dict[str, Any]) -> None:
    body = payload.model_dump(mode="json") if isinstance(payload, BaseModel) else payload
    url = _dapr_url(f"/v1.0/publish/{PUBSUB_NAME}/{topic}")
    async with httpx.AsyncClient(timeout=5) as client:
        await client.post(url, json=body)


async def invoke_service(app_id: str, method: str, params: dict[str, Any] | None = None) -> Any:
    url = _dapr_url(f"/v1.0/invoke/{app_id}/method/{method.lstrip('/')}")
    async with httpx.AsyncClient(timeout=5) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json()

