from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import Optional
from app.database import get_db
from app.models import Course, Lesson, Quiz, Question, Role, User, CourseCategory
from app.schemas import CourseCreate, CourseOut
from app.deps import get_current_user

router = APIRouter(prefix="/courses", tags=["courses"])

def check_course_access(user: User, course: Course) -> bool:
    if user.role == Role.ADMIN:
        return True
    if user.role == Role.INSTRUCTOR and course.instructor == user.email:
        return True
    return False

@router.get("", response_model=list[CourseOut])
def list_courses(
    db: Session = Depends(get_db),
    category: Optional[CourseCategory] = Query(None)
):
    query = db.query(Course).options(
        joinedload(Course.lessons).joinedload(Lesson.quiz)
    )
    if category:
        query = query.filter(Course.category == category)
    return query.all()

@router.get("/{course_id}", response_model=CourseOut)
def get_course(course_id: str, db: Session = Depends(get_db)):
    course = db.query(Course).options(
        joinedload(Course.lessons).joinedload(Lesson.quiz)
    ).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(404, detail="Course not found")
    return course

@router.post("", response_model=CourseOut)
def create_course(
    payload: CourseCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    if user.role not in [Role.INSTRUCTOR, Role.ADMIN]:
        raise HTTPException(403, detail="Only instructors can create courses")
    
    course = Course(
        title=payload.title,
        description=payload.description or "",
        instructor=payload.instructor or user.email,
        image=payload.image or "",
        category=payload.category or CourseCategory.OTHER
    )
    db.add(course)
    db.flush()

    for i, lesson_data in enumerate(payload.lessons or []):
        lesson = Lesson(
            course_id=course.id,
            title=lesson_data.title or "",
            lesson_type=lesson_data.lesson_type or "TEXT",
            content=lesson_data.content,
            order_index=i
        )
        db.add(lesson)
        db.flush()
        
        if lesson_data.quiz:
            quiz = Quiz(
                lesson_id=lesson.id,
                title=lesson_data.quiz.title,
                time_limit_sec=lesson_data.quiz.time_limit_sec,
                passing_score=lesson_data.quiz.passing_score,
                creator_id=user.id
            )
            db.add(quiz)
            db.flush()
            
            for q_data in lesson_data.quiz.questions:
                db.add(Question(
                    quiz_id=quiz.id,
                    type=q_data.type,
                    text=q_data.text,
                    options=q_data.options,
                    correct_answer=q_data.correct_answer
                ))

    db.commit()
    db.refresh(course)
    return course

@router.put("/{course_id}", response_model=CourseOut)
def update_course(
    course_id: str,
    payload: CourseCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(404, detail="Course not found")
    if not check_course_access(user, course):
        raise HTTPException(403, detail="You can only edit your own courses")
    
    course.title = payload.title
    course.description = payload.description or ""
    course.instructor = payload.instructor or course.instructor
    course.image = payload.image or ""
    course.category = payload.category or course.category
    
    db.commit()
    db.refresh(course)
    return course

@router.delete("/{course_id}")
def delete_course(
    course_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(404, detail="Course not found")
    
    if not check_course_access(user, course):
        raise HTTPException(403, detail="You can only delete your own courses")
    
    db.delete(course)
    db.commit()
    return {"message": "Course deleted successfully", "id": course_id}