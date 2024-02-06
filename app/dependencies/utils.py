from fastapi import HTTPException
from typing import Any
import httpx

async def get_json_response(url: str, headers: dict | None = None, error_message: str | None = None) -> Any:
  async with httpx.AsyncClient() as client:
    try:
      response = await client.get(url, headers=headers)
      response.raise_for_status()
      return response.json()
    except httpx.HTTPStatusError as error:
      raise HTTPException(status_code=error.response.status_code, detail=error_message)