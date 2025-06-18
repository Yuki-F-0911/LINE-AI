"""LINE Bot サービス"""

import logging
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage
from linebot.v3.webhooks import MessageEvent, TextMessageContent

from app.config import settings
from core.services.ai_service import AIService

logger = logging.getLogger(__name__)


class LineService:
    """LINE Bot サービス"""
    
    def __init__(self):
        """初期化"""
        self.configuration = Configuration(access_token=settings.line_channel_access_token)
        self.api_client = ApiClient(self.configuration)
        self.messaging_api = MessagingApi(self.api_client)
        self.ai_service = AIService()
    
    def handle_text_message(self, event: MessageEvent) -> None:
        """テキストメッセージ処理"""
        try:
            user_id = event.source.user_id
            message_text = event.message.text
            
            logger.info(f"User {user_id} sent: {message_text}")
            
            # AI応答を生成
            ai_response = self.ai_service.generate_response(user_id, message_text)
            
            # 応答送信
            self.reply_message(event.reply_token, ai_response)
            
        except Exception as e:
            logger.error(f"Error handling text message: {str(e)}")
            # エラー時はデフォルトメッセージを送信
            error_message = "申し訳ございません。一時的にサービスが利用できません。しばらく時間をおいてから再度お試しください。"
            self.reply_message(event.reply_token, error_message)
    
    def reply_message(self, reply_token: str, message: str) -> None:
        """メッセージ返信"""
        try:
            reply_request = ReplyMessageRequest(
                reply_token=reply_token,
                messages=[TextMessage(text=message)]
            )
            
            self.messaging_api.reply_message(reply_request)
            logger.info(f"Reply sent: {message[:50]}...")
            
        except Exception as e:
            logger.error(f"Error sending reply: {str(e)}")
            raise 