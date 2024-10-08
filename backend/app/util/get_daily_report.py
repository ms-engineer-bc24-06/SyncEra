import logging
import os
from dotenv import load_dotenv
from sqlalchemy import and_
from app.db.models import DailyReport
from datetime import date, datetime
from app.db.database import get_db
from app.services.redis_client import redis_client

load_dotenv()

log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# 取得したデータを通常の文字列に変換する必要がある場合は以下の処理を加える。
def compile_daily_report_data(daily_report_data):
    if not daily_report_data:
        logger.info("文字列に変換しようとしている日報データが見つからないか、空のようです。")
        compiled_daily_report_data = "日報記録がありません。"
    else:
        # daily_report_dataが存在する場合
        compiled_daily_report_data = "\n".join(
            f"ID: {report.id}, User ID: {report.slack_user_id}, Text: {report.text}, Timestamp: {report.ts}, Created At: {report.created_at}"
            for report in daily_report_data
        )
        logger.debug("◆日報データを読解可能な文字列に変換しました。")
    
    return compiled_daily_report_data

def get_daily_report(slack_user_id: str, start_date:date, end_date:date):
    start_datetime = datetime.combine(start_date, datetime.min.time())
    end_datetime = datetime.combine(end_date, datetime.max.time())
    logger.debug(f"start_data: {start_date} => start: {start_datetime}")
    logger.debug(f"end_date: {end_date} => end: {end_datetime}")

    # キャッシュキーの生成
    cache_key = f"daily_report:{slack_user_id}:{start_date}:{end_date}"

    # キャッシュからデータを取得
    cached_report = redis_client.get(cache_key)
    if cached_report:
        logger.debug("◆キャッシュから日報データを取得しました。")
        return cached_report

    # データベースから指定したユーザーの指定期間分の日報データを取得する
    db = get_db()
    try:
        target_daily_report = db.query(DailyReport).filter(
            and_(
                DailyReport.slack_user_id == slack_user_id,
                DailyReport.created_at >= start_datetime, 
                DailyReport.created_at <= end_datetime
            )
        ).all()
        logger.debug("◆DBから正常に日報データを取得できました。")
        response = compile_daily_report_data(target_daily_report)

        # キャッシュに保存（有効期限12時間）
        redis_client.set(cache_key, response, ex=43200)

        return response
    except Exception as e:
        logger.error(f"◆daily_reportの取得中にエラーが発生しました。: {e}")
        return[]
    finally:
        db.close()