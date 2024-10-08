from app.db.database import get_db, SessionLocal
from app.db.models import Employee
from sqlalchemy.orm import Session
from app.db.models import Question, Employee
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from app.services.redis_client import redis_client
from app.util.career_survey.question_cache import serialize_question
import os
import logging

log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

slack_token = os.getenv("SLACK_API_KEY")
client = WebClient(token=slack_token)

# send/messageのロジックを利用して、社員個々にアンケートを送信する
def send_survey_to_employee(slack_user_id: str, first_question: Question):
    text = first_question.question_text
    attachments = [
        {
            "text": "選択肢を選んでください",
            "fallback": "選択肢を選んでください。",
            "callback_id": str(first_question.id),
            "color": "#3AA3E3",
            "attachment_type": "default",
            "actions": [
                {
                    "name": "answer",
                    "text": first_question.choice_a,
                    "type": "button",
                    "value": "A"
                },
                {
                    "name": "answer",
                    "text": first_question.choice_b,
                    "type": "button",
                    "value": "B"
                },
                {
                    "name": "answer",
                    "text": first_question.choice_c,
                    "type": "button",
                    "value": "C"
                },
                {
                    "name": "answer",
                    "text": first_question.choice_d,
                    "type": "button",
                    "value": "D"
                }
            ]
        }
    ]
    try:
        response = client.chat_postMessage(
            channel=slack_user_id,
            text=text,
            attachments=attachments
        )
    except SlackApiError as e:
        logger.error(f"Error sending message: {e.response['error']}")

# 自由記述の質問を送信する関数
def send_survey_with_text_input(slack_user_id: str, question: Question):
    text = question.question_text
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": text
            }
        },
        {
            "type": "input",
            "block_id": str(question.id),
            "element": {
                "type": "plain_text_input",
                "action_id": "free_text_input",
                "multiline": True,  # 複数行入力を許可する
                "placeholder": {
                    "type": "plain_text",
                    "text": "ここに自由に記入してください"
                }
            },
            "label": {
                "type": "plain_text",
                "text": "ご自由にご記入ください"
            }
        },
        {
            "type": "actions",
            "block_id": "submit_action",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "送信"
                    },
                    "value": str(question.id),
                    "action_id": "submit_button",
                    "style": "primary"
                }
            ]
        }
    ]
    try:
        response = client.chat_postMessage(
            channel=slack_user_id,
            blocks=blocks,
            text=text
        )
    except SlackApiError as e:
        logger.error(f"Error sending message: {e.response['error']}")


# 初回の質問を取得するためのヘルパー関数
# 引数: db (Session): SQLAlchemyのデータベースセッションオブジェクト。
# 戻り値: Question: データベースから取得した初回の質問オブジェクト。
def get_first_question(db: Session) -> Question:
    first_question = db.query(Question).filter(Question.id == 1).first()  # id=1 の質問を初回の質問とみなして取得
    return first_question

# アンケートの質問をキャッシュに保存する関数
def cache_questions():
    db = SessionLocal()
    try:
        questions = db.query(Question).all()
        for question in questions:
            question_key = f"question:{question.id}"
            serialized_question = serialize_question(question)
            redis_client.set(question_key, serialized_question)
            logger.info(f"キャッシュに質問を保存しました: {question_key}")
    finally:
        db.close()

# DBに登録された社員全員に send_survey_to_employee 関数を適用する(=全員にアンケートを配信する)
def send_survey_to_all():
    db = SessionLocal()  # ここでDBセッションを作成
    try:
        first_question = get_first_question(db)  # 初回の質問を取得
        employees = db.query(Employee).all()
        for employee in employees:
            send_survey_to_employee(employee.slack_user_id, first_question)  # first_questionを渡す
    finally:
        db.close()  # セッションを確実に閉じる
