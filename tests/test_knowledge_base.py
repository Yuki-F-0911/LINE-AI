"""知識ベースのテスト（簡易版）"""

import pytest
from core.ai.rag.knowledge_base import KnowledgeBase


class TestKnowledgeBase:
    """知識ベーステスト（簡易版）"""
    
    def setup_method(self):
        """テスト前の準備"""
        self.knowledge_base = KnowledgeBase()
    
    def test_search_relevant_knowledge_jogging(self):
        """ジョギング関連知識検索テスト"""
        result = self.knowledge_base.search_relevant_knowledge("ジョギングについて教えて")
        
        # 検証
        assert "ジョギング" in result
        assert "有酸素運動" in result
        assert "初心者" in result
    
    def test_search_relevant_knowledge_interval(self):
        """インターバル走関連知識検索テスト"""
        result = self.knowledge_base.search_relevant_knowledge("インターバル走の効果")
        
        # 検証
        assert "インターバル" in result
        assert "最大酸素摂取量" in result
        assert "回復" in result
    
    def test_search_relevant_knowledge_injury(self):
        """怪我予防関連知識検索テスト"""
        result = self.knowledge_base.search_relevant_knowledge("怪我を防ぐには")
        
        # 検証
        assert "怪我" in result
        assert "ウォームアップ" in result
        assert "ストレッチ" in result
    
    def test_search_relevant_knowledge_no_match(self):
        """マッチしないクエリのテスト"""
        result = self.knowledge_base.search_relevant_knowledge("サッカーの練習方法")
        
        # 検証
        assert "基本的な練習指導の原則" in result
    
    def test_add_knowledge(self):
        """新しい知識追加テスト"""
        new_text = "マラソン完走のための練習法：週4回、徐々に距離を延ばす。"
        result = self.knowledge_base.add_knowledge(
            text=new_text,
            category="マラソン"
        )
        
        # 検証
        assert result is True
        
        # 追加された知識が検索できるかテスト
        search_result = self.knowledge_base.search_relevant_knowledge("マラソン")
        assert "マラソン完走" in search_result
    
    def test_knowledge_base_initialization(self):
        """知識ベース初期化テスト"""
        assert len(self.knowledge_base.knowledge_base) == 4
        
        # 各知識の構造確認
        for knowledge in self.knowledge_base.knowledge_base:
            assert "id" in knowledge
            assert "text" in knowledge
            assert "category" in knowledge
            assert "keywords" in knowledge 