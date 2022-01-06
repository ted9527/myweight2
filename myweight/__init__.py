import os
import sys

from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy


from flask_jwt_extended import JWTManager

WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'
    
app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path), os.getenv('DATABASE_FILE', 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY', 'my_jwt_token')

# 在扩展类实例化前加载配置
db = SQLAlchemy(app)
jwt = JWTManager(app)

from myweight import models
from myweight import errors, commands, restfulapi

