from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from datetime import datetime
from app.database import get_db
from app.models import Attempt, AttemptStatus, User, Quiz, Lesson, Course
from app.schemas import AttemptSubmit, AttemptOut
from app.deps import get_current_user

router = APIRouter(prefix="/attempts", tags=["attempts"])

@router.post("/{attempt_id}/submit", response_model=AttemptOut)
def submit_attempt(
    attempt_id: str,
    payload: AttemptSubmit,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    attempt = db.query(Attempt).filter(
        Attempt.id == attempt_id, Attempt.user_id == user.id
    ).first()
    
    if not attempt:
        raise HTTPException(404, detail="Attempt not found")
    if attempt.status != AttemptStatus.IN_PROGRESS:
        raise HTTPException(400, detail="Already submitted")

    quiz = attempt.quiz
    if not quiz:
        raise HTTPException(404, detail="Quiz not found")
    
    elapsed = (datetime.utcnow() - attempt.started_at).total_seconds()
    if quiz.time_limit_sec > 0 and elapsed > quiz.time_limit_sec:
        attempt.score = 0.0
        attempt.status = AttemptStatus.COMPLETED
        attempt.finished_at = datetime.utcnow()
        db.commit()
        db.refresh(attempt)
        return attempt

    questions = {q.id: q for q in quiz.questions}
    total_correct = 0.0
    
    for ans in payload.answers:
        q = questions.get(ans.question_id)
        if not q:
            continue
        user_set = set(ans.user_answer.get("selected_ids", []))
        correct_set = set(q.correct_answer.get("ids", []) if q.correct_answer else [])
        if user_set == correct_set:
            total_correct += 1.0

    attempt.score = total_correct / len(questions) if questions else 0.0
    attempt.status = AttemptStatus.AUTO_GRADED if attempt.score >= quiz.passing_score else AttemptStatus.COMPLETED
    attempt.finished_at = datetime.utcnow()
    
    db.commit()
    db.refresh(attempt)
    return attempt

@router.get("/my", response_model=list[dict])
def get_my_attempts(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    attempts = db.query(Attempt).filter(
        Attempt.user_id == user.id
    ).options(
        joinedload(Attempt.quiz).joinedload(Quiz.lesson).joinedload(Lesson.course)
    ).order_by(Attempt.started_at.desc()).all()
    
    return [
        {
            "id": a.id,
            "quiz_id": a.quiz_id,
            "quiz_title": a.quiz.title if a.quiz else "Unknown",
            "course_title": a.quiz.lesson.course.title if a.quiz and a.quiz.lesson and a.quiz.lesson.course else "Unknown",
            "status": a.status,
            "score": a.score,
            "started_at": a.started_at,
            "finished_at": a.finished_at
        }
        for a in attempts
    ]

@router.post("/quiz/{quiz_id}/retry", response_model=AttemptOut)
def retry_quiz(quiz_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(404, detail="Quiz not found")
    
    attempt = Attempt(user_id=user.id, quiz_id=quiz_id)
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return attempt