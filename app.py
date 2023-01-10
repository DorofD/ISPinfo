from flask import Flask, render_template, url_for, request, flash, session, redirect, abort, g, make_response
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
import dbscripts as db


app = Flask(__name__)
app.config['SECRET_KEY'] = 'aboba1488'
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return db.UserLogin().fromDB(user_id)


@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index.html', class1='active', class2='', class3='', class4='', user=session['username'], usertype=session['usertype'])
    else:
        return render_template('login.html')


@app.route('/search', methods=(['POST']))
def search():
    if request.form['searchType'] == 'pid':
        result = db.get_contracts_pid(request.form['pid'])
    elif request.form['searchType'] == 'shop':
        result = db.get_contracts_shop(request.form['shop'])
    return render_template('searchResult.html', result=result, result_len=len(result), class1='active', class2='', class3='', class4='', user=session['username'], usertype=session['usertype'])


@app.route('/application/<id>', methods=(['POST']))
def application(id):
    result = db.get_contract_id(id)
    return render_template('application.html', result=result, class1='active', class2='', class3='', class4='', user=session['username'], usertype=session['usertype'])


@app.route('/update', methods=('GET', 'POST'))
def update():
    if current_user.is_authenticated:
        if request.method == 'POST':
            file = request.files['file']
            if file and db.db_update(file):
                flash('Импорт успешно выполнен', category='success')
            else:
                flash('Импорт не выполнен', category='error')
        return render_template('update.html', class1='', class2='active', class3='', class4='', user=session['username'], usertype=session['usertype'])
    else:
        return render_template('login.html')


@app.route('/about')
def about():
    if current_user.is_authenticated:
        return render_template('about.html', class1='', class2='', class3='active', class4='', user=session['username'], usertype=session['usertype'])
    else:
        return render_template('login.html')


@app.route('/usermgmt')
def usermgmt():
    # if request.method == 'POST':
    #     if request.form['delete']:
    #         print('User delete')
    #         return render_template('usermgmt.html', result = result, result_len = len(result), class1 = '', class2 = '', class3 = '', class4 = 'active', user = session['username'])
    #     elif request.form['add']:
    #         print('user add')
    #         return render_template('usermgmt.html', result = result, result_len = len(result), class1 = '', class2 = '', class3 = '', class4 = 'active', user = session['username'])

    if current_user.is_authenticated:
        result = db.getAllUsers()
        return render_template('usermgmt.html', result=result, result_len=len(result), class1='', class2='', class3='', class4='active', user=session['username'], usertype=session['usertype'])
    else:
        return render_template('login.html')


@app.route('/deleteuser/<id>', methods=(['POST']))
def deleteuser(id):
    db.deleteUser(id)
    print('User delete')
    result = db.getAllUsers()
    return render_template('usermgmt.html', result=result, result_len=len(result), class1='', class2='', class3='', class4='active', user=session['username'], usertype=session['usertype'])


@app.route('/adduser', methods=(['POST']))
def adduser():
    db.adduser(request.form['username'],
               request.form['usertype'], request.form['auth'])
    result = db.getAllUsers()
    return render_template('usermgmt.html', result=result, result_len=len(result), class1='', class2='', class3='', class4='active', user=session['username'], usertype=session['usertype'])


@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        user = db.login(request.form['login'], request.form['password'])
        if user:
            userlogin = db.UserLogin().create(user)
            session['username'] = request.form['login']
            session['usertype'] = user[3]
            login_user(userlogin)
            return redirect(url_for('index'))
        else:
            flash('Не удалось войти', category='wrongpass')
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
