from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.models import Quiz, Question, Lesson, Course, Role, User, Attempt
from app.schemas import QuizOut, QuizCreate
from app.deps import get_current_user

router = APIRouter(prefix="/quizzes", tags=["quizzes"])

def check_quiz_access(user: User, quiz: Quiz, db: Session) -> bool:
    if user.role == Role.ADMIN:
        return True
    if user.role == Role.INSTRUCTOR and quiz.lesson and quiz.lesson.course:
        return quiz.lesson.course.instructor == user.email
    return False

@router.get("/{quiz_id}", response_model=QuizOut)
def get_quiz(quiz_id: str, db: Session = Depends(get_db)):
    quiz = db.query(Quiz).options(joinedload(Quiz.questions)).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(404, detail="Quiz not found")
    return quiz

@router.put("/{quiz_id}", response_model=QuizOut)
def update_quiz(
    quiz_id: str,
    payload: QuizCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    quiz = db.query(Quiz).options(
        joinedload(Quiz.lesson).joinedload(Lesson.course)
    ).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(404, detail="Quiz not found")

    if not check_quiz_access(user, quiz, db):
        raise HTTPException(403, detail="You can only edit quizzes for your courses")
    
    quiz.title = payload.title
    quiz.time_limit_sec = payload.time_limit_sec
    quiz.passing_score = payload.passing_score
    
    db.query(Question).filter(Question.quiz_id == quiz.id).delete()
    for q_data in payload.questions:
        db.add(Question(
            quiz_id=quiz.id,
            type=q_data.type,
            text=q_data.text,
            options=q_data.options,
            correct_answer=q_data.correct_answer or {"ids": []}
        ))
    
    db.commit()
    db.refresh(quiz)
    return quiz

@router.delete("/{quiz_id}")
def delete_quiz(
    quiz_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    quiz = db.query(Quiz).options(
        joinedload(Quiz.lesson).joinedload(Lesson.course)
    ).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(404, detail="Quiz not found")

    if not check_quiz_access(user, quiz, db):
        raise HTTPException(403, detail="You can only delete quizzes for your courses")
    
    db.query(Question).filter(Question.quiz_id == quiz.id).delete()
    db.delete(quiz)
    db.commit()
    return {"message": "Quiz deleted"}

@router.post("/{quiz_id}/start", response_model=dict)
def start_quiz_attempt(quiz_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(404, detail="Quiz not found")
    
    attempt = Attempt(user_id=user.id, quiz_id=quiz_id)
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    
    questions = [
        {"id": q.id, "type": q.type, "text": q.text, "options": q.options}
        for q in quiz.questions
    ]
    
    return {
        "attempt_id": attempt.id,
        "quiz_id": quiz.id,
        "title": quiz.title,
        "time_limit_sec": quiz.time_limit_sec,
        "questions": questions
    }