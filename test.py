from flask import Flask, flash, render_template, jsonify
from flask_login import (LoginManager, current_user,
                         login_required, login_user, logout_user)
import mongo as db

app = Flask(__name__)

app.config['SECRET_KEY'] = 'itssecretkey'

loginManager = LoginManager()
loginManager.init_app(app)


@loginManager.user_loader
def load_user(user_id):
    print('\n\nLOAD USER', type(user_id), user_id)
    user = db.getFromId(user_id)
    if type(user) == str:
        return None
    return user


@app.route('/loginA')
def loginA():
    if current_user.is_authenticated:
        logout_user()
    print('authenticate')
    user = db.authenticate('a', 'a')
    if type(user) == str:
        return 'user is not available'
    login_user(user)
    return 'you are now logged in as   ' + user.username


@app.route('/loginB')
def loginB():
    if current_user.is_authenticated:
        logout_user()
    print('authenticate')
    user = db.authenticate('b', 'b')
    if type(user) == str:
        return 'user is not available'
    login_user(user)
    return 'you are now logged in as   ' + user.username


@app.route('/loginC')
def loginC():
    if current_user.is_authenticated:
        logout_user()
    print('authenticate')
    user = db.authenticate('c', 'c')
    if type(user) == str:
        return 'user is not available'
    login_user(user)
    return 'you are now logged in as   ' + user.username


# final version to check user login status
# see useAjax.html for details
@app.route('/useAjax')
def useAjax():
    return render_template('useAjax.html')


@app.route('/checkStatus')
def checkStatus():
    if current_user.is_authenticated:
        return jsonify(status='loged in as   ', currentUser=current_user.username)
    else:
        return jsonify(status='user is loged out')


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
