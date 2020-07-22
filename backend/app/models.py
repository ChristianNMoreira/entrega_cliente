from .extensions import db

#flask db migrate & flask db upgrade
#Mudanças nas tabelas User e Post, criação da tabela Comment

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    idade = db.Column(db.Integer, default=0)
    #img = db.Column(db.String(200), default='')

    password_hash = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean, default=False)

    posts = db.relationship('Post', backref='owner')

    comments = db.relationship('Comment', backref='c_owner')

    def json(self):
        user_json = {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'idade': self.idade
        }
        return user_json

#POST COM DATA (?)
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), default='')
    img = db.Column(db.String(200), default='')
    #date = db.Column(db.String(30))

    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    comments = db.relationship('Comment', backref='owner')

    def json(self):

        return {'id': self.id,
                'text': self.text,
                'img': self.img,
                #'date': self.date,
                'owner': self.owner.json()}

#COMENTÁRIO COM DATA (?)
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    #date = db.Column(db.String(30))
    
    #user_id = db.Column(db.Integer, nullable=False)

    owner_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def json(self):

        return {'id': self.id,
                'text': self.text,
                #'date': self.date,
                #'user_id': self.user_id,
                'user': self.c_owner.json(),
                'owner': self.owner.json()}