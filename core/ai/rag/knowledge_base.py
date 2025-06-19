"""陸上競技中長距離・マラソン特化知識ベース管理"""

import logging
import re
from typing import List, Dict, Tuple
from collections import Counter

logger = logging.getLogger(__name__)


class KnowledgeBase:
    """陸上競技中長距離・マラソン特化知識ベース管理"""
    
    def __init__(self):
        """初期化"""
        # 陸上競技中長距離・マラソン特化の包括的知識ベース
        self.knowledge_base = [
            # === 競技特性・生理学 ===
            {
                "id": "distance_physiology",
                "text": "陸上競技の距離別エネルギー供給比率：800m（60%無酸素）、1500m（50%無酸素）、3000m（30%無酸素）、5000m（20%無酸素）、10000m（10%無酸素）、マラソン（ほぼ100%有酸素）。最大酸素摂取量（VO2max）と乳酸閾値（LT）が重要で、距離が長くなるほど有酸素能力の比重が高まります。",
                "category": "生理学",
                "keywords": ["エネルギー供給", "有酸素", "無酸素", "VO2max", "乳酸閾値", "LT", "800m", "1500m", "3000m", "5000m", "10000m", "マラソン"],
                "priority": 5,
                "levels": ["初心者", "中級者", "上級者", "エリート"],
                "ages": ["ジュニア", "シニア", "マスターズ"]
            },
            {
                "id": "lactate_threshold_training",
                "text": "乳酸閾値（LT）トレーニングは中長距離競技の最重要練習です。LTペースは約1時間持続可能なペースで、1500m選手なら5-10kmペース、5000m選手なら10-15kmペース、マラソン選手ならハーフマラソンペースが目安。週1-2回、20-60分のLT走を実施し、心拍数で言えば最大心拍数の85-90%程度を維持します。",
                "category": "練習方法",
                "keywords": ["乳酸閾値", "LT", "LT走", "閾値走", "テンポ走", "心拍数", "最大心拍数", "ペース", "ハーフマラソン"],
                "priority": 5,
                "levels": ["中級者", "上級者", "エリート"],
                "ages": ["シニア", "マスターズ"]
            },
            
            # === 練習方法 ===
            {
                "id": "interval_training_comprehensive",
                "text": "距離別インターバル走設計：800m選手（200-400m×8-12本、休息1-2分）、1500m選手（400-800m×6-10本、休息2-3分）、3000m選手（800-1200m×4-8本、休息3-4分）、5000m選手（1000-1600m×3-6本、休息4-5分）、10000m選手（1000-2000m×3-5本、休息5-7分）、マラソン選手（2000-5000m×2-4本、休息7-10分）。強度は競技ペースの95-105%で、総距離は競技距離の2-3倍を目安とします。",
                "category": "練習方法",
                "keywords": ["インターバル", "インターバル走", "800m", "1500m", "3000m", "5000m", "10000m", "マラソン", "休息", "強度", "ペース", "総距離"],
                "priority": 5,
                "levels": ["中級者", "上級者", "エリート"],
                "ages": ["ジュニア", "シニア", "マスターズ"]
            },
            {
                "id": "long_distance_running_comprehensive",
                "text": "距離別長距離走の目安：800m選手（5-8km）、1500m選手（8-12km）、3000m選手（10-15km）、5000m選手（12-20km）、10000m選手（15-25km）、マラソン選手（20-35km）。ペースは会話可能なペース（最大心拍数の70-80%）で、有酸素能力の基盤を築きます。週1-3回の実施が適切です。",
                "category": "練習方法",
                "keywords": ["長距離走", "ジョギング", "有酸素", "会話可能", "心拍数", "基盤", "800m", "1500m", "3000m", "5000m", "10000m", "マラソン"],
                "priority": 4,
                "levels": ["初心者", "中級者", "上級者", "エリート"],
                "ages": ["ジュニア", "シニア", "マスターズ"]
            },
            {
                "id": "marathon_specific_training",
                "text": "マラソン特化練習：週1回の長距離走（20-35km）、週1回のマラソンペース走（10-20km）、週1回のLT走（15-25km）、週2-3回のジョギング（8-15km）。練習量は週60-120kmが目安で、本番2-3週間前からテーパリング（練習量削減）を開始します。",
                "category": "練習方法",
                "keywords": ["マラソン", "長距離走", "マラソンペース", "LT走", "ジョギング", "練習量", "テーパリング"],
                "priority": 5,
                "levels": ["中級者", "上級者", "エリート"],
                "ages": ["シニア", "マスターズ"]
            },
            
            # === レベル別指導 ===
            {
                "id": "beginner_guidance",
                "text": "初心者向け指導：週3-4回の練習から開始し、無理のないペースで走ります。最初は10-20分のジョギングから始め、徐々に時間と距離を延ばします。目標設定は具体的で達成可能なものにし、怪我予防のため十分な休息を取ります。",
                "category": "レベル別指導",
                "keywords": ["初心者", "ジョギング", "ペース", "目標設定", "怪我予防", "休息"],
                "priority": 4,
                "levels": ["初心者"],
                "ages": ["ジュニア", "シニア", "マスターズ"]
            },
            {
                "id": "intermediate_guidance",
                "text": "中級者向け指導：週4-5回の練習で、インターバル走やLT走を取り入れます。競技会への参加を目標に、定期的なタイムトライアルで実力を把握します。練習の質と量のバランスを取り、オーバートレーニングに注意します。",
                "category": "レベル別指導",
                "keywords": ["中級者", "インターバル", "LT走", "競技会", "タイムトライアル", "オーバートレーニング"],
                "priority": 4,
                "levels": ["中級者"],
                "ages": ["ジュニア", "シニア", "マスターズ"]
            },
            {
                "id": "advanced_guidance",
                "text": "上級者向け指導：週5-6回の練習で、高度な練習メニューを実施します。年間計画に基づいたシーズン管理を行い、ピーキングを意識した練習設計をします。メンタルトレーニングも重要で、レースでの戦術的思考を養います。",
                "category": "レベル別指導",
                "keywords": ["上級者", "高度", "シーズン管理", "ピーキング", "メンタル", "戦術"],
                "priority": 4,
                "levels": ["上級者"],
                "ages": ["シニア", "マスターズ"]
            },
            {
                "id": "elite_guidance",
                "text": "エリート選手向け指導：週6-7回の練習で、科学的根拠に基づいた高度なトレーニングを実施します。個別の生理学的データに基づいた練習設計、栄養管理、コンディショニングが重要です。国際大会での活躍を目指した総合的な能力向上を図ります。",
                "category": "レベル別指導",
                "keywords": ["エリート", "科学的", "生理学的", "栄養管理", "コンディショニング", "国際大会"],
                "priority": 4,
                "levels": ["エリート"],
                "ages": ["シニア"]
            },
            
            # === 年齢別指導 ===
            {
                "id": "junior_guidance",
                "text": "ジュニア選手（中学生・高校生）向け指導：成長期を考慮した練習設計が重要です。週4-5回の練習で、基礎体力と技術の習得に重点を置きます。急激な練習量増加は避け、楽しみながら競技に取り組む姿勢を大切にします。",
                "category": "年齢別指導",
                "keywords": ["ジュニア", "中学生", "高校生", "成長期", "基礎体力", "技術", "楽しみ"],
                "priority": 4,
                "levels": ["初心者", "中級者", "上級者"],
                "ages": ["ジュニア"]
            },
            {
                "id": "senior_guidance",
                "text": "シニア選手（大学生・社会人）向け指導：競技力向上と自己管理能力の両立が重要です。週5-6回の練習で、競技特化の練習メニューを実施します。仕事や学業との両立を考慮した効率的な練習設計を行います。",
                "category": "年齢別指導",
                "keywords": ["シニア", "大学生", "社会人", "自己管理", "競技特化", "両立", "効率的"],
                "priority": 4,
                "levels": ["中級者", "上級者", "エリート"],
                "ages": ["シニア"]
            },
            {
                "id": "masters_guidance",
                "text": "マスターズ選手（40歳以上）向け指導：加齢に伴う身体変化を考慮した練習設計が重要です。週3-5回の練習で、怪我予防と継続性を重視します。筋力トレーニングと柔軟性向上も重要で、無理のないペースで長期的な競技継続を目指します。",
                "category": "年齢別指導",
                "keywords": ["マスターズ", "40歳以上", "加齢", "怪我予防", "継続性", "筋力", "柔軟性"],
                "priority": 4,
                "levels": ["初心者", "中級者", "上級者"],
                "ages": ["マスターズ"]
            },
            
            # === 戦術・レース展開 ===
            {
                "id": "race_strategy_comprehensive",
                "text": "距離別戦術：800m（前取り・後方待機・中盤戦術）、1500m（ペース配分・ポジション取り）、3000m以上（ペースコントロール・給水戦略）、マラソン（前半抑え・後半スパート・給水・栄養補給）。距離が長くなるほど戦術的要素が複雑になります。",
                "category": "戦術",
                "keywords": ["戦術", "800m", "1500m", "3000m", "マラソン", "ペース配分", "ポジション", "給水", "栄養補給"],
                "priority": 4,
                "levels": ["中級者", "上級者", "エリート"],
                "ages": ["ジュニア", "シニア", "マスターズ"]
            },
            {
                "id": "marathon_strategy",
                "text": "マラソン戦術：前半は目標ペースの95%程度で走り、30km地点でペースアップを図ります。給水は5kmごとに100-200ml、栄養補給は15-20kmごとにジェルやバナナを摂取。天候や体調に応じて戦術を調整します。",
                "category": "戦術",
                "keywords": ["マラソン", "戦術", "ペース", "給水", "栄養補給", "ジェル", "天候", "体調"],
                "priority": 5,
                "levels": ["中級者", "上級者", "エリート"],
                "ages": ["シニア", "マスターズ"]
            },
            
            # === 栄養・水分補給 ===
            {
                "id": "nutrition_comprehensive",
                "text": "距離別栄養管理：中距離（炭水化物60-65%、タンパク質15-20%、脂質20-25%）、長距離・マラソン（炭水化物65-70%、タンパク質15%、脂質15-20%）。練習前2-3時間に炭水化物中心の食事、練習後30分以内に炭水化物とタンパク質を3:1の比率で摂取します。",
                "category": "栄養",
                "keywords": ["栄養", "炭水化物", "タンパク質", "脂質", "中距離", "長距離", "マラソン", "食事"],
                "priority": 4,
                "levels": ["中級者", "上級者", "エリート"],
                "ages": ["ジュニア", "シニア", "マスターズ"]
            },
            {
                "id": "marathon_nutrition",
                "text": "マラソン栄養戦略：レース前3日間は炭水化物ローディング（体重1kgあたり8-10g）、前日は軽めの食事、当日はスタート3時間前に炭水化物中心の朝食。レース中は15-20kmごとにジェル（30-60g炭水化物）を摂取し、給水と合わせて脱水を防ぎます。",
                "category": "栄養",
                "keywords": ["マラソン", "栄養", "炭水化物ローディング", "ジェル", "給水", "脱水"],
                "priority": 5,
                "levels": ["中級者", "上級者", "エリート"],
                "ages": ["シニア", "マスターズ"]
            },
            
            # === 怪我予防・コンディショニング ===
            {
                "id": "injury_prevention_comprehensive",
                "text": "レベル・年齢別怪我予防：初心者（急激な練習量増加を避ける）、中級者（高強度練習の間隔を空ける）、上級者（個別の弱点を補強）、マスターズ（筋力トレーニングと柔軟性向上）。週の練習量増加は10%以内に抑え、痛みを感じたら即座に練習を中止します。",
                "category": "怪我予防",
                "keywords": ["怪我予防", "初心者", "中級者", "上級者", "マスターズ", "練習量", "筋力", "柔軟性", "痛み"],
                "priority": 4,
                "levels": ["初心者", "中級者", "上級者", "エリート"],
                "ages": ["ジュニア", "シニア", "マスターズ"]
            },
            {
                "id": "recovery_methods_comprehensive",
                "text": "包括的回復方法：練習後は必ずクールダウン（10-20分の軽いジョギング）を行い、アイシング（15-20分）で炎症を抑制。マッサージ、ストレッチ、入浴（38-40℃、15-20分）で血流を促進。十分な睡眠（7-9時間）と栄養補給で疲労回復を図ります。",
                "category": "怪我予防",
                "keywords": ["回復", "クールダウン", "アイシング", "マッサージ", "入浴", "睡眠", "疲労回復"],
                "priority": 3,
                "levels": ["中級者", "上級者", "エリート"],
                "ages": ["ジュニア", "シニア", "マスターズ"]
            },
            
            # === メンタル・心理面 ===
            {
                "id": "mental_training_comprehensive",
                "text": "レベル別メンタルトレーニング：初心者（楽しみながら競技に取り組む）、中級者（目標設定と達成感）、上級者（レースでの戦術的思考）、エリート（国際大会での心理的プレッシャー管理）。イメージトレーニング、自己暗示法、呼吸法でメンタル面を強化します。",
                "category": "メンタル",
                "keywords": ["メンタル", "初心者", "中級者", "上級者", "エリート", "目標設定", "戦術的思考", "プレッシャー"],
                "priority": 3,
                "levels": ["初心者", "中級者", "上級者", "エリート"],
                "ages": ["ジュニア", "シニア", "マスターズ"]
            },
            
            # === 練習計画・シーズン管理 ===
            {
                "id": "season_planning_comprehensive",
                "text": "包括的シーズン管理：オフシーズン（10-12月：基礎体力・筋力向上）、プレシーズン（1-3月：有酸素能力・LT向上）、シーズン前半（4-6月：スピード・インターバル強化）、シーズン後半（7-9月：レース調整・ピーキング）。マラソン選手は年間2-3回のレースを目標に調整します。",
                "category": "練習計画",
                "keywords": ["シーズン", "オフシーズン", "プレシーズン", "シーズン前半", "シーズン後半", "ピーキング", "マラソン"],
                "priority": 4,
                "levels": ["中級者", "上級者", "エリート"],
                "ages": ["シニア", "マスターズ"]
            },
            {
                "id": "weekly_planning_comprehensive",
                "text": "レベル別週間計画：初心者（週3-4回、ジョギング中心）、中級者（週4-5回、インターバル・LT走導入）、上級者（週5-6回、高度な練習メニュー）、エリート（週6-7回、個別調整）。高強度練習の間は必ず軽い練習や休養を入れ、オーバートレーニングを防ぎます。",
                "category": "練習計画",
                "keywords": ["週間計画", "初心者", "中級者", "上級者", "エリート", "インターバル", "LT走", "オーバートレーニング"],
                "priority": 4,
                "levels": ["初心者", "中級者", "上級者", "エリート"],
                "ages": ["ジュニア", "シニア", "マスターズ"]
            },
            
            # === 技術・フォーム ===
            {
                "id": "running_form_comprehensive",
                "text": "距離別ランニングフォーム：中距離（効率的なエネルギー使用、中足部着地）、長距離（省エネ走法、軽やかな着地）、マラソン（長時間持続可能なフォーム、上下動を抑える）。上半身はリラックスし、腕振りは自然な前後運動。歩数は1分間に180-190回が理想的です。",
                "category": "技術",
                "keywords": ["ランニングフォーム", "中距離", "長距離", "マラソン", "着地", "省エネ", "歩数"],
                "priority": 3,
                "levels": ["中級者", "上級者", "エリート"],
                "ages": ["ジュニア", "シニア", "マスターズ"]
            }
        ]
        
        logger.info(f"陸上競技中長距離・マラソン特化知識ベースを初期化しました（{len(self.knowledge_base)}件）")
    
    def search_relevant_knowledge(self, query: str, n_results: int = 3, user_level: str = None, user_age: str = None) -> str:
        """関連知識の検索（レベル・年齢対応版）"""
        try:
            # クエリの前処理
            query_processed = self._preprocess_query(query)
            
            # 知識ベースから関連度を計算
            relevant_knowledge = []
            
            for knowledge in self.knowledge_base:
                score = self._calculate_relevance_score(query_processed, knowledge)
                
                # レベル・年齢フィルタリング
                if user_level and "levels" in knowledge:
                    if user_level not in knowledge["levels"]:
                        score *= 0.5  # レベルが合わない場合はスコアを下げる
                
                if user_age and "ages" in knowledge:
                    if user_age not in knowledge["ages"]:
                        score *= 0.5  # 年齢が合わない場合はスコアを下げる
                
                if score > 0:
                    relevant_knowledge.append((score, knowledge))
            
            # スコア順にソート（優先度も考慮）
            relevant_knowledge.sort(key=lambda x: (x[0], x[1]["priority"]), reverse=True)
            
            # 上位n_results件を取得
            top_knowledge = relevant_knowledge[:n_results]
            
            if top_knowledge:
                knowledge_text = self._format_knowledge_output(top_knowledge)
                logger.info(f"関連知識 {len(top_knowledge)} 件を取得しました（最高スコア: {top_knowledge[0][0]}）")
                return knowledge_text
            else:
                logger.warning("関連知識が見つかりませんでした")
                return "陸上競技中長距離・マラソンの基本的な練習指導の原則に従って回答してください。"
                
        except Exception as e:
            logger.error(f"知識検索エラー: {str(e)}")
            return "陸上競技中長距離・マラソンの基本的な練習指導の原則に従って回答してください。"
    
    def _preprocess_query(self, query: str) -> str:
        """クエリの前処理"""
        # 小文字化
        query = query.lower()
        
        # 陸上競技関連の同義語を正規化
        synonyms = {
            "800m": ["800", "八百", "八百メートル"],
            "1500m": ["1500", "千五", "千五百", "千五百メートル"],
            "3000m": ["3000", "三千", "三千メートル"],
            "5000m": ["5000", "五千", "五千メートル"],
            "10000m": ["10000", "一万", "一万メートル"],
            "マラソン": ["42.195km", "42.195キロ", "フルマラソン"],
            "ハーフマラソン": ["21.0975km", "21.0975キロ", "ハーフ"],
            "インターバル": ["インターバル走", "間欠走"],
            "レペティション": ["レペティション走", "反復走"],
            "乳酸閾値": ["LT", "閾値", "テンポ走"],
            "最大酸素摂取量": ["VO2max", "最大酸素摂取量"],
            "初心者": ["ビギナー", "初級者"],
            "中級者": ["中級"],
            "上級者": ["上級", "アドバンス"],
            "エリート": ["トップ", "プロ"],
            "ジュニア": ["中学生", "高校生", "若年"],
            "シニア": ["大学生", "社会人", "成人"],
            "マスターズ": ["40歳以上", "シニア", "ベテラン"]
        }
        
        for standard, variants in synonyms.items():
            for variant in variants:
                query = query.replace(variant, standard)
        
        return query
    
    def _calculate_relevance_score(self, query: str, knowledge: Dict) -> float:
        """関連度スコアの計算"""
        score = 0.0
        
        # キーワードマッチング（重み: 1.0）
        for keyword in knowledge["keywords"]:
            if keyword.lower() in query:
                score += 1.0
        
        # カテゴリマッチング（重み: 2.0）
        if knowledge["category"].lower() in query:
            score += 2.0
        
        # テキスト内容マッチング（重み: 0.5）
        text_words = set(re.findall(r'\w+', knowledge["text"].lower()))
        query_words = set(re.findall(r'\w+', query))
        common_words = text_words.intersection(query_words)
        score += len(common_words) * 0.5
        
        # 優先度による補正
        score *= (1 + knowledge["priority"] * 0.1)
        
        return score
    
    def _format_knowledge_output(self, knowledge_list: List[Tuple[float, Dict]]) -> str:
        """知識出力のフォーマット"""
        formatted_parts = []
        
        for score, knowledge in knowledge_list:
            category = knowledge["category"]
            text = knowledge["text"]
            
            # レベル・年齢情報を追加
            level_info = ""
            if "levels" in knowledge:
                level_info += f"対象レベル: {', '.join(knowledge['levels'])} "
            if "ages" in knowledge:
                level_info += f"対象年齢: {', '.join(knowledge['ages'])}"
            
            if level_info:
                formatted_parts.append(f"【{category}】{level_info}\n{text}")
            else:
                formatted_parts.append(f"【{category}】\n{text}")
        
        return "\n\n".join(formatted_parts)
    
    def add_knowledge(self, text: str, category: str, keywords: List[str] = None, priority: int = 3, levels: List[str] = None, ages: List[str] = None, knowledge_id: str = None) -> bool:
        """新しい知識の追加（レベル・年齢対応版）"""
        try:
            if knowledge_id is None:
                knowledge_id = f"knowledge_{len(self.knowledge_base)}"
            
            # キーワードが指定されていない場合は自動抽出
            if keywords is None:
                keywords = self._extract_keywords(text)
            
            new_knowledge = {
                "id": knowledge_id,
                "text": text,
                "category": category,
                "keywords": keywords,
                "priority": priority
            }
            
            if levels:
                new_knowledge["levels"] = levels
            if ages:
                new_knowledge["ages"] = ages
            
            self.knowledge_base.append(new_knowledge)
            logger.info(f"新しい知識を追加しました: {knowledge_id}（カテゴリ: {category}）")
            return True
            
        except Exception as e:
            logger.error(f"知識追加エラー: {str(e)}")
            return False
    
    def _extract_keywords(self, text: str) -> List[str]:
        """テキストからキーワードを自動抽出"""
        # 陸上競技関連の重要キーワード
        important_keywords = [
            "800m", "1500m", "3000m", "5000m", "10000m", "マラソン", "ハーフマラソン",
            "中距離", "長距離", "インターバル", "レペティション", "乳酸閾値", "LT",
            "最大酸素摂取量", "VO2max", "ペース", "戦術", "栄養", "水分補給",
            "怪我予防", "回復", "メンタル", "練習計画", "フォーム", "初心者",
            "中級者", "上級者", "エリート", "ジュニア", "シニア", "マスターズ"
        ]
        
        # テキストから重要キーワードを抽出
        extracted = []
        text_lower = text.lower()
        
        for keyword in important_keywords:
            if keyword.lower() in text_lower:
                extracted.append(keyword)
        
        # 一般的な単語も抽出（3文字以上）
        words = re.findall(r'\w{3,}', text_lower)
        word_freq = Counter(words)
        
        # 頻度の高い単語を追加（最大3個）
        for word, freq in word_freq.most_common(3):
            if word not in extracted and len(extracted) < 8:
                extracted.append(word)
        
        return extracted[:8]  # 最大8個のキーワード
    
    def get_knowledge_by_category(self, category: str) -> List[Dict]:
        """カテゴリ別の知識取得"""
        return [k for k in self.knowledge_base if k["category"] == category]
    
    def get_knowledge_by_level(self, level: str) -> List[Dict]:
        """レベル別の知識取得"""
        return [k for k in self.knowledge_base if "levels" in k and level in k["levels"]]
    
    def get_knowledge_by_age(self, age: str) -> List[Dict]:
        """年齢別の知識取得"""
        return [k for k in self.knowledge_base if "ages" in k and age in k["ages"]]
    
    def get_knowledge_stats(self) -> Dict:
        """知識ベースの統計情報"""
        categories = Counter([k["category"] for k in self.knowledge_base])
        levels = Counter()
        ages = Counter()
        
        for k in self.knowledge_base:
            if "levels" in k:
                for level in k["levels"]:
                    levels[level] += 1
          