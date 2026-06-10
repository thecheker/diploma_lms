from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models import Role, AttemptStatus, LessonType, QuestionType, CourseCategory

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    role: Role = Role.STUDENT

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: str
    email: str
    role: Role
    model_config = {"from_attributes": True}

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class QuestionCreate(BaseModel):
    type: QuestionType
    text: str
    options: List[Dict] = []
    correct_answer: Dict[str, Any] = {"ids": []}

class QuizCreate(BaseModel):
    title: str = "Тест к уроку"
    time_limit_sec: int = 600
    passing_score: float = 0.7
    questions: List[QuestionCreate] = []

class LessonCreate(BaseModel):
    title: str
    lesson_type: LessonType = LessonType.TEXT
    content: Dict[str, Any] = {}
    order_index: int = 0
    quiz: Optional[QuizCreate] = None

class CourseCreate(BaseModel):
    title: str
    description: str = ""
    instructor: str = ""
    image: str = ""
    category: CourseCategory = CourseCategory.OTHER
    lessons: List[LessonCreate] = []

class QuestionOut(BaseModel):
    id: str
    type: QuestionType
    text: str
    options: Optional[List[Dict]] = None
    model_config = {"from_attributes": True}

class LessonOut(BaseModel):
    id: str
    title: str
    lesson_type: LessonType
    content: Dict
    order_index: int
    quiz: Optional["QuizOut"] = None
    model_config = {"from_attributes": True}

class CourseOut(BaseModel):
    id: str
    title: str
    description: str
    instructor: str
    image: str
    category: CourseCategory = CourseCategory.OTHER
    lessons: List[LessonOut] = []
    created_at: Optional[datetime] = None
    model_config = {"from_attributes": True}

class QuizOut(BaseModel):
    id: str
    title: str
    time_limit_sec: int
    passing_score: float
    questions: List[QuestionOut] = []
    lesson_id: str
    creator_id: Optional[str] = None
    model_config = {"from_attributes": True}

class AnswerSubmit(BaseModel):
    question_id: str
    user_answer: Dict[str, Any]

class AttemptSubmit(BaseModel):
    answers: List[AnswerSubmit]

class AttemptOut(BaseModel):
    id: str
    quiz_id: str
    status: AttemptStatus
    score: Optional[float] = None
    started_at: datetime
    finished_at: Optional[datetime] = None
    model_config = {"from_attributes": True}

class MyCourseOut(BaseModel):
    course_id: str
    course_title: str
    course_image: str
    category: str
    completed: bool
    last_lesson_id: Optional[str] = None
    progress_percent: float = 0.0
    model_config = {"from_attributes": True}