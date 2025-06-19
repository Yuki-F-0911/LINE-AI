# LINE練習相談アプリケーション 技術スタック詳細

## 🔷 技術選定方針

**高度なパーソナライズ機能**と**スケーラブルなLINE Bot**を核とした、陸上競技練習相談アプリケーションの技術スタック。AI技術を活用しつつ、ユーザー体験を最優先に設計。

---

## 🔷 バックエンド技術

### プログラミング言語・フレームワーク
- **Python 3.11**（メイン言語）
- **FastAPI 0.104+**（APIサーバー、CORS対応、OpenAPI自動生成）
- **Pydantic 2.5+ / pydantic-settings**（設定管理・型安全性、app/config.py）
- **SQLAlchemy 2.0+**（ORM、DB接続/infrastructure/database/connection.py, models/）
- **asyncpg 0.29+**（PostgreSQL非同期ドライバ、DB接続）
- **alembic**（DBマイグレーション、※現状マイグレーションファイル未作成）

### API・ルーティング
- **FastAPI Router**（api/routes/health.py, webhook.py）

---

## 🔷 AI・機械学習技術

### LLM・AIサービス
- **Google Gemini Pro API**（AI応答生成、core/services/ai_service.py）
  - **google-generativeai 0.3+**（Gemini API Python SDK）

### RAG（Retrieval Augmented Generation）
- **自作簡易RAG**（core/ai/rag/knowledge_base.py）
  - ※LangChain, ChromaDB, sentence-transformers等は現状未使用・import実績なし

---

## 🔷 データベース・キャッシュ

- **PostgreSQL 15+**（ユーザー・練習記録/infrastructure/database/models/）
- **asyncpg**（DB接続）
- **Redis 7+**（キャッシュ/セッション、app/config.pyで設定のみ、実装は未着手）

---

## 🔷 LINEプラットフォーム

- **LINE Messaging API**（Bot機能、api/routes/webhook.py, core/services/line_service.py）
  - **line-bot-sdk 3.8+**（Python SDK）

---

## 🔷 インフラ・クラウド

- **Google Cloud Platform**（Gemini API利用、将来の本番運用想定）
- **Cloud Run, Cloud SQL**（将来の本番運用候補、現状はローカル開発中心）
- **Docker**（開発・本番環境のコンテナ化想定、Dockerfile/composeは未同梱）

---

## 🔷 開発・運用ツール

- **Poetry 1.7+**（依存管理/pyproject.toml）
- **pytest 7+ / pytest-asyncio**（テスト/tests/）
- **pre-commit**（コード品質チェック、.pre-commit-config.yaml）
- **Black**（コードフォーマット）
- **Ruff**（静的解析）
- **mypy**（型チェック）
- **httpx**（テスト用HTTPクライアント、tests/test_health.py等）
- **coverage**（テストカバレッジ計測）
- **python-dotenv**（環境変数管理、tests/test_ai_service.py等）

---

## 🔷 セキュリティ・認証

- **python-jose 3.3+**（JWT処理、現状import実績なし/将来拡張用）
- **bcrypt 4.1+**（パスワードハッシュ化、現状import実績なし/将来拡張用）
- **python-multipart**（ファイルアップロード、現状import実績なし/将来拡張用）

---

## 🔷 データ処理・分析

- **pandas 2.1+ / numpy 1.26+**（現状import実績なし/将来拡張用）

---

## 🔷 バージョン管理・CI/CD

- **Git / GitHub**（バージョン管理・プロジェクト管理）
- **GitHub Actions**（CI/CD、将来拡張用）

---

## 🔷 注意事項

- 本ファイルは実装で実際に使われている技術を中心に記載しています。
- pyproject.tomlに記載があるが現状import実績がないものは「将来拡張用」として明記。
- RAGやベクトルDB、LLMオーケストレーション等の高度AI技術は現状「構造のみ」存在し、実装・import実績はありません。
- 技術スタックのバージョン変更や新規導入時は必ず事前に承認を得てください。

---

## 🔷 パフォーマンス最適化

### 非同期処理
- **asyncio**: Python非同期プログラミング
- **aiohttp 3.9+**: 非同期HTTPクライアント
- **uvicorn 0.24+**: ASGI サーバー

### キャッシュ
- **Redis**: インメモリキャッシュ
- **aiocache**: 非同期キャッシュライブラリ

## 🔷 テスト・品質保証

### テスト
- **pytest-asyncio**: 非同期テスト
- **httpx**: テスト用HTTPクライアント
- **factory-boy**: テストデータ生成

### 品質管理
- **coverage**: テストカバレッジ
- **bandit**: セキュリティ監査
- **mypy**: 静的型チェック

---

## 🔷 フロントエンド技術 (LIFF用)

### 基本技術 (将来拡張時)
- **Vue.js 3.4+**: フロントエンドフレームワーク
- **TypeScript 5+**: 型安全性
- **Vite 5+**: ビルドツール
- **Tailwind CSS 3.4+**: CSSフレームワーク

## 🔷 データ処理・分析

### データ処理
- **Pandas 2.1+**: データ分析
- **NumPy 1.26+**: 数値計算
- **Matplotlib / Plotly**: データ可視化

## 🔷 バージョン管理・協調

### 開発協調
- **Git**: バージョン管理
- **GitHub**: コード管理、プロジェクト管理
- **GitHub Issues**: タスク管理

## 🔷 パフォーマンス最適化

### 非同期処理
- **asyncio**: Python非同期プログラミング
- **aiohttp 3.9+**: 非同期HTTPクライアント
- **uvicorn 0.24+**: ASGI サーバー

### キャッシュ
- **Redis**: インメモリキャッシュ
- **aiocache**: 非同期キャッシュライブラリ

## 🔷 テスト・品質保証

### テスト
- **pytest-asyncio**: 非同期テスト
- **httpx**: テスト用HTTPクライアント
- **factory-boy**: テストデータ生成

### 品質管理
- **coverage**: テストカバレッジ
- **bandit**: セキュリティ監査
- **mypy**: 静的型チェック

---

## 🔷 注意事項

⚠️ **重要**: このスタックのバージョンは検証済みの組み合わせです。バージョン変更は互換性問題を引き起こす可能性があるため、変更前に必ず承認を得てください。

⚠️ **AI API制限**: Google Gemini API のレート制限とコスト管理に注意してください。

⚠️ **スケーラビリティ**: 初期はシンプルな構成で開始し、ユーザー増加に応じて段階的にスケールアップしてください。 