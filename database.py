from flask_sqlalchemy import SQLAlchemy

# Initialize DB object here so it can be imported elsewhere
db = SQLAlchemy()

class Round(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_flips = db.Column(db.Integer, nullable=False)
    max_dist = db.Column(db.Integer, nullable=False)
    max_h_streak = db.Column(db.Integer, nullable=False)
    max_t_streak = db.Column(db.Integer, nullable=False)
    max_h_timestamp = db.Column(db.Integer, nullable=False, default=0)
    max_t_timestamp = db.Column(db.Integer, nullable=False, default=0)
    is_active = db.Column(db.Boolean, default=True, nullable=False)