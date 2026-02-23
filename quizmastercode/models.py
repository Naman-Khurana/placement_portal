from .extensions import db
from .enums.role import RoleEnum 
from datetime import datetime,date
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "user"
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(100),nullable=False,unique=True)
    password_hash=db.Column(db.String(255),nullable=False)
    name=db.Column(db.String(100),nullable=False)
    qualification=db.Column(db.String(100))
    dob=db.Column(db.Date)
    role=db.Column(db.String(20),nullable=False,default=RoleEnum.USER.value)
    scores=db.relationship(
        "Scores",
        back_populates="user",
        cascade="all,delete-orphan"
    )
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Subject(db.Model):
    __tablename__ = "subject"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False,unique=True)
    description=db.Column(db.String(500))
    chapters=db.relationship(
        "Chapter",
        back_populates="subject"
    )


class Chapter(db.Model):
    __tablename__ = "chapter"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    description=db.Column(db.String(500))
    quizzes=db.relationship(
        "Quiz",
        back_populates="chapter"
    )
    subject_id=db.Column(
        db.Integer,
        db.ForeignKey("subject.id"),
        nullable=False,
        index=True
    )
    subject=db.relationship(
        "Subject",
        back_populates="chapters"
    )


class Quiz(db.Model):
    __tablename__ = "quiz"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    date_of_quiz=db.Column(db.Date,nullable=False,default=date.today)
    time_duration=db.Column(db.Time,nullable=False)
    description=db.Column(db.String(500))
    remarks=db.Column(db.String(200))
  
    chapter_id=db.Column(
        db.Integer,
        db.ForeignKey("chapter.id"),
        nullable=False,
        index=True
    )
    chapter=db.relationship("Chapter",back_populates="quizzes")
     
   
    scores=db.relationship(
        "Scores",
        back_populates="quiz",
        cascade="all,delete-orphan"
    )



class Scores(db.Model):
    __tablename__ = "scores"
    id=db.Column(db.Integer,primary_key=True)

    user_id=db.Column(db.Integer, db.ForeignKey("user.id"),nullable=False,index=True)
    quiz_id=db.Column(db.Integer, db.ForeignKey("quiz.id"),nullable=False,index=True)

    time_stamp_of_attempt=db.Column(db.DateTime,default=datetime.utcnow,nullable=False)
    total_scored=db.Column(db.Integer,nullable=False)

    user=db.relationship("User", back_populates="scores")
    quiz=db.relationship("Quiz",back_populates="scores")

