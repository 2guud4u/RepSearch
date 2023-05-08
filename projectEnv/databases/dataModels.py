from app import db

class Product(db.Model):
    
    post_id = db.Column(db.String(50), primary_key=True)
    score = db.Column(db.Integer)
    date_updated = db.Column(db.Time)
    title = db.Column(db.String(50))
    url = db.Column(db.String(100))

    # def __repr__(self):
    #     return '<post %r>' % self.post_id

