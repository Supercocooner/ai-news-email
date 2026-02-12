"""
AI News Email System - メインエントリーポイント
Google NewsからAI関連ニュースを取得し、翻訳してメール送信
"""
import os
import sys
from dotenv import load_dotenv

from news_fetcher import fetch_ai_news_ja, fetch_ai_news_en
from translator import translate_article
from email_sender import send_email


def main():
    """メイン処理"""
    # .envファイルがあれば読み込む（ローカル開発用）
    load_dotenv()
    
    print("=" * 50)
    print("AI News Email System (国内/海外)")
    print("=" * 50)
    
    # 1. ニュースを取得
    print("\n📰 国内ニュースを取得中...")
    articles_ja = fetch_ai_news_ja(max_articles=10)
    print(f"   {len(articles_ja)}件の記事を取得しました")

    print("\n📰 海外ニュースを取得中...")
    articles_en = fetch_ai_news_en(max_articles=10)
    print(f"   {len(articles_en)}件の記事を取得しました")
    
    if not articles_ja and not articles_en:
        print("   記事が見つかりませんでした")
        return
    
    # 2. 翻訳（海外ニュースのみ）
    print("\n🌐 翻訳中（海外ニュースのみ）...")
    translated_articles_en = []
    for i, article in enumerate(articles_en, 1):
        print(f"   [{i}/{len(articles_en)}] {article['title'][:50]}...")
        translated = translate_article(article)
        translated_articles_en.append(translated)
    print("   翻訳完了")
    
    # 国内ニュースは翻訳不要（そのままリストへ）
    # ただし、データ構造を合わせるために念のためtranslate_articleを通しても良いが、
    # translator.py内で「日本語ならそのまま返す」ロジックが入っているので安全。
    translated_articles_ja = []
    for article in articles_ja:
        translated_articles_ja.append(translate_article(article))

    # 3. メール送信
    print("\n📧 メール送信中...")
    recipient = os.environ.get('RECIPIENT_EMAIL', 'supercocooner@gmail.com')
    success = send_email(translated_articles_ja, translated_articles_en, recipient)
    
    if success:
        print("\n✅ 完了しました！")
    else:
        print("\n❌ メール送信に失敗しました")
        sys.exit(1)


if __name__ == "__main__":
    main()
