from flask import Flask, render_template, session, request, redirect
from datetime import timedelta

app = Flask(__name__)

app.secret_key = "aaakjjklkhjgkjgk"

user_data = {}

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)

@app.route("/", methods=["GET"])
def index():
    if "flag" in session and session["flag"]:
        msg = "hello,"+ str(session["uid"])
        return render_template("index.html",title="ログイン後の画面です",message=msg)
    else:
        return redirect("/login")


@app.route('/login', methods=['GET'])
def login():
    return render_template("login.html", title="ログインページ", message="以下のフォームからログインしてね")


@app.route('/login', methods=['POST'])
def login_post():
    uid = request.form["uid"]
    pwd = request.form["pwd"]
    # print(f'{uid},{pwd}')
    # print(user_data)
    #ユーザが登録済みであった場合
    if uid in user_data:
        # IDとパスワードの組み合わせが合っていれば、ログイン済みにする
        if user_data[uid] == pwd:
            session["flag"] = True
        #　ログイン済みにしない
        else:
            session["flag"] = False
    #ユーザが登録していなかった場合、登録してログイン済みにする
    else:
        user_data[uid] = pwd
        session["flag"] = True

    session["uid"] = uid
    if session["flag"]:
        return redirect("/")
    else:
        return render_template("login.html",title="ログインページ",message="パスワードが違います")

@app.route('/logout')
def logout():
    print(session['flag'])
    print(session['uid'])
    session.pop('uid', None)
    session.pop("flag", None)
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)