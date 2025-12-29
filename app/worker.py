from celery import Celery
from datetime import datetime
from .models import ActivationToken, PasswordResetToken, RefreshToken
from .database import SessionLocal

celery_app = Celery("worker", broker="redis://redis:6379/0")

@celery_app.task
def cleanup_expired_tokens():
    db = SessionLocal()
    try:
        now = datetime.utcnow()
        db.query(ActivationToken).filter(ActivationToken.expires_at < now).delete()
        db.query(PasswordResetToken).filter(PasswordResetToken.expires_at < now).delete()
        db.query(RefreshToken).filter(RefreshToken.expires_at < now).delete()
        db.commit()
    finally:
        db.close()

celery_app.conf.beat_schedule = {
    "cleanup-every-hour": {
        "task": "app.worker.cleanup_expired_tokens",
        "schedule": 3600.0,
    },
}
