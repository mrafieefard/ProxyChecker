from v2ray2proxy import V2RayProxy
import aiohttp
import asyncio
import time
from urllib.parse import urlparse, parse_qs
from telethon import TelegramClient
from telethon.network.connection import ConnectionTcpMTProxyRandomizedIntermediate
import traceback
import base64
from config import API_ID, API_HASH
import re
from config import SECRET_KEY
from fastapi import HTTPException,status

def validate_secret_key(secret_key: str) -> bool:
    if secret_key != SECRET_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid secret key")
    return True

_HEX_RE = re.compile(r"^[0-9a-fA-F]+$")

async def check_v2ray(proxy_url):
    proxy = V2RayProxy(proxy_url)

    try:
        # Use with aiohttp
        async with aiohttp.ClientSession() as session:
            start = time.perf_counter()
            async with session.get(
                "https://api.ipify.org?format=json", proxy=proxy.http_proxy_url,timeout=5
            ) as response:
                ip = await response.json()
                total_time = time.perf_counter() - start
                return total_time
    except:
        return None
    finally:
        # Always stop the proxy when done
        proxy.stop()

def _secret_to_hex_str(secret_raw: str) -> str | None:
    """
    Returns a hex string suitable for Telethon (str), or None if invalid.
    Accepts:
      - hex secrets (already)
      - base64/url-safe base64 secrets from t.me/proxy
    """
    s = secret_raw.strip()

    # If it's already hex, keep it.
    if _HEX_RE.fullmatch(s) and len(s) % 2 == 0:
        return s.lower()

    # Otherwise treat it as url-safe base64 (Telegram links commonly use this)
    try:
        padded = s + "=" * (-len(s) % 4)
        b = base64.urlsafe_b64decode(padded)
    except Exception:
        return None

    # Telethon wants hex-string
    return b.hex()

def _parse_mtproto_link(proxy_link: str) -> tuple[str, int, str] | None:
    u = urlparse(proxy_link)
    q = parse_qs(u.query)

    host = (q.get("server") or [None])[0]
    port_raw = (q.get("port") or [None])[0]
    secret_raw = (q.get("secret") or [None])[0]

    if not host or not port_raw or not secret_raw:
        return None

    try:
        port = int(port_raw)
    except ValueError:
        return None

    secret_hex = _secret_to_hex_str(secret_raw)
    if not secret_hex:
        return None

    return host, port, secret_hex

async def check_telegram(proxy_link: str) -> float | None:
    parsed = _parse_mtproto_link(proxy_link)
    if not parsed:
        return None

    host, port, secret = parsed

    client = TelegramClient(
        "proxy_test_session",
        API_ID,
        API_HASH,
        connection=ConnectionTcpMTProxyRandomizedIntermediate,
        proxy=(host, port, secret)
    )

    start = time.perf_counter()
    try:
        await asyncio.wait_for(client.connect(), timeout=5)
        if not client.is_connected():
            return None
        return time.perf_counter() - start
    except Exception:
        traceback.print_exc()
        return None
    finally:
        try:
            await client.disconnect()
        except Exception:
            pass