"""AI応答サービス"""

import logging
import google.generativeai as genai
from typing import Optional

from app.config import settings

logger = logging.getLogger(__name__)


class AIService:
    """AI応答サービス"""
    
    def __init__(self):
        """初期化"""
        # Gemini API設定
        genai.configure(api_key=settings.google_api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')
    
    def generate_response(self, user_id: str, message: str) -> str:
        """AI応答生成"""
        try:
            logger.info(f"Generating AI response for user {user_id}: {message[:50]}...")
            
            # プロンプト構築（知識ベースなし）
            prompt = self._build_prompt(message)
            
            # Gemini API で応答生成
            response = self.model.generate_content(prompt)
            
            ai_response = response.text.strip()
            logger.info(f"AI response generated: {ai_response[:50]}...")
            
            return ai_response
            
        except Exception as e:
            logger.error(f"Error generating AI response: {str(e)}")
            return self._get_fallback_response()
    
    def _build_prompt(self, user_message: str) -> str:
        """プロンプト構築"""
        return f"""あなたは陸上競技の練習アドバイザーです。特に中長距離ランナーの練習相談に専門的にお答えします。

【ユーザーからの相談】
{user_message}

【応答指針】
1. 科学的根拠に基づいた専門的なアドバイスを提供
2. ユーザーの安全を最優先に考慮
3. 親しみやすく、分かりやすい言葉で説明
4. 必要に応じて具体的な練習メニューを提案
5. 怪我のリスクがある場合は適切に警告
6. 必要に応じてランニングクリニックの受診を勧める

上記を踏まえて、専門的かつ親しみやすい回答をお願いします。"""
    
    def _get_fallback_response(self) -> str:
        """フォールバック応答"""
        return """ありがとうございます！

申し訳ございませんが、現在システムの調子が良くないようです。
お急ぎの場合は、以下をお試しください：

🏃‍♂️ 基本的な練習についてのご質問
🏥 怪我や痛みについてのご相談
📊 練習記録の分析について

しばらく時間をおいてから、再度ご相談ください。
より詳しいアドバイスが必要でしたら、ランニングクリニックでの診察もご検討ください。""" 