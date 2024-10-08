from sqlalchemy import Column, String, Integer, Text, ForeignKey, TIMESTAMP, Float,Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
from .database import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employee'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    department = Column(String(100), nullable=False)
    role = Column(String(100), nullable=False)
    project = Column(String(100), nullable=False)
    slack_user_id = Column(String, ForeignKey('slack_user_info.id'), nullable=False, unique=True)
    
    slack_user_info = relationship("SlackUserInfo", back_populates="employee")
    responses = relationship("UserResponse", back_populates="employee")

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "email": self.email,
            "department": self.department,
            "role": self.role,
            "project": self.project,
            "slack_user_id": self.slack_user_id,  # Add slack_user_id if necessary
            "slack_user_info": self.slack_user_info.to_dict() if self.slack_user_info else None,
        }

class SlackUserInfo(Base):
    __tablename__ = 'slack_user_info'

    id = Column(String(100), primary_key=True)
    name = Column(String(100), nullable=False)
    real_name = Column(String(100), nullable=False)
    image_512 = Column(String, nullable=True)

    employee = relationship("Employee", back_populates="slack_user_info")
    analysis_results = relationship("AnalysisResult", back_populates="slack_user_info")
    summarize_histories = relationship("SummarizeHistory", back_populates="slack_user_info")
    advices_histories = relationship("AdvicesHistory", back_populates="slack_user_info")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "real_name": self.real_name,
            "image_512": self.image_512
        }

class DailyReport(Base):
    __tablename__ = 'daily_report'

    id = Column(Integer, primary_key=True, autoincrement=True)
    slack_user_id = Column(String(100), ForeignKey('slack_user_info.id'), nullable=False)
    text = Column(Text, nullable=False)
    ts = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    def __repr__(self):
        return f"<DailyReport(id={self.id}, user_id={self.user_id}, text={self.text}, ts={self.ts}, created_at={self.created_at})>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "slack_user_id": self.slack_user_id,
            "text": self.text,
            "ts": self.ts,
            "created_at": self.created_at, 
        }

class TimesTweet(Base):
    __tablename__ = 'times_tweet'

    id = Column(Integer, primary_key=True, autoincrement=True)
    channel_id = Column(String, ForeignKey('times_list.channel_id'), nullable=False)
    slack_user_id = Column(String(100), ForeignKey('slack_user_info.id'), nullable=False)
    text = Column(Text, nullable=False)
    ts = Column(Float, nullable=False)
    thread_ts = Column(Float, nullable=True)
    parent_user_id = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    def __repr__(self):
        return f"<TimesTweet(id={self.id}, user_id={self.user_id}, text={self.text}, created_at={self.created_at})>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "channel_id": self.channel_id,
            "slack_user_id": self.slack_user_id,
            "text": self.text,
            "ts": self.ts,
            "thread_ts": self.thread_ts,
            "parent_user_id": self.parent_user_id,
            "created_at": self.created_at, 
        }

class TimesList(Base):
    __tablename__ = 'times_list'

    slack_user_id = Column(String(100), ForeignKey('slack_user_info.id'), nullable=False)
    channel_name = Column(String(100), nullable=False)
    channel_id = Column(String(100), primary_key=True, nullable=False)

class ContactForm(Base):
    __tablename__ = 'contact_form'

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_name = Column(String(100), nullable=False) # 追加
    department = Column(String(100), nullable=True) # 追加
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

class SummarizeHistory(Base):
    __tablename__ = 'summarize_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    slack_user_id = Column(String(100), ForeignKey('slack_user_info.id'), nullable=False)
    summary = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    slack_user_info = relationship("SlackUserInfo", back_populates="summarize_histories")

    def __repr__(self):
        return f"<SummarizeHistory(id={self.id}, slack_user_id={self.slack_user_id}, summary='{self.summary}', created_at={self.created_at})>"

    def to_dict(self):
        return {
            "id": self.id,
            "slack_user_id": self.slack_user_id,
            "summary": self.summary,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }
class AdvicesHistory(Base):
    __tablename__ = 'advices_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    slack_user_id = Column(String(100), ForeignKey('slack_user_info.id'), nullable=False)
    advices = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    slack_user_info = relationship("SlackUserInfo", back_populates="advices_histories")
    def __repr__(self):
        return f"<AdvicesHistory(id={self.id}, slack_user_id={self.slack_user_id}, advices='{self.advices}', created_at={self.created_at})>"

    def to_dict(self):
        return {
            "id": self.id,
            "slack_user_id": self.slack_user_id,
            "advices": self.advices,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
        }


# ここからcareer_survey用の定義

class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String, nullable=False)
    choice_a = Column(String, nullable=True)
    choice_b = Column(String, nullable=True)
    choice_c = Column(String, nullable=True)
    choice_d = Column(String, nullable=True)
    next_question_a_id = Column(Integer, ForeignKey('questions.id'), nullable=True)
    next_question_b_id = Column(Integer, ForeignKey('questions.id'), nullable=True)
    next_question_c_id = Column(Integer, ForeignKey('questions.id'), nullable=True)
    next_question_d_id = Column(Integer, ForeignKey('questions.id'), nullable=True)

    next_question_a = relationship("Question", remote_side=[id], foreign_keys=[next_question_a_id])
    next_question_b = relationship("Question", remote_side=[id], foreign_keys=[next_question_b_id])
    next_question_c = relationship("Question", remote_side=[id], foreign_keys=[next_question_c_id])
    next_question_d = relationship("Question", remote_side=[id], foreign_keys=[next_question_d_id])
    responses = relationship("UserResponse", order_by="UserResponse.id", back_populates="question")

class UserResponse(Base):
    __tablename__ = 'responses'

    id = Column(Integer, primary_key=True, index=True)
    slack_user_id = Column(String, ForeignKey('employee.slack_user_id'), nullable=False)
    question_id = Column(Integer, ForeignKey('questions.id'))
    answer = Column(String)
    free_text = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    employee = relationship("Employee", back_populates="responses")
    question = relationship("Question", back_populates="responses")

# 分析後のアンケート結果をDB保存しておくテーブル
class AnalysisResult(Base):
    __tablename__ = 'analysis_result'

    id = Column(Integer, primary_key=True, autoincrement=True)
    slack_user_id = Column(String, ForeignKey('slack_user_info.id'), nullable=False)
    result = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    slack_user_info = relationship("SlackUserInfo", back_populates="analysis_results")

    def __repr__(self):
        return f"<AnalysisResult(id={self.id}, slack_user_id={self.slack_user_id}, result={self.result}, created_at={self.created_at})>"

    def to_dict(self):
        return {
            "id": self.id,
            "slack_user_id": self.slack_user_id,
            "result": self.result,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }