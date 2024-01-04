from flask import Flask, session, render_template, redirect, Blueprint, request

from model.Usser import User
from utils.errorResponse import errorResponse

from config import Config
from db import db
import re

app = Flask(__name__)


# 注册配置
app.config.from_object(Config)
db.init_app(app)

from views.page import page
from views.user import user

app.register_blueprint(page.pb)
app.register_blueprint(user.ub)


# 初始化定义


@app.route('/')
def index():
    return redirect('user/login')


@app.before_request
def before_request():
    pat = re.compile(r'^/static')
    if re.search(pat, request.path):
        return
    if request.path == '/user/login':
        return
    if request.path == '/user/register':
        return
    uname = session.get('username')
    if uname:
        return None
    return redirect('/user/login')


@app.route('/<path:path>')
def catch_all(path):
    return render_template('error.html')


if __name__ == '__main__':
    app.run()
