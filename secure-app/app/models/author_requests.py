import uuid
from app.db import db

class AuthorRequests(db.Model):
    id = db.Column(db.String, primary_key=True,default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String,db.ForeignKey('user.id'),nullable=False)
    status = db.Column(db.String(50), default='InProgress')

    def __repr__(self):
        return f'<RoleRequest {self.id} - {self.user_id} - {self.status}>'