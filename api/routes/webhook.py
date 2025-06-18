"""LINE Webhook API"""

from fastapi import APIRouter, Request, HTTPException, Header
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi
from linebot.v3.webhooks import MessageEvent, TextMessageContent
import logging

from app.config import settings
from core.services.line_service import LineService

logger = logging.getLogger(__name__)

router = APIRouter()

# LINE Bot設定
configuration = Configuration(access_token=settings.line_channel_access_token)
handler = WebhookHandler(settings.line_channel_secret)

# サービス初期化
line_service = LineService()

@router.post("/line")
async def line_webhook(
    request: Request,
    x_line_signature: str = Header(None)
):
    """LINE Webhook処理"""
    try:
        body = await request.body()
        body_str = body.decode('utf-8')
        
        logger.info(f"LINE Webhook received: {body_str}")
        logger.info(f"Signature: {x_line_signature}")
        
        # 署名検証
        handler.handle(body_str, x_line_signature)
        
        logger.info("Webhook processed successfully")
        return "OK"
        
    except InvalidSignatureError:
        logger.error("Invalid signature")
        raise HTTPException(status_code=400, detail="Invalid signature")
    except Exception as e:
        logger.error(f"Webhook error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@handler.add(MessageEvent, message=TextMessageContent)
def handle_text_message(event):
    """テキストメッセージ処理"""
    try:
        logger.info(f"Processing text message from user: {event.source.user_id}")
        logger.info(f"Message content: {event.message.text}")
        logger.info(f"Reply token: {event.reply_token}")
        
        # LINE serviceに処理を委譲
        line_service.handle_text_message(event)
        
        logger.info("Text message processed successfully")
        
    except Exception as e:
        logger.error(f"Text message handling error: {str(e)}")
        # エラー時も200を返してLINEに再送させない
        pass 