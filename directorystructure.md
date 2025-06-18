# LINE練習相談アプリケーション ディレクトリ構造

## 🔷 プロジェクト構造概要

**スケーラブル**で**保守性の高い**ディレクトリ構造。機能別・レイヤー別の明確な分離により、開発効率と品質を両立。

```
line-running-consultation/
├── README.md                           # プロジェクト概要
├── pyproject.toml                      # Poetry設定、依存関係
├── poetry.lock                         # 依存関係ロック
├── .env.example                        # 環境変数テンプレート
├── .env                               # 環境変数 (gitignore)
├── .gitignore                         # Git除外設定
├── .pre-commit-config.yaml            # Pre-commit設定
├── docker-compose.yml                 # ローカル開発環境
├── Dockerfile                         # コンテナ設定
├── requirements.txt                   # 本番用依存関係
│
├── app/                               # アプリケーションコア
│   ├── __init__.py
│   ├── main.py                        # FastAPI アプリケーション起動
│   ├── config.py                      # 設定管理
│   ├── dependencies.py                # 依存関係注入
│   └── middleware.py                  # ミドルウェア設定
│
├── api/                               # API エンドポイント
│   ├── __init__.py
│   ├── routes/                        # APIルート
│   │   ├── __init__.py
│   │   ├── webhook.py                 # LINE Webhook
│   │   ├── health.py                  # ヘルスチェック
│   │   ├── admin.py                   # 管理者API
│   │   └── analytics.py               # 分析API
│   ├── schemas/                       # Pydantic スキーマ
│   │   ├── __init__.py
│   │   ├── line_events.py             # LINE イベント
│   │   ├── training_log.py            # 練習記録
│   │   ├── user.py                    # ユーザー
│   │   └── ai_response.py             # AI応答
│   └── exceptions.py                  # カスタム例外
│
├── core/                              # ビジネスロジック
│   ├── __init__.py
│   ├── services/                      # サービス層
│   │   ├── __init__.py
│   │   ├── line_service.py            # LINE Bot サービス
│   │   ├── ai_service.py              # AI 応答サービス
│   │   ├── training_service.py        # 練習管理サービス
│   │   ├── user_service.py            # ユーザー管理サービス
│   │   └── analytics_service.py       # 分析サービス
│   ├── ai/                           # AI・機械学習
│   │   ├── __init__.py
│   │   ├── llm/                      # LLM関連
│   │   │   ├── __init__.py
│   │   │   ├── gemini_client.py      # Gemini API クライアント
│   │   │   ├── prompt_manager.py     # プロンプト管理
│   │   │   └── response_formatter.py # 応答フォーマット
│   │   ├── rag/                      # RAG実装
│   │   │   ├── __init__.py
│   │   │   ├── knowledge_base.py     # 知識ベース管理
│   │   │   ├── vector_store.py       # ベクトルストア
│   │   │   ├── retriever.py          # 情報検索
│   │   │   └── generator.py          # 応答生成
│   │   ├── personalization/          # パーソナライズ
│   │   │   ├── __init__.py
│   │   │   ├── user_profiler.py      # ユーザープロファイル
│   │   │   ├── level_detector.py     # レベル判定
│   │   │   └── content_adapter.py    # コンテンツ適応
│   │   └── models/                   # AI モデル定義
│   │       ├── __init__.py
│   │       └── training_models.py    # 練習分析モデル
│   └── domain/                       # ドメインロジック
│       ├── __init__.py
│       ├── entities/                 # エンティティ
│       │   ├── __init__.py
│       │   ├── user.py               # ユーザーエンティティ
│       │   ├── training_log.py       # 練習記録エンティティ
│       │   └── ai_conversation.py    # AI会話エンティティ
│       ├── repositories/             # リポジトリインターフェース
│       │   ├── __init__.py
│       │   ├── user_repository.py    # ユーザーリポジトリ
│       │   ├── training_repository.py # 練習記録リポジトリ
│       │   └── conversation_repository.py # 会話リポジトリ
│       └── use_cases/               # ユースケース
│           ├── __init__.py
│           ├── process_training_log.py # 練習記録処理
│           ├── generate_feedback.py    # フィードバック生成
│           └── manage_user_profile.py  # ユーザープロファイル管理
│
├── infrastructure/                    # インフラストラクチャ層
│   ├── __init__.py
│   ├── database/                     # データベース
│   │   ├── __init__.py
│   │   ├── models/                   # SQLAlchemy モデル
│   │   │   ├── __init__.py
│   │   │   ├── user.py               # ユーザーモデル
│   │   │   ├── training_log.py       # 練習記録モデル
│   │   │   ├── ai_conversation.py    # AI会話モデル
│   │   │   └── user_profile.py       # ユーザープロファイルモデル
│   │   ├── repositories/             # リポジトリ実装
│   │   │   ├── __init__.py
│   │   │   ├── user_repository_impl.py
│   │   │   ├── training_repository_impl.py
│   │   │   └── conversation_repository_impl.py
│   │   ├── migrations/               # Alembic マイグレーション
│   │   │   └── versions/
│   │   ├── connection.py             # DB接続管理
│   │   └── session.py                # セッション管理
│   ├── external/                     # 外部サービス連携
│   │   ├── __init__.py
│   │   ├── line/                     # LINE API
│   │   │   ├── __init__.py
│   │   │   ├── webhook_handler.py    # Webhook処理
│   │   │   ├── message_sender.py     # メッセージ送信
│   │   │   └── rich_menu.py          # リッチメニュー
│   │   ├── google/                   # Google API
│   │   │   ├── __init__.py
│   │   │   └── gemini_api.py         # Gemini API クライアント
│   │   └── dify/                     # Dify連携
│   │       ├── __init__.py
│   │       └── dify_client.py        # Dify API クライアント
│   └── cache/                        # キャッシュ
│       ├── __init__.py
│       ├── redis_client.py           # Redis クライアント
│       └── cache_manager.py          # キャッシュ管理
│
├── shared/                           # 共通モジュール
│   ├── __init__.py
│   ├── utils/                        # ユーティリティ
│   │   ├── __init__.py
│   │   ├── logger.py                 # ログ設定
│   │   ├── datetime_utils.py         # 日時ユーティリティ
│   │   ├── validation.py             # バリデーション
│   │   └── text_processor.py         # テキスト処理
│   ├── constants/                    # 定数
│   │   ├── __init__.py
│   │   ├── training_types.py         # 練習種別
│   │   ├── user_levels.py            # ユーザーレベル
│   │   └── response_templates.py     # 応答テンプレート
│   └── exceptions/                   # 共通例外
│       ├── __init__.py
│       ├── base.py                   # 基底例外
│       ├── ai_exceptions.py          # AI関連例外
│       └── data_exceptions.py        # データ関連例外
│
├── data/                             # データファイル
│   ├── knowledge_base/               # 知識ベース
│   │   ├── training_science/         # 練習科学
│   │   │   ├── endurance_training.md
│   │   │   ├── interval_training.md
│   │   │   └── recovery_methods.md
│   │   ├── sports_medicine/          # スポーツ医学
│   │   │   ├── injury_prevention.md
│   │   │   └── nutrition_guide.md
│   │   └── coaching_tips/            # コーチングアドバイス
│   │       ├── beginner_guidance.md
│   │       └── advanced_techniques.md
│   ├── prompts/                      # プロンプトテンプレート
│   │   ├── feedback_generation.txt
│   │   ├── level_assessment.txt
│   │   └── motivation_messages.txt
│   └── sample_data/                  # サンプルデータ
│       ├── users.json
│       └── training_logs.json
│
├── tests/                            # テストコード
│   ├── __init__.py
│   ├── conftest.py                   # pytest設定
│   ├── unit/                         # ユニットテスト
│   │   ├── __init__.py
│   │   ├── core/
│   │   │   ├── services/
│   │   │   └── ai/
│   │   ├── api/
│   │   │   └── routes/
│   │   └── shared/
│   │       └── utils/
│   ├── integration/                  # 統合テスト
│   │   ├── __init__.py
│   │   ├── api/
│   │   ├── database/
│   │   └── external/
│   ├── e2e/                         # E2Eテスト
│   │   ├── __init__.py
│   │   └── scenarios/
│   └── fixtures/                     # テストフィクスチャ
│       ├── __init__.py
│       └── test_data.py
│
├── scripts/                          # スクリプト
│   ├── setup_db.py                   # DB初期化
│   ├── seed_data.py                  # サンプルデータ投入
│   ├── backup_data.py                # データバックアップ
│   └── deploy.py                     # デプロイスクリプト
│
├── docs/                             # ドキュメント
│   ├── api/                          # API仕様書
│   │   └── openapi.yaml
│   ├── architecture/                 # アーキテクチャ
│   │   ├── system_design.md
│   │   └── database_schema.md
│   ├── deployment/                   # デプロイメント
│   │   ├── docker.md
│   │   └── gcp_deployment.md
│   └── user_guide/                   # ユーザーガイド
│       └── line_bot_usage.md
│
├── monitoring/                       # 監視・ログ
│   ├── prometheus/
│   │   └── prometheus.yml
│   ├── grafana/
│   │   └── dashboards/
│   └── logs/                         # ログファイル格納
│
└── deployment/                       # デプロイメント設定
    ├── kubernetes/                   # K8s設定
    │   ├── namespace.yaml
    │   ├── deployment.yaml
    │   ├── service.yaml
    │   └── ingress.yaml
    ├── gcp/                         # GCP設定
    │   ├── cloudbuild.yaml
    │   └── app.yaml
    └── aws/                         # AWS設定
        ├── lambda/
        └── cloudformation/
```

## 🔷 主要ディレクトリの説明

### `/app/` - アプリケーションコア
- **役割**: FastAPIアプリケーションの起動・設定
- **重要ファイル**: `main.py` (エントリーポイント)、`config.py` (設定管理)

### `/api/` - APIレイヤー
- **役割**: REST API エンドポイント、リクエスト/レスポンス処理
- **重要ファイル**: `webhook.py` (LINE Webhook)、各種スキーマ定義

### `/core/` - ビジネスロジック
- **役割**: アプリケーションの核となるビジネスロジック
- **サブディレクトリ**:
  - `services/`: サービス層（ビジネスロジック）
  - `ai/`: AI・機械学習機能
  - `domain/`: ドメイン駆動設計（エンティティ、リポジトリ、ユースケース）

### `/infrastructure/` - インフラストラクチャ
- **役割**: 外部システム連携、データベース、キャッシュ
- **重要な分離**: ビジネスロジックから技術的詳細を分離

### `/shared/` - 共通モジュール
- **役割**: プロジェクト全体で使用する共通機能
- **内容**: ユーティリティ、定数、例外処理

### `/data/` - データファイル
- **役割**: 知識ベース、プロンプト、サンプルデータ
- **重要**: RAG用の知識ベースを体系的に管理

### `/tests/` - テストコード
- **構造**: ユニット → 統合 → E2E の階層構造
- **方針**: 各レイヤーに対応したテスト構造

## 🔷 設計原則

### 1. **レイヤー分離**
- API層、ビジネスロジック層、インフラ層の明確な分離
- 依存関係の方向性を明確化（上位層 → 下位層）

### 2. **ドメイン駆動設計**
- エンティティ、リポジトリ、ユースケースによる構造化
- ビジネスロジックの中心化

### 3. **マイクロサービス準備**
- 機能別の明確な分離により、将来的な分割を容易に

### 4. **テスタビリティ**
- 各層が独立してテスト可能な構造
- モックしやすい依存関係注入

### 5. **スケーラビリティ**
- 機能追加時の影響範囲を最小化
- 新しい AI モデルや外部サービスの追加が容易

## 🔷 命名規則

### ファイル・ディレクトリ
- **Snake case**: `user_service.py`、`training_log.py`
- **複数形**: `models/`、`services/`、`tests/`
- **明確な命名**: 機能が推測できる名前

### クラス・関数
- **PascalCase**: クラス名 (`UserService`)
- **Snake case**: 関数名 (`get_user_profile`)
- **動詞+名詞**: 関数名 (`create_training_log`)

## 🔷 重要な注意事項

⚠️ **構造変更禁止**: このディレクトリ構造は設計思想に基づいています。変更前に必ず承認を得てください。

⚠️ **レイヤー境界**: 各レイヤー間の依存関係を守り、循環参照を避けてください。

⚠️ **データ管理**: `/data/` ディレクトリの知識ベースは RAG の品質に直結します。体系的な管理を心がけてください。

⚠️ **テスト構造**: 実装と同じ構造でテストを作成し、保守性を確保してください。 