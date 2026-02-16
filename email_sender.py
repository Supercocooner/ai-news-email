"""
Email Sender - Gmail SMTPを使用してメール送信
"""
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict
import pytz
from datetime import datetime


def create_section_html(title: str, articles: List[Dict]) -> str:
    """ニュースセクションのHTMLを作成"""
    if not articles:
        return f"<h3>{title}</h3><p>該当する記事はありませんでした。</p>"
        
    html = f"<h3>{title}</h3>"
    for i, article in enumerate(articles, 1):
        title_text = article.get('title_ja', article.get('title', 'タイトルなし'))
        # 元のタイトル（翻訳された場合のみ表示）
        original_title_html = ""
        if article.get('lang') == 'en' and 'title_ja' in article:
             original_title_html = f'<p class="original-title">📰 {article.get("title", "")}</p>'
        elif article.get('lang') == 'ja':
             # 国内ニュースの場合は元タイトル表示不要（または同じ）
             original_title_html = ""

        summary_text = article.get('summary_ja', article.get('summary', ''))
        url = article.get('url', '#')
        source = article.get('source', 'Unknown')
        keyword = article.get('keyword', '')
        
        html += f"""
        <div class="article">
            <h2><a href="{url}" target="_blank">{title_text}</a></h2>
            {original_title_html}
            <p class="summary">{summary_text[:200]}{'...' if len(summary_text) > 200 else ''}</p>
            <p class="meta">
                <span class="keyword">{keyword}</span>
                ソース: {source}
            </p>
        </div>
        """
    return html


def create_html_email(articles_ja: List[Dict], articles_en: List[Dict]) -> str:
    """
    記事リストからHTMLメール本文を作成（国内・海外）
    """
    jst = pytz.timezone('Asia/Tokyo')
    now = datetime.now(jst).strftime("%Y年%m月%d日 %H:%M")
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: 'Helvetica Neue', Arial, 'Hiragino Kaku Gothic ProN', sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }}
            h1 {{
                color: #1a73e8;
                border-bottom: 2px solid #1a73e8;
                padding-bottom: 10px;
            }}
            h3 {{
                background-color: #f1f3f4;
                padding: 10px;
                border-left: 5px solid #1a73e8;
                margin-top: 30px;
            }}
            .article {{
                background: #fff;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 15px;
                margin: 15px 0;
            }}
            .article h2 {{
                margin: 0 0 10px 0;
                font-size: 16px;
            }}
            .article h2 a {{
                color: #1a73e8;
                text-decoration: none;
            }}
            .article h2 a:hover {{
                text-decoration: underline;
            }}
            .original-title {{
                color: #666;
                font-size: 12px;
                margin: 5px 0;
                font-style: italic;
            }}
            .summary {{
                color: #444;
                font-size: 14px;
            }}
            .meta {{
                color: #888;
                font-size: 12px;
                margin-top: 10px;
                display: flex;
                align-items: center;
                gap: 10px;
            }}
            .keyword {{
                display: inline-block;
                background: #e8f0fe;
                color: #1a73e8;
                padding: 2px 8px;
                border-radius: 12px;
                font-size: 11px;
            }}
            .footer {{
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px solid #ddd;
                color: #888;
                font-size: 12px;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <h1>🤖 AI最新ニュース</h1>
        <p>{now} 配信 (JST)</p>
        
        {create_section_html("🇯🇵 国内ニュース", articles_ja)}
        {create_section_html("🇺🇸 海外ニュース", articles_en)}
    
        <div class="footer">
            <p>このメールはAI News Email Systemにより自動送信されました。</p>
        </div>
    </body>
    </html>
    """
    
    return html


def send_email(articles_ja: List[Dict], articles_en: List[Dict], recipient: str = None) -> bool:
    """
    AI関連ニュースをメールで送信
    """
    # 環境変数から設定を取得
    gmail_address = os.environ.get('GMAIL_ADDRESS')
    gmail_password = os.environ.get('GMAIL_APP_PASSWORD')
    recipient = recipient or os.environ.get('RECIPIENT_EMAIL', gmail_address)
    
    if not gmail_address or not gmail_password:
        print("Error: GMAIL_ADDRESS and GMAIL_APP_PASSWORD environment variables are required")
        return False
    
    # メール作成
    jst = pytz.timezone('Asia/Tokyo')
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"🤖 AI最新ニュース (国内/海外) - {datetime.now(jst).strftime('%m/%d %H:%M')}"
    msg['From'] = gmail_address
    msg['To'] = recipient
    
    # HTML本文
    html_content = create_html_email(articles_ja, articles_en)
    msg.attach(MIMEText(html_content, 'html', 'utf-8'))
    
    # 送信
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(gmail_address, gmail_password)
            server.send_message(msg)
        print(f"Email sent successfully to {recipient}")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False



if __name__ == "__main__":
    # テスト用ダミーデータ
    test_articles = [
        {
            'title': 'Test Article',
            'title_ja': 'テスト記事',
            'summary': 'This is a test summary',
            'summary_ja': 'これはテスト要約です',
            'url': 'https://example.com',
            'source': 'Test Source',
            'keyword': 'ChatGPT'
        }
    ]
    send_email(test_articles)
