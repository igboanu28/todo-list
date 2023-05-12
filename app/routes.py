from app import app,db
from werkzeug.urls import url_parse
from flask import render_template,request,url_for,redirect,flash
from app.models import Task, User
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PasswordForm
from flask_login import login_user, logout_user, current_user,login_required



@app.get('/')
@app.get('/index')
@login_required
def index():
    todo_list=Task.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html',todo_list=todo_list)

@app.post('/add')
def add():
    name=request.form.get("name")
    if not name:
        flash('Must fill in!!!')
        return redirect(url_for("index"))
    user = current_user.id
    new_task=Task(name=name,user_id=user,complete=False)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for("index"))

@app.get('/update/<int:todo_id>')
def update(todo_id):
    todo=Task.query.get(todo_id)
    todo.complete=not todo.complete
    db.session.commit()
    return redirect(url_for("index"))

@app.get('/delete/<int:todo_id>')
def delete(todo_id):
    todo=Task.query.get(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.get('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def user_password_change():
    form = PasswordForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user: User = User.query.get(current_user.id)
            user.set_password(form.password.data)
            db.session.commit()
            flash ('Password has been updated!')
        # else:
        #     for error in form.errors:
        #         for err in form.errors[error]:
        #             flash (err)
            # return redirect(url_for('user.user_profile'))
    return render_template('create_password.html', form=form)

