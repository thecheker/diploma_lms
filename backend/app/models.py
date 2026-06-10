import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, JSON, Integer, ForeignKey, Enum as SQLEnum, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from enum import Enum

class CourseCategory(str, Enum):
    PROGRAMMING = "programming"
    DESIGN = "design"
    MARKETING = "marketing"
    BUSINESS = "business"
    LANGUAGES = "languages"
    OTHER = "other"

class Role(str, Enum):
    STUDENT = "STUDENT"
    INSTRUCTOR = "INSTRUCTOR"
    ADMIN = "ADMIN"

class LessonType(str, Enum):
    TEXT = "TEXT"
    VIDEO = "VIDEO"

class QuestionType(str, Enum):
    SINGLE_CHOICE = "SINGLE_CHOICE"
    MULTIPLE_CHOICE = "MULTIPLE_CHOICE"
    TRUE_FALSE = "TRUE_FALSE"

class AttemptStatus(str, Enum):
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    AUTO_GRADED = "AUTO_GRADED"

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String)
    role: Mapped[str] = mapped_column(SQLEnum(Role), default=Role.STUDENT)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    attempts: Mapped[list["Attempt"]] = relationship("Attempt", back_populates="user")

class Course(Base):
    __tablename__ = "courses"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(String, default="")
    instructor: Mapped[str] = mapped_column(String, default="")
    image: Mapped[str] = mapped_column(String, default="")
    category: Mapped[str] = mapped_column(String, default=CourseCategory.OTHER)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    lessons: Mapped[list["Lesson"]] = relationship("Lesson", back_populates="course", cascade="all, delete-orphan")

class Lesson(Base):
    __tablename__ = "lessons"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    course_id: Mapped[str] = mapped_column(String, ForeignKey("courses.id"))
    title: Mapped[str] = mapped_column(String)
    lesson_type: Mapped[str] = mapped_column(String, default=LessonType.TEXT)
    content: Mapped[dict] = mapped_column(JSON, default=dict)
    order_index: Mapped[int] = mapped_column(Integer, default=0)
    course: Mapped["Course"] = relationship("Course", back_populates="lessons")
    quiz: Mapped[Optional["Quiz"]] = relationship("Quiz", back_populates="lesson", uselist=False)

class Quiz(Base):
    __tablename__ = "quizzes"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    lesson_id: Mapped[str] = mapped_column(String, ForeignKey("lessons.id"))
    title: Mapped[str] = mapped_column(String)
    time_limit_sec: Mapped[int] = mapped_column(Integer, default=600)
    passing_score: Mapped[float] = mapped_column(Float, default=0.7)
    creator_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=True)
    lesson: Mapped["Lesson"] = relationship("Lesson", back_populates="quiz")
    questions: Mapped[list["Question"]] = relationship("Question", back_populates="quiz", cascade="all, delete-orphan")
    attempts: Mapped[list["Attempt"]] = relationship("Attempt", back_populates="quiz")

class Question(Base):
    __tablename__ = "questions"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    quiz_id: Mapped[str] = mapped_column(String, ForeignKey("quizzes.id"))
    type: Mapped[str] = mapped_column(String)
    text: Mapped[str] = mapped_column(String)
    options: Mapped[dict] = mapped_column(JSON, default=list)
    correct_answer: Mapped[dict] = mapped_column(JSON, default=dict)
    quiz: Mapped["Quiz"] = relationship("Quiz", back_populates="questions")

class Attempt(Base):
    __tablename__ = "attempts"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"))
    quiz_id: Mapped[str] = mapped_column(String, ForeignKey("quizzes.id"))
    status: Mapped[str] = mapped_column(SQLEnum(AttemptStatus), default=AttemptStatus.IN_PROGRESS)
    score: Mapped[float] = mapped_column(Float, nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    user: Mapped["User"] = relationship("User", back_populates="attempts")
    quiz: Mapped["Quiz"] = relationship("Quiz", back_populates="attempts")