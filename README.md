# MyWeight

A weight record tool

V0.2 functionality:
1. add/edit/delete any day's weight
2. view the weight record the most 7 days or all days (since v0.1)
3. view the chart of weight record of the most 7 days or all days (since v0.1)

V0.2 technology: 
1. Backend: Flask Framework (since v0.1) 
2.          Restful API
3.          JWT token-based authentication         
4. Frontend: Bulma -- CSS (since v0.1) 
5.           Vue (Vuex) -- Framework
6.           Axios -- handle HTTP request
7.           bulma-calendar -- a calenndar date control 
  
Obsolete:
Backend: Form validation -- Flask-WTF 
Frontend: submit local date to server side -- moment.js and jQuery3.5.1.js

## Installation

clone:
```
$ git clone https://github.com/ted9527/myweight2.git
$ cd myweight2
```
create & active virtual enviroment then install dependencies:
```
$ python -m venv env  # use `virtualenv env` for Python2, use `python3 ...` for Python3 on Linux & macOS
$ . env/Scripts/activate  # use `source env/bin/activate` on Windows
$ pip install -r requirements.txt
```

generate fake data then run:
```
$ flask initdb
$ flask run
* Running on http://127.0.0.1:5000/
```

## Run after installation
```
$ cd myweight2
$ . env/Scripts/activate
$ flask run
* Running on http://127.0.0.1:5000/
```

## License

This project is licensed under the MIT License (see the
[LICENSE](LICENSE) file for details).

## About .flaskenv file

Since the fold name is myweight2, however the app name is myweight,
so need to specify the APP name to FLASK in .flaskenv file