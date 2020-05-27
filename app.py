from flask import Flask, flash, redirect, render_template, url_for, request, jsonify
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from forms import Log_in_form, Sign_up_form, New_note, Edit_user, Edit_note
from werkzeug.security import generate_password_hash, check_password_hash
from models import app, db, User, Note, insert_note, insert_user, delete_note
from flask_mail import Mail, Message
    

mail = Mail(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/')
def home():
  
    return render_template('home.html', user = current_user)


@app.route('/login/', methods=["GET", "POST"])
def log_in():
    if current_user.is_authenticated:
        return redirect(url_for('user_bag', user_id=current_user.id))

    form = Log_in_form()
    if request.method == "POST" and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
  
            return redirect(url_for('user_bag', user_id=user.id))

        flash("This is not a valid account")
        return redirect(url_for('log_in'))

    return render_template('login.html', form=form)


@app.route('/signup/', methods=["GET", "POST"])
def sign_up():
   
    if current_user.is_authenticated:
        return redirect(url_for('user_bag', user_id=current_user.id))

    form = Sign_up_form()
    if request.method == "POST" and form.validate_on_submit():
        email = form.email.data
        name = request.form['name']
        password = form.password.data
        user = User.query.filter_by(email=email).first()

        if user:
            flash("This email is already exists")
            return redirect(url_for('sign_up'))

        new_user = User(email=email, name=name, password=generate_password_hash(password))
        insert_user(new_user)
        msg = Message("Hi there", recipients=[new_user.email])
        msg.html = """<h1 style='color:green'>Hello in write&Note</h1>
                        <h2>Write&Note website will help you record your notes
                            in a wonderful way ..let's start now! Happy trip.</h2><br>
                            <img src='{{ url_for('static', filename='write1.jpg') }}'>""" 
        # with app.open_resource("write1.jpg") as img:
        #     msg.attach('write1.jpg', 'image/jpeg', img.read())
        mail.send(msg)

        login_user(User.query.filter_by(email=email).first())
        return redirect(url_for('user_bag', user_id=new_user.id))

    return render_template('signup.html', form=form)


@app.route("/logout/")
@login_required
def logout():

    logout_user()
    return redirect(url_for('home'))


@app.route('/user/<int:user_id>/', methods=["GET", "POST"])
@login_required
def user_bag(user_id):

    form = New_note()
    user = User.query.filter_by(id=user_id).first()
    notes = Note.query.filter_by(user_id=user.id).all()

    if request.method == "POST":
        information = form.information.data
        color = request.form['color']
        new_note = Note(information=information, color=color, user_id=user.id)
        insert_note(new_note)
        return redirect(url_for('user_bag', user_id=user.id))

    return render_template('user_bag.html', user = user, form=form, notes=notes)


@app.route('/user/<int:user_id>/useraccount/', methods=["GET", "POST"])
@login_required
def user_account(user_id):

    user = User.query.filter_by(id=user_id).first()
    form = Edit_user()
    if request.method == "POST":
        name = request.form['name']
        user.name = name
        db.session.commit()
        return redirect(url_for('user_bag', user_id=user.id))

    return render_template('user_account.html', form=form, user=user)


@app.route('/user/<int:user_id>/note/<note_id>')
def note(user_id, note_id):

    user = User.query.filter_by(id=user_id).first()
    note = Note.query.filter_by(id=note_id, user_id=user.id).first()

    return render_template('note_bag.html', user=user, note=note)


@app.route('/user/<int:user_id>/note/<int:note_id>/edit/', methods=["GET", "POST"])
def edit_note(user_id, note_id):

    user = User.query.filter_by(id=user_id).first()
    note = Note.query.filter_by(id=note_id, user_id=user.id).first()
    note_information = Note.query.filter_by(id=note_id, user_id=user.id).first().information
    form = Edit_note()
    if request.method == "POST":
        information = request.form['information']
        color = request.form['color']
        note.information = information
        note.color = color
        db.session.commit()
        return redirect(url_for('user_bag', user_id=user.id))

    return render_template('edit_note.html', user=user, note=note, form=form)


@app.route('/user/<int:user_id>/note/<int:note_id>/delete/', methods=["GET", "POST"])
def delete__note(user_id, note_id):

    user = User.query.filter_by(id=user_id).first()
    note = Note.query.filter_by(id=note_id, user_id=user_id).first()
    if request.method == "POST":
        delete_note(note)
        return redirect(url_for('user_bag', user_id=user.id))

    return render_template('delete_note.html', note=note, user=user)


@app.route('/users/api/')
def users():

    if current_user.email == "mohamedkholeef082@gmail.com":
        users = User.query.all()
        users_ls = []
        for user in users:
            users_ls.append({"email": user.email, " name": user.name})
        return jsonify({"users": users_ls})

    else:
        return "badddd"


if __name__ == "__main__":

    app.run(debug=app.config['DEBUG'])