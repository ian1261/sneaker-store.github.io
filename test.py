# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import pymysql 
import os
import datetime




# 創建一個 MySQL 連線
db = pymysql.connect(host='localhost',
                    port=3306,
                    user='root',
                    password='12345678'.encode('utf-8'),
                    database='SNEAKERS',
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor)

# 初始化 Flask 伺服器
app = Flask(__name__)
app.secret_key = "any string but secret"

# 處理路由
@app.route("/")
def index():
    if "nickname" in session:
        return redirect("/success")
    else:
        return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/success")
def success():
    if "nickname" in session:
        return render_template("success.html")
    else:
        return redirect("/")

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
    session["nickname"] = result["nickname"]
    return redirect("/success")

@app.route("/SAMBA")
def SAMBA():
    return render_template("SAMBA OG.html")

@app.route("/JA1")
def JA1():
    return render_template("JA1.html")

@app.route("/force")
def force():
    return render_template("force.html")

@app.route("/max")
def max():
    return render_template("max.html")

@app.route("/su")
def su():
    return render_template("su.html")


@app.route("/nb5740")
def nb5740():
    return render_template("5740.html")

@app.route("/nb327")
def nb327():
    return render_template("327.html")

@app.route("/all")
def all():
    return render_template("all.html")

@app.route("/ok")
def ok():
    return render_template("ok.html")

@app.route("/order")
def order():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM orders WHERE nickname=%s", (session["nickname"],))
    orders = cursor.fetchall()
    return render_template("order.html", orders=orders)

@app.route("/signout")
def signout():
    del session["nickname"]
    return redirect("/")

@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    data = request.get_json()
    nickname = session.get("nickname", None)
    if nickname is None:
        return jsonify({"message": "請先登入帳號"})

    product_name = data["product_name"]
    size = data["size"]
    quantity = data["quantity"]
    price = data["price"]

    cursor = db.cursor()
    cursor.execute("INSERT INTO purchase (nickname, product_name, size, quantity, price) VALUES (%s, %s, %s, %s,%s)",
                    (nickname, product_name, size, quantity, price))
    db.commit()
    return jsonify({"message": "已將商品添加到購物車"})

@app.route("/cart")
def cart():

    if "nickname" not in session:
        return redirect("/login")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM purchase WHERE nickname=%s", (session["nickname"],))
    purchases = cursor.fetchall()
    return render_template("cart.html", purchases=purchases)

@app.route("/remove_from_cart", methods=["POST"])
def remove_from_cart():
    data = request.get_json()
    nickname = data["nickname"]
    product_name = data["product_name"]
    size = data["size"]

    cursor = db.cursor()
    cursor.execute("DELETE FROM purchase WHERE nickname=%s AND product_name=%s AND size=%s", (nickname, product_name, size))
    db.commit()
    return jsonify({"message": "已從購物車中刪除商品"})

@app.route("/confirm_purchase", methods=["POST"])
def confirm_purchase():
    if "nickname" not in session:
        return redirect("/login")

    nickname = session["nickname"]
    date = datetime.datetime.now().date()

    cursor = db.cursor()

    cursor.execute("SELECT * FROM purchase WHERE nickname=%s", (nickname,))
    purchases = cursor.fetchall()

    total = sum([purchase["price"] * purchase["quantity"] for purchase in purchases])

    for purchase in purchases:
        cursor.execute("INSERT INTO orders (nickname, date, product_name, size, quantity, total) VALUES (%s, %s, %s, %s, %s, %s)",
                       (nickname, date, purchase["product_name"], purchase["size"], purchase["quantity"], total))
    db.commit()

    # 清空購物車
    cursor.execute("DELETE FROM purchase WHERE nickname=%s", (nickname,))
    db.commit()
    return redirect("/order")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)