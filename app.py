# -*- coding: utf-8 -*-
# 載入pymongo 套件
from flask import Flask, render_template, request, redirect, url_for
import pymongo
import certifi
ca = certifi.where()
# 創建一個MongoClient，並設置ssl=False以禁用SSL驗證
client = pymongo.MongoClient("mongodb+srv://root:root123@mycluster.xc25zra.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=ca)
# 選擇操作 test 資料庫

db = client.member_system
print("資料庫連線建立成功")
#初始化 Flask 伺服器
from flask import *
app=Flask(__name__,)
app.secret_key="any string but secret"
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
  message=request.args.get("msg", "信箱已被註冊!")
  return render_template("error.html", message=message)

@app.route("/about")
def about ():
  return render_template("about us.html")

@app.route("/signup",methods=["POST"])
def signup():
  # 從前端接收資料
  nickname=request.form["nickname"]
  email=request.form["email"]
  account=request.form["account"]
  password=request.form["password"]
  # 根據收到的資料，和資造庫互動
  collection=db.user
  # 檢查會員集合中是否有相同Email的文件資料
  result=collection.find_one({
    "email":email
  })
  if result != None:
    return redirect("/error?message=信箱已被註冊")
  #把資料放進資料庫，完成註冊
  collection.insert_one({
    "nickname":nickname,
    "email":email,
    "account":account,
    "password":password
  })
  return redirect("/success")
@app.route("/signin",methods=["POST"])
def signin():
  # 從前端取得使用者得輸入
  account=request.form["account"]
  password=request.form["password"]
  # 和資料庫做互動
  collectiion=db.user
  # 檢查帳號密碼是否正確
  result=collectiion.find_one({
    "$and":[
      {"account":account},
      {"password":password}
    ]
  })
  # 找不到資料。登入失敗，導向錯誤頁面
  if result==None:
    return redirect("/error?msg=帳號或密碼輸入錯誤")
  # 登入成功，導向會員頁面
  return redirect("/success")

@app.route("/SAMBA")
def SAMBA():
  return render_template("SAMBA OG.html")

app.run(port=3000)

