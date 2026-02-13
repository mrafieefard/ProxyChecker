from fastapi import FastAPI
from models import CheckProxyPayload, CheckProxyResult, ProxyType

from functions import check_v2ray,check_telegram
import uvicorn

app = FastAPI()


@app.post("/check", response_model=CheckProxyResult)
async def check_proxy_route(payload: CheckProxyPayload):
    if payload.proxy_type == ProxyType.v2ray:
        latency = await check_v2ray(payload.url)

        if latency is None:
            return CheckProxyResult(is_valid=False)

        return CheckProxyResult(is_valid=True, latency=int(latency * 1000))

    elif payload.proxy_type == ProxyType.telegram:
        return CheckProxyResult(is_valid=False)  # Placeholder until Telegram check is implemented
        latency = await check_telegram(payload.url)

        if latency is None:
            return CheckProxyResult(is_valid=False)
        
        return CheckProxyResult(is_valid=True, latency=int(latency * 1000))

        pass


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
