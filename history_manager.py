"""
History Manager - 送信済み記事の履歴管理とフィルタリング
"""
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict

HISTORY_FILE = "sent_history.json"
EXPIRE_DAYS = 2  # 2日間（48時間）

def load_history() -> Dict[str, str]:
    """履歴ファイルを読み込む"""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading history: {e}")
            return {}
    return {}

def save_history(history: Dict[str, str]):
    """履歴ファイルを保存する"""
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving history: {e}")

def clean_old_history(history: Dict[str, str]) -> Dict[str, str]:
    """有効期限を過ぎた履歴を削除する"""
    now = datetime.now()
    cleaned_history = {}
    
    for url, timestamp_str in history.items():
        try:
            timestamp = datetime.fromisoformat(timestamp_str)
            if now - timestamp < timedelta(days=EXPIRE_DAYS):
                cleaned_history[url] = timestamp_str
        except (ValueError, TypeError):
            # 無効な形式のデータは破棄
            continue
            
    return cleaned_history

def filter_new_articles(articles: List[Dict], history: Dict[str, str]) -> List[Dict]:
    """履歴にあるURLの記事を除外する"""
    return [a for a in articles if a.get('url') not in history]

def update_history(history: Dict[str, str], new_articles: List[Dict]) -> Dict[str, str]:
    """新しい記事を履歴に追加する"""
    now_str = datetime.now().isoformat()
    updated_history = history.copy()
    
    for article in new_articles:
        url = article.get('url')
        if url:
            updated_history[url] = now_str
            
    return updated_history
