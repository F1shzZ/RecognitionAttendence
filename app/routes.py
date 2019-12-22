from flask import *
import flask_login as fl
from flask_login import login_required
import userdb as db
import json
from app import app
#import app.ownFunctions as run
import base64

login_manager = fl.LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.User.objects.get(username=user_id)


@app.route('/')
@app.route('/success!')
@app.route('/loggedout')
def login():
    if fl.current_user.is_authenticated:
        return redirect('/home')
    else:
        return render_template('login.html', error='')


@app.route('/loginfail')
def loginFailed():
    return render_template('login.html', error='Login failed: Username or password incorrect')


@app.route('/signup')
def signup():
    if fl.current_user.is_authenticated:
        return redirect('/home')
    else:
        return render_template('signup.html', error='')


@app.route('/signupfail', methods=['POST'])
def checksignup():
    if db.user_search_i(request.form['username']):
        return render_template('signup.html', error='Username already taken')
    elif request.form['password'] != request.form['confirmpassword']:
        return render_template('signup.html', error='Passwords do not match')
    else:
        db.registerUser(request.form['username'], request.form['password'])
        return redirect('/success!')


@app.route('/authorization', methods=['POST'])
def authorize():
    user = db.authenticate(request.form['username'], request.form['password'])
    if user:
        fl.login_user(user)
        return redirect('/home')
    else:
        return redirect('/loginfail')


@app.route('/home')
@login_required
def home():
    # Turn mongodb document into json
    classrooms = fl.current_user.get_classes()
    json_serializable_object = []
    for classroom in classrooms:
        classroom_info = {}
        classroom_info['class_code'] = classroom.class_code
        classroom_info['num_students'] = len(classroom.class_list)
        json_serializable_object.append(classroom_info)
    classroom_json = json.dumps(json_serializable_object)

    return render_template('home.html', user=fl.current_user.get_id(), classrooms=classroom_json)


@app.route('/logout')
@login_required
def logout():
    fl.current_user.logout()
    fl.logout_user()
    return redirect('/loggedout')


@app.route('/create')
@login_required
def create():
    return render_template('create.html', error='')


@app.route('/creating', methods=['POST'])
@login_required
def creating():
    class_error = db.addClass(request.form['class_code'], fl.current_user.get_id())
    if class_error is None:
        return redirect('/home')
    else:
        return render_template('create.html', error=class_error)


@app.route('/class_home', methods=['POST'])
@login_required
def class_home():
    return redirect('/' + request.form['classroom'])


@app.route('/<class_code>')
@login_required
def class_home_redirect(class_code):
    if db.class_search(class_code, db.user_search(fl.current_user.get_id())):
        return render_template('class_home.html', class_code=class_code)
    else:
        return abort(404, 'We caught you red handed manually entering the url, nice try tho')


@app.route('/<class_code>/<action>')
@login_required
def class_attendance(class_code, action):
    print(class_code)
    print(action)
    if action == 'attendance':
        pass
    elif action == 'people':

        class_list = db.class_search(class_code, db.user_search(fl.current_user.get_id())).class_list

        # Turn mongodb document into json
        json_serializable_object = []
        for student in class_list:
            student_info = {}
            student_info['first'] = student.first_name
            student_info['last'] = student.last_name
            student_info['id'] = student.id
            json_serializable_object.append(student_info)
        classlist_json = json.dumps(json_serializable_object)

        return render_template('class_attendance', class_code=class_code, class_list=classlist_json)

    elif action == 'settings':
        pass
    else:
        return abort(404, 'Wtf is %s, lmao, good effort for trying to find bugs :)' % action)


@app.route('/capture')
def capture():
    return render_template('capture.html')

@app.route('/search')
def search():
    dataURL = request.args.get('dataURL')
    data = dataURL.split(',')[1]
    with open("app/static/img/image.png", "wb") as fh:
        fh.write(base64.b64decode(data))
        fh.close()
    #result = run.searchName('Family','app/static/img/image.png')
    return jsonify(result='Not available')


@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/add')
def add():
    dataURL = request.args.get('dataURL')
    name = request.args.get('name')
    data = dataURL.split(',')[1]
    with open("app/static/img/image.png", "wb") as fh:
        fh.write(base64.b64decode(data))
        fh.close()
    #result = run.addFace('Family','app/static/img/image.png',name)
    #return jsonify(result=result)
    return jsonify(result='Not available')


@app.route('/delete')
def delete():
    return render_template('delete.html')

@app.route('/deleteFace')
def deleteFace():
    dataURL = request.args.get('dataURL')
    data = dataURL.split(',')[1]
    with open("app/static/img/image.png", "wb") as fh:
        fh.write(base64.b64decode(data))
        fh.close()
    #result = run.deleteByImg('Family','app/static/img/image.png')
    return jsonify(result='Not available')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', error=error)


# <label>Add students</label><input placeholder="First,Last:First,Last" type="text" name="class_list">

'''
names = request.form['class_list'].split(':')
    for name in names:
        firstlast = name.split(',')
        first = firstlast[0]
        last = firstlast[1]
    name_error = first == '' or last == '' or first[0].islower() or last[0].islower()

    if name_error == True:
        return render_template('create.html', error='Please look over the student names!')
        db.addStudent(first, last, request.form['class_code'], fl.current_user.get_id())
'''

app.secret_key = 'wtf is this'