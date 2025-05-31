from flask import Flask, request, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = '비밀키'  # 세션을 위한 비밀키

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # 입력한 아이디/비밀번호 로그에 출력
        print(f"[로그인 시도] 아이디: {username}, 비밀번호: {password}")

        # 무조건 로그인 성공 처리
        session['username'] = username
        return redirect(url_for('survey'))

    return render_template('login.html')

@app.route('/survey')
def survey():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('survey.html', username=session['username'])

@app.route('/submit', methods=['POST'])
def submit():
    if 'username' not in session:
        return redirect(url_for('login'))

    name = request.form.get('name')
    email = request.form.get('email')
    feedback = request.form.get('feedback')

    print(f"[설문 제출] 참여자: {name}, 이메일: {email}, 의견: {feedback}")
    return render_template('thankyou.html', name=name)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
