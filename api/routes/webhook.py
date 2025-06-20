"""LINE Webhook API"""

from fastapi import APIRouter, Request, Header

router = APIRouter()

@router.post("/line")
async def line_webhook(
    request: Request,
    x_line_signature: str = Header(None)
):
    """LINE Webhook処理"""
    body = await request.body()
    return "OK" 