"""LINE Bot サービス"""

import logging
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from linebot.v3.exceptions import BaseError

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
            # エラー時はデフォルトメッセージを送信（テスト環境では無効なreply_tokenの場合がある）
            error_message = "申し訳ございません。一時的にサービスが利用できません。しばらく時間をおいてから再度お試しください。"
            try:
                self.reply_message(event.reply_token, error_message)
            except Exception as reply_error:
                logger.warning(f"Error sending error message (likely test environment): {str(reply_error)}")
    
    def reply_message(self, reply_token: str, message: str) -> None:
        """メッセージ返信"""
        try:
            # テスト用のreply_tokenの場合はスキップ
            if reply_token.startswith('test_'):
                logger.info(f"Test reply token detected, skipping actual LINE API call: {message[:50]}...")
                return
                
            reply_request = ReplyMessageRequest(
                reply_token=reply_token,
                messages=[TextMessage(text=message)]
            )
            
            self.messaging_api.reply_message(reply_request)
            logger.info(f"Reply sent successfully: {message[:50]}...")
            
        except BaseError as e:
            error_msg = str(e).lower()
            if "reply token" in error_msg and ("expired" in error_msg or "invalid" in error_msg):
                logger.warning(f"Reply token expired or invalid (likely test environment): {str(e)}")
            else:
                logger.error(f"LINE Bot API error sending reply: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error sending reply: {str(e)}")
            raise 