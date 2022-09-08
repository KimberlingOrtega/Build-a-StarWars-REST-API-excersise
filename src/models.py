from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorites = db.relationship("Favorite", backref="user", uselist=True)
    
    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
        
class People(db.Model):
    # __tablename__ = 'personajes'
    id = db.Column(db.Integer,primary_key=True)  
    name = db.Column(db.String(150), nullable=False)
    url = db.Column(db.String(250), nullable=False)
    
   
    def serialize(self):
        return{
            "id": self.id,
            'uid': self.uid,
            "name": self.name,
            "url": self.url,
            
        }
        
class Planets(db.Model):
    # __tablename__ ='planetas'
    id = db.Column(db.Integer,primary_key=True)  
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    favorite_planet_id = db.Column(db.Integer,nullable=False )
    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }     
        
class Favorite(db.Model):
    # __tablename__ = 'personajes_favoritos'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    url = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    __table_args__ =(db.UniqueConstraint(
        'user_id', 
        'url',
        name = 'unique_favorite'
    ),)
    # character_id = db.Column(db.Integer, db.ForeignKey('character.id')
    def serialize(self):
        return{
           "id": self.id,
           "user_id": self.user_id,
           "url": self.url,
           'favorite_name': self.name,  
           
        }
        
    def delete(self):
        db.session.delete(self)
        try:
            db.session.commit()
            return True
        except Exception as error:
            db.session.rollback()
            return False       
    
    
