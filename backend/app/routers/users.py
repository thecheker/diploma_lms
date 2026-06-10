from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.models import Attempt, AttemptStatus, Quiz, Lesson, Course, User
from app.schemas import MyCourseOut
from app.deps import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me/courses", response_model=list[MyCourseOut])
def get_my_courses(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    attempts = db.query(Attempt).filter(
        Attempt.user_id == user.id
    ).options(
        joinedload(Attempt.quiz).joinedload(Quiz.lesson).joinedload(Lesson.course)
    ).all()
    
    course_data = {}
    for attempt in attempts:
        if not attempt.quiz or not attempt.quiz.lesson:
            continue
        lesson = attempt.quiz.lesson
        course = lesson.course
        
        if course.id not in course_data:
            course_data[course.id] = {"course": course, "completed_lessons": set(), "last_lesson_id": lesson.id}
        
        if attempt.status in [AttemptStatus.COMPLETED, AttemptStatus.AUTO_GRADED]:
            course_data[course.id]["completed_lessons"].add(lesson.id)
        course_data[course.id]["last_lesson_id"] = lesson.id
    
    result = []
    for course_id, data in course_data.items():
        course = data["course"]
        total = len(course.lessons) if course.lessons else 1
        completed = len(data["completed_lessons"])
        progress = min(100.0, round((completed / total) * 100, 1))
        
        result.append(MyCourseOut(
            course_id=course.id,
            course_title=course.title,
            course_image=course.image,
            category=course.category,
            completed=progress >= 100,
            last_lesson_id=data["last_lesson_id"],
            progress_percent=progress
        ))
    return result