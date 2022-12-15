from flask import Flask, render_template, url_for, request, flash, session, redirect, abort, g, make_response

import sqlite3, os, math, time, re

app = Flask(__name__)

@app.route('/')
def index():
    print(url_for('index'))
    return render_template('index.html')

@app.route('/pid', methods=('GET', 'POST'))
def pid():
    result = 'сасать, нет такого магазина, лох'
    if request.method == 'POST':
        if request.form['pid'] == '228':
            result = request.form['pid']
 
    return render_template('searchResult.html', result = result)

@app.route('/shop', methods=('GET', 'POST'))
def shop():
    result = 'сасать, нет такого магазина, лох'
    if request.method == 'POST':
        if request.form['shop'] == 'магазин':
            result = request.form['shop']
 
    return render_template('searchResult.html', result = result)

if __name__ == '__main__':
    app.run(debug=True)