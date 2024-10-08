import logging
import os
from dotenv import load_dotenv
from sqlalchemy import and_
from app.db.models import TimesTweet
from app.db.database import get_db
from datetime import datetime, date
from app.services.redis_client import redis_client

load_dotenv()

log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

CACHE_KEY_PREFIX = 'times_tweet'

# 取得したデータを通常の文字列に変換する必要がある場合は以下の処理を加える。
def compile_times_tweet_data(times_tweet_data):
    if not times_tweet_data:
        logger.info("◆文字列に変換しようとしているtimesの投稿データが見つかりません。")
        compiled_times_tweet_data = "日報記録がありません。"
    else:
        compiled_times_tweet_data = "\n".join(
            f"ID: {tweet.id}, Channel ID: {tweet.channel_id}, User ID: {tweet.slack_user_id}, Text: {tweet.text}, Timestamp: {tweet.ts}, Thread Timestamp: {tweet.thread_ts}, Parent User ID: {tweet.parent_user_id}, Created At: {tweet.created_at}"
            for tweet in times_tweet_data
        )
        logger.debug("◆timesの投稿データを読解可能な文字列に変換しました。")
    
    return compiled_times_tweet_data
def get_times_tweet(slack_user_id: str, start_date: date, end_date: date):
    # キャッシュキーの生成
    cache_key = f"{CACHE_KEY_PREFIX}{slack_user_id}:{start_date}:{end_date}"
    
    # Redisからキャッシュデータを取得
    cached_data = redis_client.get(cache_key)
    if cached_data:
        logger.info("◆キャッシュからtimesの投稿データを取得しました。")
        return cached_data.decode('utf-8')
    
    # YYYY-MM-DD から　Unixタイムスタンプ形式に変換する
    start_datetime = datetime.combine(start_date, datetime.min.time())
    end_datetime = datetime.combine(end_date, datetime.max.time())
    logger.debug(f"start_data: {start_date} => start: {start_datetime}")
    logger.debug(f"end_date: {end_date} => end: {end_datetime}")
    # データベースから指定したユーザーの指定期間分のtimesの投稿データを取得する
    db = get_db()
    try:
        target_times_tweet = db.query(TimesTweet).filter(
            and_(
                TimesTweet.slack_user_id == slack_user_id,
                TimesTweet.created_at >= start_datetime, 
                TimesTweet.created_at <= end_datetime
            )
        ).all()
        logger.debug("◆DBから正常にtimesの投稿データを取得できました。")
        response = compile_times_tweet_data(target_times_tweet)

        redis_client.set(cache_key, response, ex=43200)  # 12時間 = 43200秒
        
        return response
    except Exception as e:
        logger.error(f"""◆
        timesの投稿を取得中にエラーが発生しました。: {e}
        """)
        return[]
    finally:
        db.close()