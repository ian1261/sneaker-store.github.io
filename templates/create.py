# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for
import pymysql

# 創建一個 MySQL 連線
db = pymysql.connect(host='localhost',
                     port='3306',
                     user='user',
                     password='12345678',
                     database='SNEAKERS',
                     charset='utf8mb4',
                     cursorclass=pymysql.cursors.DictCursor)

# 初始化 Flask 伺服器
app = Flask(__name__)
app.secret_key = "any string but secret"

# 處理路由
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/success")
def success():
    return render_template("success.html")

# /error?msg=錯誤訊息
@app.route("/error")
def error():
    message = request.args.get("msg", "信箱已被註冊!")
    return render_template("error.html", message=message)

@app.route("/about")
def about():
    return render_template("about us.html")

@app.route("/signup", methods=["POST"])
def signup():
    # 從前端接收資料
    nickname = request.form["nickname"]
    email = request.form["email"]
    account = request.form["account"]
    password = request.form["password"]

    # 根據收到的資料，和資料庫互動
    cursor = db.cursor()

    # 檢查會員集合中是否有相同Email的文件資料
    cursor.execute("SELECT * FROM user WHERE email=%s", (email,))
    result = cursor.fetchone()

    if result is not None:
        return redirect("/error?message=信箱已被註冊")

    # 把資料放進資料庫，完成註冊
    cursor.execute("INSERT INTO user (nickname, email, account, password) VALUES (%s, %s, %s, %s)", (nickname, email, account, password))
    db.commit()
    return redirect("/success")

@app.route("/signin", methods=["POST"])
def signin():
    # 從前端取得使用者得輸入
    account = request.form["account"]
    password = request.form["password"]

    # 和資料庫做互動
    cursor = db.cursor()

    # 檢查帳號密碼是否正確
    cursor.execute("SELECT * FROM user WHERE account=%s AND password=%s", (account, password))
    result = cursor.fetchone()

    # 找不到資料。登入失敗，導向錯誤頁面
    if result is None:
        return redirect("/error?msg=帳號或密碼輸入錯誤")
    # 登入成功，導向會員頁面
    return redirect("/success")

@app.route("/SAMBA")
def SAMBA():
    return render_template("SAMBA OG.html")

if __name__ == "__main__":
    app.run(port=3000)
