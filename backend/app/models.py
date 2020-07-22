from .extensions import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    idade = db.Column(db.Integer, default=0)

    password_hash = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean, default=False)

    posts = db.relationship('Post', backref='owner')

    def json(self):
        user_json = {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'idade': self.idade
        }
        return user_json

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), default='')
    img = db.Column(db.String(200), default='')

    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def json(self):

        return {'id': self.id,
                'text': self.text,
                'img': self.img,
                'owner': self.owner.json()}
