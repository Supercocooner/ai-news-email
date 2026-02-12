# 🤖 AI News Email System

Google NewsからAI関連ニュース（Gemini、ChatGPT、Claude、AIエージェント）を取得し、毎日10時と17時に自動でメール配信するシステムです。

## 機能

- 📰 Google News RSSから最新AI関連記事を取得
- 🌐 英語記事を自動で日本語に翻訳
- 📧 HTML形式の見やすいメールで配信
- ⏰ GitHub Actionsで毎日自動実行（10:00, 17:00 JST）

## セットアップ手順

### 1. GitHubにリポジトリを作成

1. [GitHub](https://github.com/new) で新しいリポジトリを作成
2. **リポジトリ名**: `ai-news-email`（任意）
3. **公開設定**: **Public**（無料でGitHub Actionsを使うため）

### 2. コードをアップロード

```bash
cd /Users/tomo/マイドライブ/google_antigravity/news_AI

# Gitリポジトリを初期化
git init
git add .
git commit -m "Initial commit: AI News Email System"

# GitHubリポジトリと連携
git remote add origin https://github.com/YOUR_USERNAME/ai-news-email.git
git branch -M main
git push -u origin main
```

### 3. Gmailアプリパスワードを取得

1. [Googleアカウント](https://myaccount.google.com/) にアクセス
2. **セキュリティ** → **2段階認証** を有効化
3. **アプリパスワード** を生成
   - アプリ: 「メール」
   - デバイス: 「その他」→「GitHub Actions」
4. 表示された16文字のパスワードをコピー

### 4. GitHub Secretsを設定

1. GitHubリポジトリページ → **Settings** → **Secrets and variables** → **Actions**
2. **New repository secret** をクリックし、以下を追加：

| Name | Value |
|------|-------|
| `GMAIL_ADDRESS` | あなたのGmailアドレス |
| `GMAIL_APP_PASSWORD` | 取得した16文字のアプリパスワード |
| `RECIPIENT_EMAIL` | `ohsako@psycholo.net` |

### 5. 動作確認

1. リポジトリページ → **Actions** タブ
2. 「AI News Email」ワークフロー → **Run workflow** をクリック
3. 数分後にメールが届けば成功！

## ローカルでテスト

```bash
# 依存関係をインストール
pip install -r requirements.txt

# 環境変数を設定
cp .env.example .env
# .env ファイルを編集してGmail情報を入力

# 実行
python main.py
```

## ファイル構成

```
news_AI/
├── main.py              # メインスクリプト
├── news_fetcher.py      # ニュース取得
├── translator.py        # 翻訳処理
├── email_sender.py      # メール送信
├── requirements.txt     # 依存関係
├── .env.example         # 環境変数テンプレート
├── .gitignore
└── .github/
    └── workflows/
        └── news_email.yml   # GitHub Actions設定
```

## カスタマイズ

### 検索キーワードを変更

`news_fetcher.py` の `keywords` リストを編集：

```python
keywords = [
    "Gemini AI",
    "ChatGPT",
    "Claude AI Anthropic",
    "AI agent artificial intelligence"
]
```

### 配信時間を変更

`.github/workflows/news_email.yml` の cron 設定を編集：

```yaml
schedule:
  - cron: '0 1 * * *'   # UTC 01:00 = JST 10:00
  - cron: '0 8 * * *'   # UTC 08:00 = JST 17:00
```

## トラブルシューティング

### メールが届かない
- GitHub Secretsが正しく設定されているか確認
- Gmailの「安全性の低いアプリへのアクセス」が有効か確認
- Actionsタブでエラーログを確認

### 翻訳が機能しない
- deep-translatorのAPI制限に達した可能性があります
- しばらく待ってから再実行してください

## ライセンス

MIT License
