from flask import Flask, render_template, url_for, request, flash, session, redirect, abort, g, make_response

import sqlite3, os, math, time, re

app = Flask(__name__)



@app.route('/')
def index():
    print(url_for('index'))
    return render_template('index.html', class1 = 'active', class2 = '', class3 = '')

@app.route('/pid', methods=('GET', 'POST'))
def pid():
    result = 'сасать, нет такого магазина, лох'
    if request.method == 'POST':
        if request.form['pid'] == '228':
            result = request.form['pid']
    return render_template('searchResult.html', result = result, class1 = 'active', class2 = '', class3 = '')

@app.route('/shop', methods=('GET', 'POST'))
def shop():
    result = 'сасать, нет такого магазина, лох'
    if request.method == 'POST':
        if request.form['shop'] == 'магазин':
            result = request.form['shop']
    return render_template('searchResult.html', result = result, class1 = 'active', class2 = '', class3 = '')

@app.route('/update')
def update():
    return render_template('update.html', class1 = '', class2 = 'active', class3 = '')

@app.route('/about')
def about():
    return render_template('about.html', class1 = '', class2 = '', class3 = 'active')

if __name__ == '__main__':
    app.run(debug=True)