from flask import Flask, flash, render_template
from flask_login import (LoginManager, UserMixin,
                         current_user, login_required, login_user, logout_user)
from mongoengine import Document, connect, StringField

app = Flask(__name__)

app.config['SECRET_KEY'] = 'itssecretkey'

login_manager = LoginManager()
login_manager.init_app(app)

connect('test_object')

# message = 'original'


class User(Document, UserMixin):
    name = StringField(unique=True)


@login_manager.user_loader
def load_user(user_id):
    print('LOAD USER', type(user_id), user_id)
    return User.objects(id=user_id).first()


@app.route('/')
@app.route('/login')
def index():
    print('login')
    user = User.objects(name='testObject').first()
    login_user(user)
    return 'you are now logged in'


@app.route('/home')
@login_required
def home():
    return 'the current user is ' + current_user.name


@app.route('/test')
@login_required
def test():
    flash('flashed message')
    return render_template('test2.html')


# not using @login required

# sustomize login status check

# check status every second
# if not loged in then display "not logged in"
# if logged in then displat "already logged in"
@app.route('/test2')
def test2():
    if not current_user.is_authenticated:
        flash('not loged in')
    else:
        flash("already logged in")
    return render_template('test2.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    # message = 'flash message now'
    flash('flashed message')
    # print(message)
    return render_template('test.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
