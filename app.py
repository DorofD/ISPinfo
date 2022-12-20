from flask import Flask, render_template, url_for, request, flash, session, redirect, abort, g, make_response

import dbscripts as db


app = Flask(__name__)
app.config['SECRET_KEY'] = 'aboba1488'


@app.route('/')
def index():
    return render_template('index.html', class1 = 'active', class2 = '', class3 = '')

@app.route('/pid', methods=('GET', 'POST'))
def pid():
    if request.method == 'POST':
        result = db.get_contracts_pid(request.form['pid'])
    return render_template('searchResult.html', result = result, result_len = len(result), class1 = 'active', class2 = '', class3 = '')

@app.route('/shop', methods = ('GET', 'POST'))
def shop():
    if request.method == 'POST':
        result = db.get_contracts_shop(request.form['shop'])
    return render_template('searchResult.html', result = result, result_len = len(result), class1 = 'active', class2 = '', class3 = '')

@app.route('/application/<id>', methods = ('GET', 'POST'))
def application(id):
    if request.method == 'POST':
        result = db.get_contract_id(id)
    return render_template('application.html', result = result, class1 = 'active', class2 = '', class3 = '')

@app.route('/update', methods = ('GET', 'POST'))
def update():
    if request.method == 'POST':
        if request.form['password'] == '1488':
            file = request.files['file']
            if file and db.db_update(file):
                flash('Импорт успешно выполнен', category = 'success')
            else:
                flash('Импорт не выполнен', category = 'error')
        else:
            flash('Неверный пароль', category = 'wrongpass')
    return render_template('update.html', class1 = '', class2 = 'active', class3 = '')

@app.route('/about')
def about():
    return render_template('about.html', class1 = '', class2 = '', class3 = 'active')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)