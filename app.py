from flask import Flask, render_template, url_for, request, flash, session, redirect, abort, g, make_response

import sqlite3, os, math, time, re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)