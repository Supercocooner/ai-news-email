"""
Translator - deep-translatorを使用して英語→日本語翻訳
"""
from deep_translator import GoogleTranslator
from typing import Optional
import re


def is_japanese(text: str) -> bool:
    """テキストが日本語かどうかを判定"""
    # ひらがな、カタカナ、漢字が含まれているかチェック
    japanese_pattern = re.compile(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]')
    return bool(japanese_pattern.search(text))


def translate_to_japanese(text: str) -> str:
    """
    英語テキストを日本語に翻訳
    
    Args:
        text: 翻訳するテキスト
        
    Returns:
        日本語に翻訳されたテキスト
    """
    if not text or not text.strip():
        return text
    
    # すでに日本語の場合はそのまま返す
    if is_japanese(text):
        return text
    
    try:
        translator = GoogleTranslator(source='en', target='ja')
        # テキストが長すぎる場合は切り詰める（API制限対策）
        if len(text) > 4500:
            text = text[:4500] + "..."
        
        translated = translator.translate(text)
        return translated if translated else text
    except Exception as e:
        print(f"Translation error: {e}")
        return text  # エラー時は原文を返す


def translate_article(article: dict) -> dict:
    """
    記事のタイトルと要約を翻訳
    
    Args:
        article: 記事辞書（title, summary等を含む）
        
    Returns:
        翻訳済みの記事辞書
    """
    translated = article.copy()
    
    # タイトルを翻訳
    if 'title' in translated:
        translated['title_ja'] = translate_to_japanese(translated['title'])
    
    # 要約を翻訳
    if 'summary' in translated:
        # HTMLタグを除去
        summary_clean = re.sub(r'<[^>]+>', '', translated['summary'])
        translated['summary_ja'] = translate_to_japanese(summary_clean)
    
    return translated


if __name__ == "__main__":
    # テスト実行
    test_text = "OpenAI releases new ChatGPT features for developers"
    print(f"Original: {test_text}")
    print(f"Translated: {translate_to_japanese(test_text)}")
