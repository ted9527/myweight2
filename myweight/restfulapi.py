from sqlalchemy.sql.sqltypes import Interval
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask import request, jsonify

import datetime
from datetime import datetime
import datetime as dt
from sqlalchemy import desc

from myweight import app,db

from myweight.models import User, EverydayWeight

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import datetime as dt
import matplotlib.dates as mdates

##########################################################################################################################
#
# RESTful API - C(reate)R(ead)U(pdate)D(elete) of weight record
#
# ---------------------------------- Create ----------------------------------  
# request:  POST    127.0.0.1:5000/myweight/api/v0.2/weights
# with Body JSON 
#
"""    
 {
    "date": "2020-08-06",
    "username": "ted",
    "weight": 66.6
 }
"""
@app.route('/myweight/api/v0.2/weights', methods=['POST'])
@jwt_required
def add_weight():
    weight = request.get_json()
    if weight is None:
        return {'error': 'You need input the context which need to be created'}, 400
    #weight is a json, not a list, so no need to use weight[0]['username']
    inputted_username = weight['username']
    inputted_date = weight['date']
    inputted_weight = weight['weight']
    formatted_inputted_date = datetime.strptime( inputted_date , '%Y-%m-%d')
    #get logined username
    logined_username = get_jwt_identity()
    #User could only add his/her weitht, could not add other people's weight
    if not inputted_username == logined_username:
        return {'error': 'You can only add your weight'}, 403
    todayWeight = EverydayWeight(username = inputted_username,date = formatted_inputted_date ,weight = inputted_weight)
    #check if the date's weight is already existed in DB
    everydayWeights = EverydayWeight.query.filter_by(username=inputted_username).order_by(desc(EverydayWeight.date)).all()
    for myEverydayWeight in everydayWeights:
        if  myEverydayWeight.date == formatted_inputted_date:  
            return {'error': 'There is already a weight record for the inputted date'}, 403
            break
    db.session.add(todayWeight)  # 添加到数据库会话
    db.session.commit()  # 提交数据库会话
    return {'added':'yes'},200 

# ---------------------------------- Read ---------------------------------- 
# get all weights recored which belongs to the logined user
# 1.  get all dates record 
# request:  GET     127.0.0.1:5000/myweight/api/v0.2/weights
# respone:
""" 
[
  {
    "date": "2020-08-06 00:00",
    "id": 2,
    "username": "ted",
    "weight": 63.4
  },
  {
    "date": "2020-08-17 00:00",
    "id": 3,
    "username": "ted",
    "weight": 63.4
  },
  {
    "date": "2020-08-18 00:00",
    "id": 4,
    "username": "ted",
    "weight": 66.6
  }
] 
"""
# 2.  get one specify date's record 
# request:  GET     127.0.0.1:5000/myweight/api/v0.2/weights?date=2020-08-06
# respone:  
"""
# {
#    "date": "2020-08-06 00:00",
#    "id": 2,
#    "username": "ted",
#    "weight": 63.4
# }
"""

@app.route('/myweight/api/v0.2/weights', methods=['GET'])
@jwt_required
def get_weight():

    #parse parameter
    args = request.args
    query_date = ""
    if not len(args) == 0:
        #if args.keys()
        #if args.has_key('username'):
        query_date = args['date']
        formatted_inputted_date = datetime.strptime( query_date , '%Y-%m-%d')

    logined_username = get_jwt_identity()
    allweight_list = []
    oneDayWeight = ""
    if query_date == "":
        allweights = EverydayWeight.query.filter_by(username=logined_username).order_by(desc(EverydayWeight.date)).all()
        for weight in allweights:
            allweight_list.append(weight.to_dict())
        return jsonify(allweight_list)
    else:
        allweights = EverydayWeight.query.filter_by(username=logined_username,date=formatted_inputted_date).order_by(EverydayWeight.date).all()
        oneDayWeight = allweights[0].to_dict()
        return jsonify(oneDayWeight)
    
    #everydayWeights_normal_order = list(reversed(allweights))  
    #return jsonify(json.dumps(everydayWeights_normal_order))
    ##return jsonify(json.dumps(allweight_list))
    

# ---------------------------------- Update ---------------------------------- 
# request:  PUT    127.0.0.1:5000/myweight/api/v0.2/weights
# with Body JSON 
#
"""    
 {
    "date": "2020-08-06",
    "username": "ted",
    "weight": 66.6
 }
"""
@app.route('/myweight/api/v0.2/weights', methods=['PUT']) 
@jwt_required
def update_weight():
    weight = request.get_json()
    if weight is None:
        return {'error': 'You need input the context which need to be updated'}, 400
    inputted_username = weight['username']
    inputted_date = weight['date']
    inputted_weight = weight['weight']
    formatted_inputted_date = datetime.strptime( inputted_date , '%Y-%m-%d')
    #get logined username
    logined_username = get_jwt_identity()
    #User could only add his/her weitht, could not add other people's weight
    if not inputted_username == logined_username:
        return {'error': 'You can only update your weight'}, 403
    toUpdate = EverydayWeight(username = inputted_username,date = formatted_inputted_date ,weight = inputted_weight)
    #check if the date's weight is existed in DB
    theOneInDb = EverydayWeight.query.filter_by(username=inputted_username,date=formatted_inputted_date).first()
    if theOneInDb == None:  
        return {'error': 'There is no related date need to be updated'}, 403
    theOneInDb.weight = inputted_weight
    db.session.commit()  # 提交数据库会话
    return {'updated':'yes'},200 

# ---------------------------------- Delete ----------------------------------
# request:  DELETE    127.0.0.1:5000/myweight/api/v0.2/weights?date=2020-08-06
# 
#
@app.route('/myweight/api/v0.2/weights', methods=['DELETE'])
@jwt_required
def delete_weight():
    logined_username = get_jwt_identity()
    #parse parameter
    args = request.args
    query_date = ""
    if not len(args) == 0:
        #if args.keys()
        #if args.has_key('username'):
        query_date = args['date']
        formatted_inputted_date = datetime.strptime( query_date , '%Y-%m-%d')
    else:
        return {'error': 'Please specify a date to be deleted'}, 400 
    #check if the date's weight is existed in DB
    theOneInDb = EverydayWeight.query.filter_by(username=logined_username,date=formatted_inputted_date).first()
    if theOneInDb == None:  
        return {'error': 'There is no related date need to be deleted'}, 403 
    db.session.delete(theOneInDb)  # 删除对应的记录
    db.session.commit()  # 提交数据库会话
    return {'deleted':'yes'},200

##########################################################################################################################
#
# RESTful API - User Sign up and Log in 
#
# Requset   127.0.0.1:5000/myweight/api/v0.2/login
# Requset   127.0.0.1:5000/myweight/api/v0.2/signup
# with JSON 
# 
""" 
{
    "username": "ted",
    "password": "xxxx"
}
"""
# Response
#
""" 
{
  "token": "xxxxxxxxxx"
}
""" 
@app.route('/myweight/api/v0.2/login', methods=['POST'])
def restful_login():
    loginInfo = request.get_json()
    if loginInfo is None:
        return {'error': 'You need input username and password in JSON to login'}, 400
    user = User.query.filter_by(username=loginInfo.get('username')).first()
    if user is None or not user.validate_password(loginInfo.get('password')):
        return {'error': 'Username or password invalid'}, 401
    #login_user(user, remember=form.remember_me.data)
    expires = dt.timedelta(days=7)   
    access_token = create_access_token(identity=str(loginInfo.get('username')), expires_delta=expires)
    print("Incoming login request received...")
    user.token = access_token
    user.password_hash = None   
    # return {'token': access_token}, 200
    return jsonify(user.to_dict( rules=('token', 'method')))


@app.route('/myweight/api/v0.2/signup', methods=['POST'])
def restful_signup():
    loginInfo = request.get_json()
    if loginInfo is None:
        return {'error': 'You need input username and password in JSON to sign up'}, 400
    user = User(username=loginInfo.get('username'))
    user.set_password(loginInfo.get('password'))
    db.session.add(user)
    db.session.commit()
    expires = dt.timedelta(days=7)   
    access_token = create_access_token(identity=str(loginInfo.get('username')), expires_delta=expires)
    user.token = access_token
    user.password_hash = None   
    # return {'token': access_token}, 200
    return jsonify(user.to_dict( rules=('token', 'method')))

#################################### Chart #################################################
def getDummy(a,b,n):
    dummyList = []
    if a > b:
        for i in range(1,n):
            dummyList.append(b + (n-i)/n*(a-b) )
    if a <= b:
        for i in range(1,n):
            dummyList.append(a + i/n*(b-a) )
    return dummyList
    
@app.route('/myweight/api/v0.2/chart', methods=['GET'])
@jwt_required
def get_chart():

    logined_username = get_jwt_identity()
    #取得最近7天的记录 （最多7天，但也可能为0天或者小于7天的数字）
    everydayWeights = EverydayWeight.query.filter_by(username=logined_username).order_by(desc(EverydayWeight.date)).all()[:7]
    everydayWeights_normal_order = list(reversed(everydayWeights))  
    numOfLoggedDays = EverydayWeight.query.filter_by(username=logined_username).count()
    fig = plt.figure()
    ax2 = fig.add_subplot(111)
    if numOfLoggedDays > 0:
        date1 = everydayWeights_normal_order[0].date  
        date2 = everydayWeights_normal_order[len(everydayWeights_normal_order)-1].date   
        delta = dt.timedelta(days=1)
        date3 = date2 + delta
        days = (date2 - date1).days
        daysnum = len(everydayWeights_normal_order)
        
        y2 = []
        #if only one day record exist
        if daysnum == 1:
            y2 = [everydayWeights_normal_order[0].weight]
            dates2 = date1
        else:
            for i in range(0, daysnum):
                y2.append(everydayWeights_normal_order[i].weight)
                if i == daysnum -1:
                    break
                deltaDays = (everydayWeights_normal_order[i+1].date - everydayWeights_normal_order[i].date).days
                if deltaDays > 1:
                    listD = getDummy(everydayWeights_normal_order[i].weight, everydayWeights_normal_order[i+1].weight, deltaDays) 
                    y2 = y2 + listD
            
            dates2 = mpl.dates.drange(date1, date3, delta)
        ax2.plot_date(dates2, y2, linestyle='-') 

        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
        if days < 18:
            ax2.xaxis.set_major_locator(mdates.DayLocator())   
        elif days < 126:
            ax2.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=matplotlib.dates.MO))
        else:
            ax2.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=matplotlib.dates.MO, interval=((days//126)+1)))
        # Plot
    
        fig.autofmt_xdate(bottom=0.18)
        fig.subplots_adjust(left=0.18)

        plt.gcf().autofmt_xdate()
        plt.savefig("./myweight/static/img/chart.png")

        plt.close()

    return {'image OK':'yes'},200

@app.route('/myweight/api/v0.2/chartall', methods=['GET'])
@jwt_required
def get_chartall():

    logined_username = get_jwt_identity()
    everydayWeights = EverydayWeight.query.filter_by(username=logined_username).order_by(desc(EverydayWeight.date)).all()
    everydayWeights_normal_order = list(reversed(everydayWeights))  
    numOfLoggedDays = EverydayWeight.query.filter_by(username=logined_username).count()
    fig = plt.figure()
    ax2 = fig.add_subplot(111)
    if numOfLoggedDays > 0:
        date1 = everydayWeights_normal_order[0].date  
        date2 = everydayWeights_normal_order[len(everydayWeights_normal_order)-1].date   
        delta = dt.timedelta(days=1)
        date3 =date2 + delta
        days = (date2 - date1).days
        daysnum = len(everydayWeights_normal_order)
        
        y2 = []
        #if only one day record exist
        if daysnum == 1:
            y2 = [everydayWeights_normal_order[0].weight]
            dates2 = date1
        else:
            for i in range(0, daysnum):
                y2.append(everydayWeights_normal_order[i].weight)
                if i == daysnum -1:
                    break
                deltaDays = (everydayWeights_normal_order[i+1].date - everydayWeights_normal_order[i].date).days
                if deltaDays > 1:
                    listD = getDummy(everydayWeights_normal_order[i].weight, everydayWeights_normal_order[i+1].weight, deltaDays) 
                    y2 = y2 + listD 
            dates2 = mpl.dates.drange(date1, date3,delta)

        ax2.plot_date(dates2, y2, linestyle='-') 

        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
        if days < 18:
            ax2.xaxis.set_major_locator(mdates.DayLocator())   
        elif days < 126:
            ax2.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=matplotlib.dates.MO))
        else:
            ax2.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=matplotlib.dates.MO, interval=((days//126)+1)))
        #
        # Plot
    
        fig.autofmt_xdate(bottom=0.18)
        fig.subplots_adjust(left=0.18)

        plt.gcf().autofmt_xdate()
        plt.savefig("./myweight/static/img/chartall.png")

        plt.close()
    return {'image OK':'yes'},200
