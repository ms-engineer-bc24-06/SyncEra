from fastapi import APIRouter

router = APIRouter()

# 日報が投稿された時　`POST /post_daily_report`　`by Slack`
@router.post("/post_daily_report/")
def save_daily_report():
    return "処理なども全て未実装、随時ここは追記していく"

# timesに投稿があった時 `POST /post_times` 　`by Slack`
@router.post("/post_times")
def save_times_tweet():
    return "処理なども全て未実装、随時ここは追記していく"

# キャリアアンケート実施のリクエストがあった時　GET or POST /execution_career_survey by Slack
@router.get("/execution_career_survey") # または @router.post("/execution_career_survey")
def execution_career_survey():
    return "処理なども全て未実装、随時ここは追記していく"

# キャリアアンケートの回答が提出された時 POST /post_career_survey　by Slack
@router.post("/post_career_survey")
def save_career_survey():
    return "処理なども全て未実装、随時ここは追記していく"

# 以下はPOSTリクエストのみを受け付けているエンドポイントが正常に解説されているか確認するためのコード
@router.get("/post_daily_report/")
def check_endpoint():
    return "/post_daily_report エンドポイントOKだよ!!"

@router.post("/post_times")
def check_endpoint():
    return "/post_times エンドポイントOKだよ!!"

@router.post("/post_career_survey")
def check_endpoint():
    return "/post_career_survey エンドポイントOKだよ!!"