from pydantic import BaseModel
from enum import Enum
from typing import Optional

class ProxyType(Enum):
    telegram = "telegram"
    v2ray = "v2ray"

class CheckProxyPayload(BaseModel):
    proxy_type: ProxyType
    url: str

class CheckProxyResult(BaseModel):
    is_valid: bool
    latency: Optional[int] = None
