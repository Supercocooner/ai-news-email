"""
AI News Fetcher - Google NewsからAI関連記事を取得
大手メディア・有力ソースを優先してランキング
"""
import feedparser
from typing import List, Dict
from urllib.parse import quote


# 大手メディア・テック専門メディアの優先度スコア
# スコアが高いほど優先表示される
PRIORITY_SOURCES = {
    # Tier 1: 最大手メディア (スコア: 100)
    "Reuters": 100,
    "Associated Press": 100,
    "Bloomberg": 100,
    "The New York Times": 100,
    "The Washington Post": 100,
    "The Wall Street Journal": 100,
    "BBC": 100,
    "CNN": 100,
    "NHK": 100,
    "日本経済新聞": 100,
    "Nikkei Asia": 100,
    
    # Tier 2: テック大手メディア (スコア: 90)
    "The Verge": 90,
    "Wired": 90,
    "Ars Technica": 90,
    "TechCrunch": 90,
    "MIT Technology Review": 90,
    "CNBC": 90,
    "The Guardian": 90,
    "Financial Times": 90,
    
    # Tier 3: テック・AI専門メディア (スコア: 80)
    "VentureBeat": 80,
    "The Information": 80,
    "Engadget": 80,
    "ZDNet": 80,
    "CNET": 80,
    "Mashable": 80,
    "TechRadar": 80,
    "The Register": 80,
    "Tech Xplore": 80,
    "SiliconANGLE": 80,
    
    # Tier 4: 公式ソース (スコア: 85)
    "Google": 85,
    "Google DeepMind": 85,
    "Google Blog": 85,
    "OpenAI": 85,
    "Anthropic": 85,
    "Microsoft": 85,
    
    # Tier 5: 有力メディア (スコア: 70)
    "Forbes": 70,
    "Business Insider": 70,
    "Hindustan Times": 70,
    "The Independent": 70,
    "Yahoo": 70,
    "PCMag": 70,
    "Tom's Guide": 70,
    "9to5Google": 70,
    "Android Authority": 70,
}

# デフォルトスコア（不明なソース）
DEFAULT_SCORE = 30


def _get_source_score(source_name: str) -> int:
    """
    ソース名から優先度スコアを取得
    部分一致でもマッチする
    """
    # 完全一致チェック
    if source_name in PRIORITY_SOURCES:
        return PRIORITY_SOURCES[source_name]
    
    # 部分一致チェック（ソース名にキーワードが含まれるか）
    source_lower = source_name.lower()
    for known_source, score in PRIORITY_SOURCES.items():
        if known_source.lower() in source_lower or source_lower in known_source.lower():
            return score
    
    return DEFAULT_SCORE



def fetch_ai_news_en(max_articles: int = 10) -> List[Dict]:
    """
    海外（英語）のAI関連ニュースを取得
    """
    return _fetch_news_by_lang(lang='en', region='US', max_articles=max_articles)


def fetch_ai_news_ja(max_articles: int = 10) -> List[Dict]:
    """
    国内（日本語）のAI関連ニュースを取得
    """
    return _fetch_news_by_lang(lang='ja', region='JP', max_articles=max_articles)


def _fetch_news_by_lang(lang: str, region: str, max_articles: int) -> List[Dict]:
    """
    指定された言語・地域でAI関連ニュースを取得
    """
    # 検索キーワード（言語ごとに最適化しても良いが、今回は共通で動作確認）
    # 日本語の場合は日本語クエリも追加すると精度向上
    if lang == 'ja':
        keywords = [
            "Gemini AI",
            "ChatGPT",
            "Claude AI Anthropic",
            "AI エージェント 人工知能",
            "生成AI"
        ]
    else:
        keywords = [
            "Gemini AI",
            "ChatGPT",
            "Claude AI Anthropic",
            "AI agent artificial intelligence"
        ]
    
    all_articles = []
    seen_urls = set()
    seen_titles = set()
    
    for keyword in keywords:
        articles = _fetch_google_news(keyword, lang, region)
        for article in articles:
            title_normalized = article['title'].lower().strip()
            if article['url'] not in seen_urls and title_normalized not in seen_titles:
                seen_urls.add(article['url'])
                seen_titles.add(title_normalized)
                article['priority_score'] = _get_source_score(article['source'])
                all_articles.append(article)
    
    # 優先度スコア（降順）→ 公開日時（降順）でソート
    all_articles.sort(
        key=lambda x: (x.get('priority_score', 0), x.get('published', '')),
        reverse=True
    )
    
    return all_articles[:max_articles]


def _fetch_google_news(keyword: str, lang: str = 'en', region: str = 'US') -> List[Dict]:
    """
    特定のキーワードでGoogle Newsを検索
    """
    encoded_keyword = quote(keyword)
    # hl, gl, ceid パラメータを動的に設定
    # 英語: hl=en-US&gl=US&ceid=US:en
    # 日本語: hl=ja&gl=JP&ceid=JP:ja
    
    if lang == 'ja':
        params = "hl=ja&gl=JP&ceid=JP:ja"
    else:
        params = "hl=en-US&gl=US&ceid=US:en"
        
    url = f"https://news.google.com/rss/search?q={encoded_keyword}&{params}"
    
    try:
        feed = feedparser.parse(url)
        articles = []
        
        for entry in feed.entries[:8]:
            article = {
                'title': entry.get('title', ''),
                'url': entry.get('link', ''),
                'summary': entry.get('summary', ''),
                'source': entry.get('source', {}).get('title', 'Unknown'),
                'published': entry.get('published', ''),
                'keyword': keyword,
                'lang': lang  # 言言語情報を追加
            }
            articles.append(article)
        
        return articles
    except Exception as e:
        print(f"Error fetching news for '{keyword}': {e}")
        return []


if __name__ == "__main__":
    print("--- 国内ニュース ---")
    news_ja = fetch_ai_news_ja(5)
    for i, article in enumerate(news_ja, 1):
        print(f"{i}. {article['title']} ({article['source']})")
    
    print("\n--- 海外ニュース ---")
    news_en = fetch_ai_news_en(5)
    for i, article in enumerate(news_en, 1):
        print(f"{i}. {article['title']} ({article['source']})")

