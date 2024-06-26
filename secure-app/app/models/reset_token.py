import uuid
from app.db import db
from datetime import datetime

class ResetToken(db.Model):
    id = db.Column(db.String, primary_key=True,default=lambda: str(uuid.uuid4()))
    token = db.Column(db.String(100), unique=True, nullable=False)
    used = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)