"""知識ベース管理（簡易版）"""

import logging
from typing import List, Dict

logger = logging.getLogger(__name__)


class KnowledgeBase:
    """知識ベース管理（簡易版）"""
    
    def __init__(self):
        """初期化"""
        # 基本的な練習知識をメモリに保存
        self.knowledge_base = [
            {
                "id": "basic_jogging",
                "text": "ジョギングは有酸素運動の基本で、心肺機能向上に効果的です。初心者は週3-4回、1回30-45分程度から始めましょう。話しながら走れるペースが適切です。",
                "category": "基本練習",
                "keywords": ["ジョギング", "有酸素運動", "初心者", "ペース"]
            },
            {
                "id": "interval_training",
                "text": "インターバル走は高い強度と低い強度を交互に繰り返す練習法です。最大酸素摂取量向上に効果的ですが、週1-2回に留め、十分な回復時間を確保しましょう。",
                "category": "高強度練習",
                "keywords": ["インターバル", "高強度", "最大酸素摂取量", "回復"]
            },
            {
                "id": "injury_prevention",
                "text": "怪我予防には適切なウォームアップ、クールダウン、ストレッチが重要です。急激な練習量増加は避け、痛みを感じたら休息を取りましょう。専門医の診察も考慮してください。",
                "category": "怪我予防",
                "keywords": ["怪我", "ウォームアップ", "ストレッチ", "痛み", "休息"]
            },
            {
                "id": "beginner_program",
                "text": "初心者向け練習プログラム：週3回、ジョギング20-30分から開始。徐々に時間を延ばし、8週間で45分程度を目標に。無理は禁物、体調に合わせて調整しましょう。",
                "category": "初心者向け",
                "keywords": ["初心者", "プログラム", "週3回", "無理"]
            }
        ]
        
        logger.info(f"簡易知識ベースを初期化しました（{len(self.knowledge_base)}件）")
    
    def search_relevant_knowledge(self, query: str, n_results: int = 3) -> str:
        """関連知識の検索（簡易版）"""
        try:
            # キーワードベースの簡易検索
            relevant_knowledge = []
            
            for knowledge in self.knowledge_base:
                score = 0
                query_lower = query.lower()
                
                # キーワードマッチング
                for keyword in knowledge["keywords"]:
                    if keyword.lower() in query_lower:
                        score += 1
                
                # カテゴリマッチング
                if knowledge["category"].lower() in query_lower:
                    score += 2
                
                if score > 0:
                    relevant_knowledge.append((score, knowledge["text"]))
            
            # スコア順にソート
            relevant_knowledge.sort(key=lambda x: x[0], reverse=True)
            
            # 上位n_results件を取得
            top_knowledge = relevant_knowledge[:n_results]
            
            if top_knowledge:
                knowledge_text = "\n\n".join([k[1] for k in top_knowledge])
                logger.info(f"関連知識 {len(top_knowledge)} 件を取得しました")
                return knowledge_text
            else:
                logger.warning("関連知識が見つかりませんでした")
                return "基本的な練習指導の原則に従って回答してください。"
                
        except Exception as e:
            logger.error(f"知識検索エラー: {str(e)}")
            return "基本的な練習指導の原則に従って回答してください。"
    
    def add_knowledge(self, text: str, category: str, knowledge_id: str = None) -> bool:
        """新しい知識の追加"""
        try:
            if knowledge_id is None:
                knowledge_id = f"knowledge_{len(self.knowledge_base)}"
            
            # 簡易的なキーワード抽出（実際の実装ではより高度な処理が必要）
            keywords = [word for word in text.split() if len(word) > 2]
            
            new_knowledge = {
                "id": knowledge_id,
                "text": text,
                "category": category,
                "keywords": keywords[:5]  # 上位5個のキーワード
            }
            
            self.knowledge_base.append(new_knowledge)
            logger.info(f"新しい知識を追加しました: {knowledge_id}")
            return True
            
        except Exception as e:
            logger.error(f"知識追加エラー: {str(e)}")
            return False