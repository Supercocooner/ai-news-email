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
import history_manager


def main():
    """メイン処理"""
    # .envファイルがあれば読み込む（ローカル開発用）
    load_dotenv()
    
    print("=" * 50)
    print("AI News Email System (国内/海外)")
    print("=" * 50)

    # 履歴の読み込み
    history = history_manager.load_history()
    history = history_manager.clean_old_history(history)
    
    # 1. ニュースを取得
    print("\n📰 国内ニュースを取得中...")
    articles_ja = fetch_ai_news_ja(max_articles=15) # フィルタリング分を見越して多めに取得
    print(f"   {len(articles_ja)}件の記事を取得しました")

    print("\n📰 海外ニュースを取得中...")
    articles_en = fetch_ai_news_en(max_articles=15)
    print(f"   {len(articles_en)}件の記事を取得しました")

    # 重複排除フィルタリング
    articles_ja = history_manager.filter_new_articles(articles_ja, history)
    articles_en = history_manager.filter_new_articles(articles_en, history)
    
    # 最大10件に制限
    articles_ja = articles_ja[:10]
    articles_en = articles_en[:10]

    print(f"   重複排除後: 国内 {len(articles_ja)}件, 海外 {len(articles_en)}件")
    
    if not articles_ja and not articles_en:
        print("   新規記事が見つかりませんでした。送信をスキップします。")
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
    translated_articles_ja = []
    for article in articles_ja:
        translated_articles_ja.append(translate_article(article))

    # 3. メール送信
    print("\n📧 メール送信中...")
    recipient = os.environ.get('RECIPIENT_EMAIL', 'supercocooner@gmail.com')
    success = send_email(translated_articles_ja, translated_articles_en, recipient)
    
    if success:
        # 送信成功した記事を履歴に追加して保存
        history = history_manager.update_history(history, articles_ja + articles_en)
        history_manager.save_history(history)
        print("\n✅ 完了しました！")
    else:
        print("\n❌ メール送信に失敗しました")
        sys.exit(1)


if __name__ == "__main__":
    main()
