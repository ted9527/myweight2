from werkzeug.security import generate_password_hash, check_password_hash

from myweight import db

from sqlalchemy_serializer import SerializerMixin

class EverydayWeight(db.Model, SerializerMixin):  # 表名将会是 everydayweight（自动生成，小写处理）
    id = db.Column(db.Integer, primary_key=True)  # 主键
    username = db.Column(db.String(20))  # 用户名
    date = db.Column(db.DateTime)  
    weight = db.Column(db.Float)

class User(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))  # 用户名
    password_hash = db.Column(db.String(128))  # 密码散列值
    token: str = ''

    def method(self):
        return "forTokenSerialize" 

    def set_password(self, password):  # 用来设置密码的方法，接受密码作为参数
        self.password_hash = generate_password_hash(password)  # 将生成的密码保持到对应字段

    def validate_password(self, password):  # 用于验证密码的方法，接受密码作为参数
        return check_password_hash(self.password_hash, password)  # 返回布尔值