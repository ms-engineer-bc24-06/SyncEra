import os
from dotenv import load_dotenv
import logging
from sqlalchemy.orm import Session
from openai import OpenAI
# from app.database import SessionLocal
# from app.models import テーブル名
from util.get_user_info import get_user_info
from util.get_daily_report import get_daily_report
from util.get_times_tweet import get_times_tweet
from make_summary import make_summarize_report

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def make_advices(user_id, start_date, end_date):
    try:
        user_info = get_user_info(user_id)
        daily_report = get_daily_report(user_id, start_date, end_date)
        times_tweet = get_times_tweet(user_id, start_date, end_date)
        summary = make_summarize_report(user_id, start_date, end_date)

        if not user_info:
            logger.error("◆user_infoの取得に失敗しました")
        else:
            logger.info("◆user_infoの取得に成功しました")

        if not daily_report:
            logger.error("◆daily_reportの取得に失敗しました")
        else:
            logger.info("◆daily_reportの取得に成功しました")

        if not times_tweet:
            logger.error("◆timesの投稿データ取得に失敗しました")
        else:
            logger.info("◆timesの投稿データ取得に成功しました")

        prompt = f"""
        あなたは職場内コミュニケーション活性化を推進するプロフェッショナルです。
        今、あなたはある上司からアドバイスが欲しいと相談を受けています。
        その上司はこれから部下と1on1を実施するようですが、なかなか部下の本音を聞き出せず、1on1が有効活用できていないと悩んでいるようです。
        本来1on1では部下が主役となり、仕事のことやキャリアのことはもちろん、公私問わず最近のことを話し上司部下の信頼関係構築や会社へのエンゲージメント向上を狙いとして実施されます。
        この上司は、あなたに以下のことを期待しています。末尾の参考情報から、上司の期待に応えてください。
        【期待していること】1on1を有効活用するために、上司から部下に切り出すと部下が食いついてきそうな話題や褒めるべき点、投げかけると部下の本音が聞き出せそうな質問
        【参考情報】
        1)部下の日報: {daily_report}
        2)部下のslackのtimesの呟き: {times_tweet}
        3)部下のプロフィール: {user_info}
        4)1~3をもとに作成した要約文: {summary}
        """

        response = client.Completion.create(
            model="gpt-4", #gpt4o-miniでもいいかも
            prompt=prompt,
            max_tokens=1000,
            temperature=0.5, #可変部
        )

        advices = response.choices[0].text.strip()
        logger.debug(f"◆LLMが生成した1on1のアドバイス: {advices}")

        return advices
    except Exception:
        return f"アドバイス生成中のエラー: {Exception}"


# テストするなら以下をアレンジ
if __name__ == "__main__":
    user_id = 1
    start_date = "2024-07-29"
    end_date = "2024-08-2"
    advices = make_advices(user_id, start_date, end_date)
    print(advices)