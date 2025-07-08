from flask import Flask, request, render_template, redirect, url_for, session
import threading
import time
import requests

app = Flask(__name__)
app.secret_key = 'dev-secret-key'  # 실제 배포 시 환경변수로 분리 권장

# === 1. 로그인 페이지 ===
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # 입력한 아이디/비밀번호 로그에 출력
        print(f"[로그인 시도] 아이디: {username}, 비밀번호: {password}")

        # 로그인 성공 처리 (실제 인증은 구현하지 않음)
        session['username'] = username
        return redirect(url_for('survey'))

    return render_template('login.html')


# === 2. 설문 페이지 ===
@app.route('/survey')
def survey():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('survey.html', username=session['username'])


# === 3. 설문 제출 처리 ===
@app.route('/submit', methods=['POST'])
def submit():
    if 'username' not in session:
        return redirect(url_for('login'))

    name = request.form.get('name')
    email = request.form.get('email')
    feedback = request.form.get('feedback')

    q1 = request.form.get('q1')
    q2 = request.form.get('q2')
    q3 = request.form.get('q3')
    ad_agree = request.form.get('ad_agree')  # 체크 안 하면 None

    # 서버 콘솔 로그 기록
    print(f"[설문 제출] 참여자: {name}, 이메일: {email}")
    print(f" - 개인정보 침해 경험: {q1}")
    print(f" - 걱정되는 유형: {q2}")
    print(f" - 실천 방법: {q3}")
    print(f" - 자유 의견: {feedback}")
    print(f" - 광고 수신 동의: {'예' if ad_agree else '아니오'}")

    return render_template('thankyou.html', name=name, q1=q1, ad_agree=ad_agree)


# === 4. 로그아웃 처리 ===
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


# === 5. Keep-alive 핑 기능 (Render 무료 서버용) ===
def keep_alive_ping():
    while True:
        try:
            url = "https://<너의-서버-주소>.onrender.com/"  # 여기에 실제 주소 입력!
            res = requests.get(url)
            print(f"[PING] 서버 응답 코드: {res.status_code}")
        except Exception as e:
            print(f"[PING 실패] {e}")
        time.sleep(840)  # 14분 주기 (Render 무료는 15분 미사용 시 슬립됨)


# === 6. 앱 실행 ===
if __name__ == '__main__':
    # Keep-alive 스레드 실행
    ping_thread = threading.Thread(target=keep_alive_ping, daemon=True)
    ping_thread.start()

    # Flask 앱 실행
    app.run(debug=True)
