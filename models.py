from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login import UserMixin
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager


app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

migrate = Migrate(app, db, render_as_batch=True)
manager = Manager(app)
manager.add_command('db', MigrateCommand)




class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    notes = db.relationship('Note', backref='user')


class Note(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    information = db.Column(db.String, nullable=False)
    color = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # num = db.Column(db.Integer)     >>>> I removes it by Flask-migrate and Flask-script



def insert_user(user):

    db.session.add(user)
    db.session.commit()


def insert_note(note):

    db.session.add(note)
    db.session.commit()


def delete_note(note):

    db.session.delete(note)
    db.session.commit()


# db.create_all()
if __name__ == "__main__":
    manager.run()

