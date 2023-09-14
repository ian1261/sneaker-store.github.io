from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # 帳號密碼驗證
    if username == 'admin1' and password == 'admin1':
        response = {'success': True, 'message': '登入成功！'}
    else:
        response = {'success': False, 'message': '帳號或密碼錯誤！'}

    return jsonify(response)

if __name__ == '__main__':
    app.run()
