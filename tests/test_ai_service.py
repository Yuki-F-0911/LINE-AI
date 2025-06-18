"""AIサービスのテスト"""

import pytest
import os
from dotenv import load_dotenv
from unittest.mock import Mock, patch
from core.services.ai_service import AIService

# .envファイルの読み込み
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)


class TestAIService:
    """AIサービステスト"""
    
    @patch('core.services.ai_service.genai.GenerativeModel')
    def test_generate_response_success(self, mock_model_class):
        """正常な応答生成テスト"""
        mock_model_instance = Mock()
        mock_response = Mock()
        mock_response.text = "テスト応答です。"
        mock_model_instance.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model_instance

        with patch('core.services.ai_service.settings') as mock_settings:
            mock_settings.google_api_key = "test_api_key"
            ai_service = AIService()
            with patch.object(ai_service, 'knowledge_base') as mock_kb:
                mock_kb.search_relevant_knowledge.return_value = "テスト知識"
                result = ai_service.generate_response(
                    user_id="test_user",
                    message="テストメッセージ"
                )
        assert result == "テスト応答です。"
        mock_kb.search_relevant_knowledge.assert_called_once_with("テストメッセージ")
        mock_model_instance.generate_content.assert_called_once()

    @patch('core.services.ai_service.genai.GenerativeModel')
    def test_generate_response_error(self, mock_model_class):
        """エラー時のフォールバック応答テスト"""
        mock_model_instance = Mock()
        mock_model_instance.generate_content.side_effect = Exception("API Error")
        mock_model_class.return_value = mock_model_instance

        with patch('core.services.ai_service.settings') as mock_settings:
            mock_settings.google_api_key = "test_api_key"
            ai_service = AIService()
            with patch.object(ai_service, 'knowledge_base') as mock_kb:
                mock_kb.search_relevant_knowledge.return_value = "テスト知識"
                result = ai_service.generate_response(
                    user_id="test_user",
                    message="テストメッセージ"
                )
        assert "申し訳ございません" in result
        assert "システムの調子が良くない" in result

    def test_build_prompt(self):
        """プロンプト構築テスト"""
        with patch('core.services.ai_service.settings') as mock_settings:
            mock_settings.google_api_key = "test_api_key"
            ai_service = AIService()
            user_message = "ジョギングについて教えて"
            relevant_knowledge = "ジョギングは有酸素運動の基本です。"
            prompt = ai_service._build_prompt(user_message, relevant_knowledge)
            assert "陸上競技の練習アドバイザー" in prompt
            assert user_message in prompt
            assert relevant_knowledge in prompt
            assert "科学的根拠" in prompt

    def test_get_fallback_response(self):
        """フォールバック応答テスト"""
        with patch('core.services.ai_service.settings') as mock_settings:
            mock_settings.google_api_key = "test_api_key"
            ai_service = AIService()
            result = ai_service._get_fallback_response()
            assert "申し訳ございません" in result
            assert "システムの調子が良くない" in result
            assert "ランニングクリニック" in result 